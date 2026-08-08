require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { createClient } = require('@supabase/supabase-js');
const stripeKey = process.env.STRIPE_SECRET_KEY;
const stripe = stripeKey ? require('stripe')(stripeKey) : null;

const app = express();
const PORT = process.env.PORT || 8080;

// Configuración de Supabase
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

let supabase;
let supabaseAdmin; // Para crear usuarios de Staff sin perder sesión

if (supabaseUrl && supabaseKey) {
    supabase = createClient(supabaseUrl, supabaseKey);
    console.log('✅ Conectado a Supabase (Cliente)');
} else {
    console.log('⚠️ Supabase no configurado aún (Faltan variables en .env)');
}

if (supabaseUrl && supabaseServiceKey) {
    supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey, {
        auth: { autoRefreshToken: false, persistSession: false }
    });
    console.log('🛡️ Conectado a Supabase (Admin API)');
}

// --- AUTH MIDDLEWARE (FIREWALL) ---
const requireMerchantAuth = async (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ success: false, error: 'Unauthorized' });
    }
    const token = authHeader.split(' ')[1];
    const { data: { user }, error } = await supabase.auth.getUser(token);
    
    if (error || !user) {
        return res.status(401).json({ success: false, error: 'Invalid token' });
    }
    
    // RBAC: Si es cajero, su dueño es merchant_id. Si es dueño, su id es su merchant_id.
    if (user.user_metadata && user.user_metadata.role === 'staff') {
        req.merchantId = user.user_metadata.merchant_id;
        req.userRole = 'staff';
    } else {
        req.merchantId = user.id;
        req.userRole = 'admin';
    }
    
    next();
};

const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, 
    max: 100,
    message: { error: 'Demasiadas peticiones, por favor intenta más tarde.' }
});

app.use(helmet({
    contentSecurityPolicy: false
}));

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logging middleware
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();
});

// --- API ESCÁNER (STAFF) ---

// 1. Buscar Cliente por ID (QR)
app.get('/api/scanner/customer/:id', apiLimiter, requireMerchantAuth, async (req, res) => {
    const customerId = req.params.id;
    
    try {
        const { data: customer, error } = await supabase
            .from('customers')
            .select('*')
            .eq('id', customerId)
            .eq('merchant_id', req.merchantId)
            .single();
            
        if (error || !customer) {
            return res.status(404).json({ success: false, error: 'Cliente no encontrado o no pertenece a este comercio.' });
        }
        
        res.json({ success: true, customer });
    } catch (err) {
        res.status(500).json({ success: false, error: 'Error interno' });
    }
});

// 2. Procesar Transacción
app.post('/api/scanner/transaction', apiLimiter, requireMerchantAuth, async (req, res) => {
    const { customerId, amount, type } = req.body;
    // type: 'earn' (Dar puntos) o 'redeem' (Cobrar)
    
    if (!customerId || !amount || amount <= 0 || !['earn', 'redeem'].includes(type)) {
        return res.status(400).json({ success: false, error: 'Datos inválidos' });
    }
    
    try {
        // Verificar que el cliente es de este comercio
        const { data: customer, error: fetchErr } = await supabase
            .from('customers')
            .select('*')
            .eq('id', customerId)
            .eq('merchant_id', req.merchantId)
            .single();
            
        if (fetchErr || !customer) {
            return res.status(404).json({ success: false, error: 'Cliente no encontrado.' });
        }

        let newBalance = customer.current_balance;
        let earned = 0;
        let redeemed = 0;

        if (type === 'earn') {
            // Ejemplo: 5% de Cashback
            earned = amount * 0.05;
            newBalance += earned;
        } else if (type === 'redeem') {
            if (customer.current_balance < amount) {
                return res.status(400).json({ success: false, error: 'Saldo insuficiente.' });
            }
            redeemed = amount;
            newBalance -= redeemed;
        }

        // Actualizar Cliente
        const { error: updateErr } = await supabase
            .from('customers')
            .update({ 
                current_balance: newBalance,
                lifetime_value: customer.lifetime_value + (type === 'earn' ? amount : 0),
                visits: customer.visits + 1
            })
            .eq('id', customerId);

        if (updateErr) throw updateErr;

        // Registrar Transacción
        await supabase
            .from('transactions')
            .insert([{
                merchant_id: req.merchantId,
                customer_id: customerId,
                amount: amount,
                type: type
            }]);
            
        let reviewTriggered = false;
        
        // --- GOOGLE MAPS REVIEW TRIGGER ---
        if (customer.visits === 0) {
            // Es su primera visita! Traer el URL de Google Maps del merchant
            const { data: merchantData } = await supabase
                .from('merchants')
                .select('google_maps_url, business_name')
                .eq('id', req.merchantId)
                .single();
                
            if (merchantData && merchantData.google_maps_url) {
                // SIMULATE SENDING PUSH NOTIFICATION
                console.log(`[UNICORN ENGINE] 🚀 Disparando Push Notification a ${customer.name}`);
                console.log(`[UNICORN ENGINE] 📝 Mensaje: "¡Gracias por tu primera visita a ${merchantData.business_name}! ¿Nos regalas 5 estrellas? ⭐⭐⭐⭐⭐"`);
                console.log(`[UNICORN ENGINE] 🔗 Enlace: ${merchantData.google_maps_url}`);
                reviewTriggered = true;
            }
        }

        res.json({ 
            success: true, 
            newBalance, 
            pointsEarned: earned, 
            amountRedeemed: redeemed,
            reviewTriggered
        });

    } catch (err) {
        res.status(500).json({ success: false, error: 'Error procesando transacción.' });
    }
});

// -------------------------------------------------------------
// WEBHOOK DE STRIPE (Debe ir antes del body parser JSON)
// -------------------------------------------------------------
app.post('/api/stripe/webhook', express.raw({type: 'application/json'}), async (req, res) => {
    const sig = req.headers['stripe-signature'];
    const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

    if (!endpointSecret) {
        console.warn("⚠️ Advertencia: No hay STRIPE_WEBHOOK_SECRET configurado. El webhook no se puede verificar.");
        return res.status(400).send('Webhook secret missing');
    }

    let event;
    try {
        event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
    } catch (err) {
        console.error(`❌ Webhook Error: ${err.message}`);
        return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    // Manejar el evento de pago exitoso
    if (event.type === 'checkout.session.completed') {
        const session = event.data.object;
        const merchantId = session.client_reference_id;
        
        if (merchantId && supabase) {
            console.log(`✅ Pago exitoso para el comercio: ${merchantId}`);
            // Actualizar el estado en la base de datos a ACTIVO
            await supabase
                .from('merchants')
                .update({ plan_status: 'active', stripe_customer_id: session.customer })
                .eq('id', merchantId);
        }
    }

    res.json({received: true});
});

// Middleware de Seguridad Básica eliminado (ya está arriba)
app.use(express.urlencoded({ extended: true }));

// Servir archivos estáticos (Frontend)
app.use(express.static(path.join(__dirname, '/'), { 
    index: false,
    setHeaders: (res, path) => {
        if (path.endsWith('.html')) {
            res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, private');
        }
    }
}));

// --- RUTAS DEL API ---

// Healthcheck
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', message: 'Fidelio API v1.0 running' });
});

// Autenticación de Negocios (Login)
app.post('/api/auth/login', async (req, res) => {
    const { email, password } = req.body;
    
    if (!supabase) return res.status(500).json({ error: 'Supabase no configurado' });

    try {
        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });

        if (error) throw error;
        res.json({ success: true, session: data.session, user: data.user });
    } catch (error) {
        res.status(401).json({ error: error.message });
    }
});

// Registro de Negocios
app.post('/api/auth/register', async (req, res) => {
    const { businessName, email, password, phone } = req.body;
    
    if (!supabase) return res.status(500).json({ error: 'Supabase no configurado' });

    try {
        // 1. Crear usuario en Auth
        const { data: authData, error: authError } = await supabase.auth.signUp({
            email,
            password,
        });

        if (authError) throw authError;

        // 2. Insertar perfil en merchants
        if (authData.user) {
            const { error: dbError } = await supabase
                .from('merchants')
                .insert([
                    { id: authData.user.id, business_name: businessName }
                ]);
            
            if (dbError) console.error("Error al crear merchant:", dbError);
        }

        res.json({ success: true, user: authData.user });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// Creación de Cajeros (Staff)
app.post('/api/auth/staff/create', apiLimiter, requireMerchantAuth, async (req, res) => {
    const { email, password, name } = req.body;
    
    if (req.userRole !== 'admin') {
        return res.status(403).json({ error: 'Solo el dueño puede crear cajeros.' });
    }
    if (!supabaseAdmin) {
        return res.status(500).json({ error: 'Supabase Admin no configurado (Falta SERVICE_ROLE_KEY).' });
    }

    try {
        // 1. Crear el usuario con la API Admin para no cerrar la sesión del dueño
        const { data: staffAuth, error: authError } = await supabaseAdmin.auth.admin.createUser({
            email: email,
            password: password,
            email_confirm: true,
            user_metadata: {
                role: 'staff',
                merchant_id: req.merchantId,
                name: name
            }
        });

        if (authError) throw authError;

        // 2. Registrar al cajero en la tabla 'staff' para que el dueño lo vea en la lista
        const { error: dbError } = await supabaseAdmin
            .from('staff')
            .insert([{ 
                id: staffAuth.user.id, 
                merchant_id: req.merchantId, 
                email: email,
                name: name
            }]);
            
        if (dbError) throw dbError;

        res.json({ success: true, user: staffAuth.user });
    } catch (error) {
        console.error("Staff Create Error:", error);
        res.status(400).json({ error: error.message });
    }
});

// Checkout con Stripe
app.post('/api/stripe/checkout', async (req, res) => {
    const { merchantId, email } = req.body;
    
    if (!stripe) return res.status(500).json({ error: 'Stripe no configurado' });

    try {
        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card'],
            customer_email: email,
            client_reference_id: merchantId,
            line_items: [
                {
                    price_data: {
                        currency: 'mxn',
                        product_data: {
                            name: 'Suscripción Enterprise Fidelio',
                            description: 'Acceso a la plataforma B2B para pases en Apple & Google Wallet'
                        },
                        unit_amount: 99900,
                        recurring: { interval: 'month' },
                    },
                    quantity: 1,
                },
            ],
            mode: 'subscription',
            success_url: `http://localhost:8080/panel?payment=success`,
            cancel_url: `http://localhost:8080/`,
        });

        res.json({ success: true, url: session.url });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Generar Pase de Apple Wallet (.pkpass)
app.post('/api/wallet/apple', apiLimiter, requireMerchantAuth, async (req, res) => {
    const { customerId } = req.body;
    if (!customerId) return res.status(400).json({ error: 'Falta customerId' });

    try {
        const { PKPass } = require('passkit-generator');
        
        // Credenciales de Apple desde variables de entorno
        const wwdr = process.env.APPLE_WWDR_CERT; // El certificado WWDR G4 en base64
        const signerCert = process.env.APPLE_SIGNER_CERT; // El certificado pass (.pem) en base64
        const signerKey = process.env.APPLE_SIGNER_KEY; // La llave privada (.pem) en base64
        const signerKeyPassphrase = process.env.APPLE_SIGNER_KEY_PASSPHRASE; // Contraseña de la llave privada
        const teamIdentifier = process.env.APPLE_TEAM_ID;
        const passTypeIdentifier = process.env.APPLE_PASS_TYPE_ID;

        if (!wwdr || !signerCert || !signerKey || !teamIdentifier || !passTypeIdentifier) {
            return res.status(500).json({ error: 'Faltan certificados de Apple en las variables de entorno.' });
        }

        // 1. Fetch Merchant Data
        const { data: merchant, error: mErr } = await supabase.from('merchants').select('*').eq('id', req.merchantId).single();
        if (mErr || !merchant) throw new Error("Merchant no encontrado");
        
        // 2. Fetch Customer Data
        const { data: customer, error: cErr } = await supabase.from('customers').select('*').eq('id', customerId).single();
        if (cErr || !customer) throw new Error("Cliente no encontrado");
        
        // 3. Fetch Branches for Geofencing
        const { data: branches } = await supabase.from('branches').select('lat, lng, name').eq('merchant_id', req.merchantId);

        // Crear la estructura de la tarjeta
        const pass = new PKPass({
            "pass.json": {
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: customer.id,
                teamIdentifier: teamIdentifier,
                organizationName: merchant.business_name || "Mi Negocio",
                description: "Tarjeta de Lealtad",
                logoText: merchant.business_name || "Mi Negocio",
                backgroundColor: merchant.color_primary || "#090d16",
                foregroundColor: "#ffffff",
                labelColor: merchant.color_accent || "#8b5cf6",
                storeCard: {
                    primaryFields: [
                        { key: "balance", label: "SALDO", value: `$${customer.current_balance}` }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" }
                    ],
                    backFields: [
                        { key: "portal", label: "PORTAL WEB", value: `https://fidelio.com/portal.html?id=${customer.id}` }
                    ]
                },
                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: customer.id
                }
            }
        });

        // Geofencing (si hay sucursales)
        if (branches && branches.length > 0) {
            const locations = branches.map(b => ({
                latitude: b.lat,
                longitude: b.lng,
                relevantText: `¡Bienvenido a ${b.name}! Tienes $${customer.current_balance} para usar hoy.`
            }));
            pass.add('locations', locations);
        }

        // Cargar Certificados (decodificados de base64)
        pass.certificates({
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        });

        // Generar archivo binario (.pkpass)
        const buffer = await pass.getAsBuffer();
        
        // Responder con el archivo binario directo al navegador
        res.set({
            'Content-Type': 'application/vnd.apple.pkpass',
            'Content-Disposition': `attachment; filename="${merchant.business_name || 'tarjeta'}.pkpass"`
        });
        res.send(buffer);

        console.log(`[UNICORN ENGINE] 🍏 Tarjeta Apple Wallet generada y firmada para ${customer.name}`);

    } catch (err) {
        console.error("Error Apple Wallet:", err);
        res.status(500).json({ success: false, error: err.message });
    }
});

// Utilidad para firmar JWT sin dependencias (RS256)
const crypto = require('crypto');
function signJwtRS256(payload, privateKey) {
    const header = { alg: "RS256", typ: "JWT" };
    const toBase64Url = (obj) => Buffer.from(JSON.stringify(obj)).toString('base64url');
    const data = `${toBase64Url(header)}.${toBase64Url(payload)}`;
    const signature = crypto.createSign('RSA-SHA256').update(data).sign(privateKey, 'base64url');
    return `${data}.${signature}`;
}

// Generar Tarjeta de Google Wallet (JWT)
app.post('/api/wallet/google', apiLimiter, requireMerchantAuth, async (req, res) => {
    const { customerId } = req.body;
    if (!customerId) return res.status(400).json({ error: 'Falta customerId' });

    try {
        const issuerId = process.env.GOOGLE_WALLET_ISSUER_ID;
        const clientEmail = process.env.GOOGLE_CLIENT_EMAIL;
        let privateKey = process.env.GOOGLE_PRIVATE_KEY;

        if (!issuerId || !clientEmail || !privateKey) {
            return res.status(500).json({ error: 'Credenciales de Google Wallet no configuradas en el servidor.' });
        }
        
        // Render parsea los \n como texto plano, hay que convertirlos a saltos reales
        privateKey = privateKey.replace(/\\n/g, '\n');

        const { data: merchant } = await supabase.from('merchants').select('*').eq('id', req.merchantId).single();
        const { data: customer } = await supabase.from('customers').select('*').eq('id', customerId).single();
        
        if (!merchant || !customer) throw new Error("Datos incompletos");

        // Objecto de Lealtad (Tarjeta)
        const jwtPayload = {
            iss: clientEmail,
            aud: "google",
            typ: "savetowallet",
            iat: Math.floor(Date.now() / 1000),
            origins: [],
            payload: {
                loyaltyObjects: [{
                    id: `${issuerId}.${customer.id}`,
                    classId: `${issuerId}.${req.merchantId}`, // Asume que la clase (plantilla) ya se creó en la consola
                    accountId: customer.id,
                    accountName: customer.name,
                    state: "ACTIVE",
                    barcode: { type: "QR_CODE", value: customer.id },
                    loyaltyPoints: {
                        balance: { string: `$${customer.current_balance}` },
                        label: "Saldo"
                    }
                }]
            }
        };

        const token = signJwtRS256(jwtPayload, privateKey);
        const saveUrl = `https://pay.google.com/gp/v/save/${token}`;

        console.log(`[UNICORN ENGINE] 🚀 Link de Google Wallet generado para ${customer.name}`);

        res.json({
            success: true,
            saveUrl: saveUrl
        });

    } catch (err) {
        console.error("Error Google Wallet:", err);
        res.status(500).json({ success: false, error: err.message });
    }
});

// Rutas principales
app.get('/api/config', (req, res) => {
    res.json({
        supabaseUrl: process.env.SUPABASE_URL,
        supabaseAnonKey: process.env.SUPABASE_ANON_KEY
    });
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'landing.html'));
});

app.get('/panel', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 Fidelio Backend Server active on http://localhost:${PORT}`);
});
