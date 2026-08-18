require('dotenv').config();
const express = require('express');
const { generateHybridStrip } = require('./render_hybrid_strip.js');
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


const requireBusinessPlan = async (req, res, next) => {
    try {
        const { data: merchant, error } = await supabase
            .from('merchants')
            .select('business_type')
            .eq('id', req.merchantId)
            .single();
            
        if (error || !merchant) return res.status(404).json({ success: false, error: 'Merchant not found' });
        
        // Admin overrides
        if (req.userRole === 'admin' && req.merchantId === 'hola@fideliorewards.com') return next(); 
        
        const plan = merchant.business_type || 'starter';
        if (plan === 'business' || plan === 'enterprise') {
            next();
        } else {
            return res.status(403).json({ success: false, error: 'Upgrade to Business to access this feature.' });
        }
    } catch (e) {
        return res.status(500).json({ success: false, error: 'Internal validation error' });
    }
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
    

    amount = parseFloat(amount);
    if (!customerId || isNaN(amount) || amount <= 0 || !['earn', 'redeem'].includes(type)) {
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
    maxAge: '1d',
    dotfiles: 'allow',
    index: false,
    setHeaders: (res, path) => {
        if (path.endsWith('.html') || path.endsWith('.js')) {
            res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
            res.setHeader('Pragma', 'no-cache');
            res.setHeader('Expires', '0');
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
app.post('/api/portal/:username/register', async (req, res) => {
    try {
        const { username } = req.params;
        const { fullName, email, phone, birthday } = req.body;
        
        // Find merchant
        const { data: merchant, error: mError } = await supabase
            .from('merchants')
            .select('id')
            .filter('appointment_settings->landing_prefs->>username', 'eq', username)
            .limit(1)
            .single();
            
        if (mError || !merchant) return res.status(404).json({ error: 'Negocio no encontrado' });
        
        // Insert customer
        const insertData = {
            merchant_id: merchant.id,
            full_name: fullName,
            email: email
        };
        if (phone) insertData.phone = phone;
        if (birthday) insertData.birthday = birthday;
        
        const { error: insertError } = await supabase.from('customers').insert([insertData]);
        
        if (insertError) {
            // If already exists, we might want to just update or ignore
            if (insertError.code === '23505') {
                return res.json({ success: true, message: 'El cliente ya estaba registrado.' });
            }
            throw insertError;
        }
        
        res.json({ success: true });
    } catch (ex) {
        res.status(500).json({ error: ex.message });
    }
});

app.get('/api/portal/:username', async (req, res) => {
    try {
        const { username } = req.params;
        const { data, error } = await supabase
            .from('merchants')
            .select('id, business_name, appointment_settings')
            .filter('appointment_settings->landing_prefs->>username', 'eq', username)
            .limit(1)
            .single();
            
        if (error || !data) {
            return res.status(404).json({ error: 'Portal no encontrado' });
        }
        res.json({
            business_name: data.business_name,
            landing_prefs: data.appointment_settings?.landing_prefs || {}
        });
    } catch (ex) {
        res.status(500).json({ error: ex.message });
    }
});

app.post('/api/auth/register', async (req, res) => {
    let { businessType, businessName, email, password, phone, promoCode, username } = req.body;
    username = username || businessName.toLowerCase().replace(/[^a-z0-9]/g, '');

    
    if (!supabase) return res.status(500).json({ error: 'Supabase no configurado' });

    try {
        let planStatus = 'trial';
        let skipStripe = false;
        
        // 0. Validar Promo Code
        if (promoCode) {
            const { data: promo, error: promoError } = await supabase
                .from('promo_codes')
                .select('*')
                .eq('code', promoCode)
                .eq('is_active', true)
                .single();
                
            if (promo && !promoError) {
                if (promo.used_count < promo.max_uses) {
                    // Marcar uso
                    await supabase.from('promo_codes').update({ used_count: promo.used_count + 1 }).eq('code', promoCode);
                    
                    
                    if (promo.target_plan) {
                        businessType = promo.target_plan;
                    }
                    if (promo.reward_type === 'lifetime_free' || (promo.reward_type === 'discount' && promo.discount_pct >= 100)) {
                        planStatus = 'active_lifetime';
                        skipStripe = true; // El cliente ya no necesita pagar
                    }
                }
            }
        }

        // 1. Crear usuario en Auth
        let authData, authError;
        if (supabaseAdmin) {
            const res = await supabaseAdmin.auth.admin.createUser({
                email,
                password,
                email_confirm: true
            });
            authData = res.data;
            authError = res.error;
        } else {
            const res = await supabase.auth.signUp({
                email,
                password,
            });
            authData = res.data;
            authError = res.error;
        }

        if (authError) throw authError;
        
        if (!authData || !authData.user) {
            throw new Error("El correo electrónico ya está registrado o hubo un problema con el registro.");
        }

        // 2. Insertar perfil en merchants
        const { error: dbError } = await supabase
            .from('merchants')
            .insert([
                { id: authData.user.id, business_name: businessName, plan_status: planStatus, business_type: businessType || 'restaurant' }
            ]);
        
        if (dbError) console.error("Error al crear merchant:", dbError);

        res.json({ success: true, user: authData.user, skipStripe });
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
    const { merchantId, email, businessType, plan, interval } = req.body;
    
    if (!stripe) return res.status(500).json({ error: 'Stripe no configurado' });

    try {
        // Diccionario de precios dinámicos (en centavos de MXN)
        let amount = 99900; // default (Restaurante Founder Mensual)
        let productName = 'Suscripción Fidelio';
        
        if (businessType === 'professional') {
            if (plan === 'founder') {
                amount = (interval === 'year') ? 199900 : 19900;
                productName = 'Licencia Founder (Fidelio Professionals)';
            } else {
                amount = (interval === 'year') ? 399900 : 39900;
                productName = 'Licencia Estándar (Fidelio Professionals)';
            }
        } else {
            // Business (Antes Restaurantes)
            if (plan === 'founder') {
                amount = (interval === 'year') ? 999900 : 99900;
                productName = 'Licencia Founder (Fidelio Negocios)';
            } else {
                amount = (interval === 'year') ? 1999900 : 199900;
                productName = 'Licencia Estándar (Fidelio Negocios)';
            }
        }

        const session = await stripe.checkout.sessions.create({
            payment_method_types: ['card'],
            customer_email: email,
            client_reference_id: merchantId,
            line_items: [
                {
                    price_data: {
                        currency: 'mxn',
                        product_data: {
                            name: productName,
                            description: 'Acceso a la plataforma B2B para pases en Apple & Google Wallet'
                        },
                        unit_amount: amount,
                        recurring: { interval: interval || 'month' },
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

// Generar Pase de Apple Wallet para Clientes (Descarga Directa)
app.get('/api/wallet/apple/:customerId/:campaignId', apiLimiter, async (req, res) => {
    const { customerId, campaignId } = req.params;
    if (!customerId || !campaignId) return res.status(400).send('Falta customerId o campaignId');

    try {
        const { PKPass } = require('passkit-generator');
        
        // Credenciales de Apple
        const wwdr = process.env.APPLE_WWDR_CERT; 
        const signerCert = process.env.APPLE_SIGNER_CERT; 
        const signerKey = process.env.APPLE_SIGNER_KEY; 
        const signerKeyPassphrase = process.env.APPLE_SIGNER_KEY_PASSPHRASE; 
        const teamIdentifier = process.env.APPLE_TEAM_ID;
        const passTypeIdentifier = process.env.APPLE_PASS_TYPE_ID;

        if (!wwdr || !signerCert || !signerKey || !teamIdentifier || !passTypeIdentifier) {
            return res.status(500).send('Apple Wallet no configurado en el servidor.');
        }

        // Fetch Customer
        const { data: customer, error: cErr } = await supabase.from('customers').select('*').eq('id', customerId).single();
        if (cErr || !customer) return res.status(404).send('Cliente no encontrado');

        // Fetch Campaign
        const { data: campaign, error: campErr } = await supabase.from('campaigns').select('*').eq('id', campaignId).single();
        if (campErr || !campaign) return res.status(404).send('Campaña no encontrada');

        // Fetch Customer_Campaign status
        const { data: cStatus } = await supabase.from('customer_campaigns').select('*').eq('customer_id', customerId).eq('campaign_id', campaignId).single();
        const stamps = cStatus ? cStatus.stamps_count : 0;
        const cashback = cStatus ? cStatus.balance_cashback : 0;
        
        const balanceVal = campaign.type === 'stamps' ? `${stamps} / ${campaign.rules_config.stamps_total || 5}` : `$${cashback}`;
        const labelVal = campaign.type === 'stamps' ? 'SELLOS' : 'CASHBACK';

        // Fetch Branches for Geofencing
        const { data: branches } = await supabase.from('branches').select('lat, lng, name').eq('merchant_id', campaign.merchant_id);

        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };
        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: `${customerId}|${campaignId}|v4_${Date.now()}`,
                teamIdentifier: teamIdentifier,
                webServiceURL: "https://fideliorewards.com/api/wallet",
                authenticationToken: customerId.replace(/-/g, '').substring(0, 16),
                organizationName: campaign.name || "Mi Negocio",
                description: campaign.description || "Tarjeta de Lealtad",
                logoText: campaign.name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(0, 0, 0)",
                labelColor: "rgb(100, 100, 100)",
                coupon: {
                    headerFields: [
                        { key: "status", label: "ESTADO", value: "ACTIVO" }
                    ],
                    primaryFields: [],
                    secondaryFields: [
                        { key: "name", label: "SU TARJETA VIRTUAL", value: customer.full_name || "Invitado" },
                        { key: "progress", label: campaign.type === 'stamps' ? "SELLOS" : "CASHBACK", value: balanceVal }
                    ],
                    auxiliaryFields: [],
                    backFields: (() => {
                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: "Abrir mi tarjeta web", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}">Haz clic aquí para abrir</a>` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {
                            arr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: "Agendar ahora", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=appointment">Haz clic aquí para agendar</a>` });
                        }
                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: "Realizar pago", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=payment">Haz clic aquí para pagar</a>` });
                        }
                        arr.push({ key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." });
                        arr.push({ key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" });
                        return arr;
                    })()
                },
                barcodes: [{
                    format: "PKBarcodeFormatQR",
                    message: `${customerId}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Mostrar para escanear"
                }]
            }))
        }, certs);

        if (campaign.type === 'stamps') {
            try {
                const totalStamps = campaign.rules_config?.stamps_total || 5;
                const earnedStamps = stamps;
                const cPrimary = campaign.color_primary || '#8b5cf6';
                const stripBuffer = await generateHybridStrip(totalStamps, earnedStamps, cPrimary, campaign.banner_url);
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            } catch (e) {
                console.error("Hybrid strip generation failed", e);
            }
        }
        
        // Geofencing (si hay sucursales)
        /* Omitido por compatibilidad v3, se debe meter directo en pass.json si se requiere */

        // Certificados ya cargados en constructor

        // Generar strip.png usando Puppeteer si es tipo stamps
        if (campaign.type === 'stamps') {
            try {
                const totalStamps = campaign.rules_config?.stamps_total || 5;
                const earnedStamps = stamps;
                const cPrimary = campaign.color_primary || '#8b5cf6';
                const stripBuffer = await generateHybridStrip(totalStamps, earnedStamps, cPrimary, campaign.banner_url);
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            } catch (e) {
                console.error("Hybrid strip generation failed", e);
            }
        }
        
        // Intentar agregar iconos o logos customizados
        try {
            // El módulo passkit-generator requiere al menos un icono
            // Se asume que icon.png y logo.png existen en la raíz o cargarlos desde URL
            // Como fallback, Passkit-generator requiere archivos locales. 
            const fs = require('fs');
            if (fs.existsSync('./icon-192.png')) {
                pass.addBuffer('icon.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('icon@2x.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('logo.png', fs.readFileSync('./icon-192.png'));
            }
            
            // Si el user tiene strip_icon (Base64)
            if (campaign.stamp_icon_url && campaign.stamp_icon_url.startsWith('data:image')) {
                const base64Data = campaign.stamp_icon_url.replace(/^data:image\/\w+;base64,/, "");
                const stripBuffer = Buffer.from(base64Data, 'base64');
                pass.addBuffer('strip.png', stripBuffer);
            } else if (campaign.banner_url && campaign.banner_url.startsWith('data:image')) {
                const base64Data = campaign.banner_url.replace(/^data:image\/\w+;base64,/, "");
                const stripBuffer = Buffer.from(base64Data, 'base64');
                pass.addBuffer('strip.png', stripBuffer);
            }
        } catch(e) {
            console.error("Error agregando imagenes al pase:", e);
        }

        // Generar archivo binario (.pkpass)
        const buffer = await pass.getAsBuffer();
        
        // Responder
        res.set({
            'Content-Type': 'application/vnd.apple.pkpass',
            'Content-Disposition': `attachment; filename="${(campaign.name || 'tarjeta').replace(/[^a-z0-9]/gi, '_')}.pkpass"`
        });
        res.send(buffer);

    } catch (err) {
        console.error("Error Generando GET Apple Wallet:", err);
        res.status(500).send('Error interno generando el pase de Apple Wallet: ' + err.message);
    }
});

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
        // Crear la estructura de la tarjeta
        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };
        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: customerId,
                teamIdentifier: teamIdentifier,
                webServiceURL: "https://fidelio-41j9.onrender.com/api/wallet",
                authenticationToken: customerId.replace(/-/g, '').substring(0, 16), // A token must be at least 16 chars
                serialNumber: `${customer.id}|v4_${Date.now()}`,
                teamIdentifier: teamIdentifier,
                organizationName: merchant.business_name || "Mi Negocio",
                description: "Tarjeta de Lealtad",
                logoText: merchant.business_name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(0, 0, 0)",
                labelColor: "rgb(100, 100, 100)",
                coupon: {
                    primaryFields: [
                        { key: "balance", label: "SALDO", value: `$${customer.current_balance}` }
                    ],
                    secondaryFields: [
                        { key: "name", label: "SU TARJETA VIRTUAL", value: customer.full_name || "Invitado" },
                        { key: "type", label: "TIPO", value: campaign.type === 'stamps' ? 'Sellos' : 'Cashback' }
                    ],
                    backFields: (() => {
                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: "Abrir mi tarjeta web", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}">Haz clic aquí para abrir</a>` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {
                            arr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: "Agendar ahora", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=appointment">Haz clic aquí para agendar</a>` });
                        }
                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: "Realizar pago", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=payment">Haz clic aquí para pagar</a>` });
                        }
                        arr.push({ key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." });
                        arr.push({ key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" });
                        return arr;
                    })()
                },
                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: customer.id
                }
            }))
        }, certs);

        if (campaign.type === 'stamps') {
            try {
                const totalStamps = campaign.rules_config?.stamps_total || 5;
                const earnedStamps = stamps;
                const cPrimary = campaign.color_primary || '#8b5cf6';
                const stripBuffer = await generateHybridStrip(totalStamps, earnedStamps, cPrimary, campaign.banner_url);
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            } catch (e) {
                console.error("Hybrid strip generation failed", e);
            }
        }
        
        // Geofencing (si hay sucursales)
        if (branches && branches.length > 0) {
            /* omitted locations for v3 compat */
        }

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

// ==========================================
// MY BUSINESS & INTEGRACIONES (NUEVO)
// ==========================================

// 1. Guardar Perfil del Negocio (RFC, Nombre, Automatizaciones)
app.post('/api/mybusiness/save', apiLimiter, requireMerchantAuth, async (req, res) => {
    try {
        const { rfc, businessName, address, autoInstagram, autoTiktok, autoMaps } = req.body;
        
        const { error } = await supabase.from('merchants').update({
            rfc: rfc,
            business_name: businessName,
            address: address,
            auto_instagram_visit_trigger: autoInstagram || 0,
            auto_tiktok_visit_trigger: autoTiktok || 0,
            auto_maps_visit_trigger: autoMaps || 0
        }).eq('id', req.merchantId);

        if (error) throw error;
        res.json({ success: true, message: 'Perfil actualizado correctamente.' });
    } catch (err) {
        console.error("Error guardando perfil:", err);
        res.status(500).json({ success: false, error: err.message });
    }
});

// 2. Stripe Checkout (Pago de Suscripción)
app.post('/api/stripe/checkout', apiLimiter, requireMerchantAuth, async (req, res) => {
    try {
        if (!stripe) {
            return res.status(500).json({ success: false, error: 'Stripe no está configurado en el servidor.' });
        }
        
        const { data: merchant } = await supabase.from('merchants').select('stripe_customer_id, business_name, custom_price').eq('id', req.merchantId).single();
        
const { billing_cycle, tier } = req.body;
        
        let priceId = null;
        if (tier === 'founder') {
            priceId = billing_cycle === 'annual' ? process.env.STRIPE_PRICE_FOUNDER_YR : process.env.STRIPE_PRICE_FOUNDER_MO;
        } else {
            priceId = billing_cycle === 'annual' ? process.env.STRIPE_PRICE_STANDARD_YR : process.env.STRIPE_PRICE_STANDARD_MO;
        }

        let sessionParams = {
            mode: 'subscription',
            payment_method_types: ['card'],
            customer: merchant.stripe_customer_id || undefined,
            success_url: `${req.headers.origin}/panel?payment=success`,
            cancel_url: `${req.headers.origin}/panel?payment=cancelled`,
            metadata: { merchant_id: req.merchantId }
        };

        if (merchant.custom_price) {
            // Dynamic custom pricing
            sessionParams.line_items = [{
                price_data: {
                    currency: 'mxn',
                    product_data: { name: 'Licencia Especial Fidelio' },
                    unit_amount: merchant.custom_price * 100,
                    recurring: { interval: 'month' }
                },
                quantity: 1
            }];
        } else {
            // Standard static pricing
            if (!priceId) {
                return res.status(500).json({ success: false, error: 'Falta configurar los STRIPE_PRICE_ en el archivo .env' });
            }
            sessionParams.line_items = [{ price: priceId, quantity: 1 }];
        }

        const session = await stripe.checkout.sessions.create(sessionParams);

        res.json({ success: true, url: session.url });
    } catch (err) {
        console.error("Error creando Checkout Stripe:", err);
        res.status(500).json({ success: false, error: err.message });
    }
});

// 3. Solicitar Factura
app.post('/api/billing/request', apiLimiter, requireMerchantAuth, async (req, res) => {
    try {
        const { rfc } = req.body;
        if (!rfc) return res.status(400).json({ success: false, error: 'RFC requerido' });
        
        // Simulación: Envío a proveedor de facturación (PAC)
        console.log(`[FACTURACIÓN] Solicitud recibida para RFC: ${rfc} del merchant: ${req.merchantId}`);
        
        res.json({ success: true, message: 'Solicitud de factura enviada al proveedor exitosamente.' });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
});

// 4. Google Maps OAuth (Conectar Sucursal)
app.get('/auth/google', (req, res) => {
    const clientId = process.env.GOOGLE_CLIENT_ID;
    if (!clientId) return res.status(500).send('Google Client ID no configurado en el servidor.');
    
    // merchant_id viene en query params desde el JS frontend
    const state = req.query.merchant_id || 'unknown';
    const redirectUri = `${req.protocol}://${req.get('host')}/auth/google/callback`;
    const scope = encodeURIComponent('https://www.googleapis.com/auth/business.manage');
    
    const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=code&scope=${scope}&access_type=offline&prompt=consent&state=${state}`;
    
    res.redirect(googleAuthUrl);
});

// 5. Callback de Google Maps
app.get('/auth/google/callback', async (req, res) => {
    const { code, state, error } = req.query;
    if (error) return res.status(400).send(`Error de Google: ${error}`);
    
    const merchantId = state; 
    
    try {
        console.log(`[GOOGLE OAUTH] Código recibido exitosamente para el merchant: ${merchantId}`);
        console.log(`Código para intercambiar: ${code}`);
        
        // TODO: Intercambiar "code" por Token usando axios.post a oauth2.googleapis.com/token
        // Y guardar en supabase: merchants.google_access_token
        
        res.redirect('/panel?google_connected=true');
    } catch (err) {
        res.status(500).send('Error procesando autenticación de Google');
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
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    
    const host = req.hostname;
    const parts = host.split('.');
    const ignoredSubdomains = ['www', 'app', 'panel', 'api', 'localhost', 'fideliorewards'];
    
    let isSubdomain = false;
    let slug = null;

    if (parts.length >= 2) {
        const sub = parts[0];
        if (!ignoredSubdomains.includes(sub) && sub !== '127') {
            isSubdomain = true;
            slug = sub;
        }
    }

    if (isSubdomain) {
        return res.sendFile(path.join(__dirname, 'merchant-public.html'));
    }

    const targetPath = path.join(__dirname, 'landing.html');
    res.sendFile(targetPath, { dotfiles: 'allow' });
});

app.get('/panel', (req, res) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/privacidad.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'privacidad.html'), { dotfiles: 'allow' });
});

app.get('/pro', (req, res) => {
    res.sendFile(path.join(__dirname, 'professionals.html'), { dotfiles: 'allow' });
});

app.get('/business', (req, res) => {
    res.sendFile(path.join(__dirname, 'business.html'), { dotfiles: 'allow' });
});

// Ruta Dinámica (Catch-all) para páginas de restaurantes (ej. fideliorewards.com/starbucks)
app.get('/:slug', (req, res) => {
    const slug = req.params.slug;
    // Ignorar si es una llamada a la API o un archivo que no existe (ej. favicon.ico)
    if (slug.startsWith('api') || slug.includes('.')) {
        return res.status(404).send('Not found');
    }
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    res.sendFile(path.join(__dirname, 'merchant-public.html'));
});

// --- AI (GEMINI) ENDPOINT ---
const { GoogleGenerativeAI } = require('@google/generative-ai');
const genAI = process.env.GEMINI_API_KEY ? new GoogleGenerativeAI(process.env.GEMINI_API_KEY) : null;

app.post('/api/ai/support', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) {
        return res.status(503).json({ error: 'La IA no está configurada actualmente (GEMINI_API_KEY).' });
    }

    try {
        const { message, merchantContext } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Mensaje requerido.' });
        }

        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        
        const systemPrompt = `
Eres Fidelio AI, el asistente inteligente oficial de soporte técnico para restaurantes que usan la plataforma Fidelio Rewards.
Debes responder de manera profesional, amable y concisa. Estás hablando con un administrador de un restaurante (comerciante).
Conoces todo sobre el sistema de Fidelio:
- Escáner y Terminal PoS: Tienen un diseño premium y la capacidad de lincar/escanear tarjetas de lealtad físicas tipo código de barras para asignar puntos. 
- Logros y Niveles (Gamificación): Puedes orientar sobre cómo los clientes suben de nivel (Bronce, Plata, Oro, VIP) en base a su gasto o puntos, y cómo desbloquear recompensas.
- Referidos: Los usuarios pueden ganar puntos invitando amigos.
- 8 Tipos de Programas: Puntos, Sellos (visitas), Cashback, Tarjeta Regalo, Suscripción, Cupones, Descuentos, y Monedero (The Bank). Tienen flexibilidad total para configurar reglas.
- CRM: Tienen control total sobre la base de datos de sus clientes.
- Sucursales GPS: Pueden añadir ubicaciones para que Apple Wallet notifique a los clientes cuando pasen cerca. Tienen importación masiva vía CSV.
- Apple Wallet y Google Wallet se gestionan automáticamente al activar clientes en el CRM.
- Marketing IA y Campañas Push: Pueden generar campañas de SMS/Push y correos automáticamente con IA hacia los móviles de sus clientes.
- Citas Médicas y Reservas con Stripe: Tienen agendas, y pueden cobrar anticipos mediante enlaces de pago.
- Soporte y Súper Admin: Hay un Inbox interno con un modal dinámico para atender tickets tipo Zendesk.
- Equipo: Pueden dar accesos limitados (Solo Escáner) o Sistema Completo a sus cajeros o administradores.
- Si el usuario reporta un error técnico, bug, cobro doble, o algo que requiera humanos, dile explícitamente: "Por favor, usa el formulario de la derecha (o el botón 'Levantar Ticket') para escalar este problema a nuestros ingenieros."
- Eres experto en resolver dudas operativas sobre cómo usar estas secciones.
- Trata de no hacer listas largas. Sé directo.

Contexto del Negocio actual: \${JSON.stringify(merchantContext || {})}
`;

        const chat = model.startChat({
            history: [
                {
                    role: "user",
                    parts: [{ text: systemPrompt }],
                },
                {
                    role: "model",
                    parts: [{ text: "Entendido. Actuaré como el asistente Fidelio AI y usaré este contexto para ayudar al restaurante." }],
                }
            ],
            generationConfig: {
                maxOutputTokens: 250,
            },
        });

        const result = await chat.sendMessage(message);
        const response = await result.response;
        const text = response.text();

        res.json({ reply: text });
    } catch (error) {
        console.error('Error en Gemini AI:', error);
        res.status(500).json({ error: 'Error procesando tu solicitud con Inteligencia Artificial.' });
    }
});

app.post('/api/ai/copilot', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) {
        return res.status(503).json({ error: 'La IA no está configurada actualmente (GEMINI_API_KEY).' });
    }

    try {
        const { merchantContext } = req.body;
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        
        const systemPrompt = `
Eres el Copiloto de Marketing AI de Fidelio. Tu objetivo es analizar la situación actual del restaurante y proponer exactamente 3 campañas de marketing altamente efectivas.
Estas campañas pueden ser de dos formatos:
1. "push": Notificaciones Push al celular.
2. "card": Tarjetas Especiales (promociones o eventos que el cliente guarda en su Apple/Google Wallet).

Debes devolver ÚNICAMENTE un arreglo JSON válido (sin markdown, sin bloques de código, sin texto antes ni después) con exactamente 3 objetos. 
Cada objeto debe tener esta estructura exacta:
{
  "title": "Título llamativo para la tarjeta (ej. Día de Pizza)",
  "description": "Explicación de por qué esta campaña es buena idea",
  "format": "push o card",
  "pushMessage": "El texto persuasivo de la Notificación Push o Descripción de la Tarjeta (max 120 caracteres)",
  "segment": "uno de estos: [all, active, risk, inactive, vip_oro, vip_plata, cumpleaneros, aniversario]",
  "estimatedReach": "Ej. ~150 Clientes",
  "type": "uno de estos: [recuperacion, cumpleanos, dias_lentos, vip_exclusivo, winback]"
}
Asegúrate de incluir al menos una sugerencia de tipo "card".

Contexto actual del negocio:
${JSON.stringify(merchantContext || {})}
`;

        const result = await model.generateContent(systemPrompt);
        let text = await result.response.text();
        
        // Limpiar el texto de Gemini si responde con ```json
        text = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
        
        let opportunities = [];
        try {
            opportunities = JSON.parse(text);
        } catch (e) {
            console.error("Fallo al parsear JSON de Gemini:", text);
            // Fallback en caso de que Gemini no devuelva JSON válido
            opportunities = [
                {
                    title: "Recuperar Clientes en Riesgo",
                    description: "Tienes varios clientes que no te visitan desde hace más de 30 días. Envíales un incentivo ahora.",
                    format: "push",
                    pushMessage: "¡Te extrañamos! Vuelve esta semana y te regalamos el postre en tu consumo.",
                    segment: "risk",
                    estimatedReach: "~45 Clientes",
                    type: "recuperacion"
                },
                {
                    title: "Pase VIP Exclusivo",
                    description: "Crea una tarjeta especial dorada para tus mejores clientes con beneficios únicos.",
                    format: "card",
                    pushMessage: "Tarjeta de Beneficios Oro. Acceso sin filas y postre de cortesía en cada visita.",
                    segment: "vip_oro",
                    estimatedReach: "~20 Clientes",
                    type: "vip_exclusivo"
                },
                {
                    title: "Premiar a los Cumpleañeros",
                    description: "Fideliza a los que cumplen años este mes con un pequeño detalle.",
                    format: "push",
                    pushMessage: "¡Feliz mes de cumpleaños! Ven a celebrar y nosotros invitamos la ronda de shots.",
                    segment: "cumpleaneros",
                    estimatedReach: "~12 Clientes",
                    type: "cumpleanos"
                }
            ];
        }

        res.json({ opportunities });
    } catch (error) {
        console.error('Error en Copiloto AI:', error);
        res.status(500).json({ error: 'Error analizando datos con Inteligencia Artificial.' });
    }
});


// --- MULTI-CARD (CAMPAIGNS) API ---
app.get('/api/campaigns', requireMerchantAuth, async (req, res) => {
    try {
        const { merchantId } = req;
        if (!merchantId) return res.status(401).json({ error: 'No merchantId' });
        
        const { data: campaigns, error } = await supabase
            .from('campaigns')
            .select('*')
            .eq('merchant_id', merchantId)
            .order('created_at', { ascending: false });
            
        if (error) throw error;
        res.json({ campaigns });
    } catch (ex) {
        console.error('Error fetching campaigns:', ex);
        res.status(500).json({ error: ex.message });
    }
});

// --- SPECIAL CARDS EMISSIONS API ---
app.get('/api/special-emissions', requireMerchantAuth, async (req, res) => {
    try {
        const { merchantId } = req;
        if (!merchantId) return res.status(401).json({ error: 'No merchantId' });

        const { data, error } = await supabase
            .from('special_card_emissions')
            .select('*')
            .eq('merchant_id', merchantId)
            .order('created_at', { ascending: false });
        
        if (error) throw error;
        res.json(data || []);
    } catch (err) {
        console.error("Error GET /special-emissions:", err);
        res.status(500).json({ error: 'Error del servidor' });
    }
});

app.post('/api/special-emissions', requireMerchantAuth, async (req, res) => {
    try {
        const { merchantId } = req;
        if (!merchantId) return res.status(401).json({ error: 'No merchantId' });

        const { client_name, client_phone, client_email, card_type, card_name, expiry_date } = req.body;
        
        const { data, error } = await supabase
            .from('special_card_emissions')
            .insert([{
                merchant_id: merchantId,
                client_name,
                client_phone,
                client_email,
                card_type,
                card_name,
                expiry_date,
                status: 'active'
            }])
            .select()
            .single();

        if (error) throw error;
        res.json(data);
    } catch (err) {
        console.error("Error POST /special-emissions:", err);
        res.status(500).json({ error: 'Error al registrar la emisión' });
    }
});

app.delete('/api/campaigns/:id', requireMerchantAuth, async (req, res) => {
    try {
        const { merchantId } = req;
        const campaignId = req.params.id;
        if (!merchantId) return res.status(401).json({ error: 'No merchantId' });

        const { error } = await supabase
            .from('campaigns')
            .delete()
            .match({ id: campaignId, merchant_id: merchantId });
            
        if (error) throw error;
        res.json({ success: true });
    } catch (ex) {
        console.error('Error deleting campaign:', ex);
        res.status(500).json({ error: ex.message });
    }
});

app.post('/api/campaigns', requireMerchantAuth, async (req, res) => {
    try {
        const { merchantId } = req;
        const payload = req.body;
        payload.merchant_id = merchantId;
        
        // Coerce types to avoid violating campaigns_type_check constraint
        const allowedTypes = ['cashback', 'stamps', 'membership', 'multipass'];
        if (!allowedTypes.includes(payload.type)) {
            if (payload.type === 'certificates') payload.type = 'multipass';
            else payload.type = 'cashback'; // maps hybrid, discount, coupons, custom
        }

        // Si no se manda rules_config, poner defaults para no romper
        if (!payload.rules_config) {
            payload.rules_config = {
                stamps_total: 5,
                cashback_percent: 10,
                stamps_reward_text: 'Premio Gratis'
            };
        }

        // Upsert (Insert or Update based on ID)
        const { data, error } = await supabase
            .from('campaigns')
            .upsert([payload])
            .select()
            .single();
            
        if (error) {
            console.error('SUPABASE UPSERT ERROR:', error, 'PAYLOAD:', payload);
            throw error;
        }
        res.json({ success: true, campaign: data });
    } catch (ex) {
        console.error('Error saving campaign:', ex);
        res.status(500).json({ error: ex.message });
    }
});

app.post('/api/stripe/keys', async (req, res) => {
    try {
        const { merchantId } = req;
        const { stripe_pub_key, stripe_secret_key } = req.body;
        const { error } = await supabase
            .from('merchants')
            .update({ stripe_pub_key, stripe_secret_key })
            .eq('id', merchantId);
        if (error) throw error;
        res.json({ success: true });
    } catch (ex) {
        res.status(500).json({ error: ex.message });
    }
});

// --- FIN MULTI-CARD API ---


// ------------------------------------------------------------
// API: Solicitar Cita
// ------------------------------------------------------------
app.post('/api/appointments', apiLimiter, async (req, res) => {
    const { customerId, campaignId, date, time, notes } = req.body;
    if (!customerId || !campaignId || !date || !time) {
        return res.status(400).json({ success: false, error: "Faltan datos obligatorios" });
    }

    try {
        // Obtenemos el merchant_id de la campaña
        const { data: campaign, error: campErr } = await supabase
            .from('campaigns')
            .select('merchant_id')
            .eq('id', campaignId)
            .single();

        if (campErr || !campaign) {
            return res.status(404).json({ success: false, error: "Campaña no encontrada" });
        }

        // Guardamos la cita en transactions para no requerir tabla nueva de inmediato
        const payload = { date, time, notes };
        
        const { error } = await supabase.from('transactions').insert([{
            merchant_id: campaign.merchant_id,
            customer_id: customerId,
            transaction_type: 'appointment_request',
            notes: JSON.stringify(payload)
        }]);

        if (error) throw error;

        res.json({ success: true });
    } catch (err) {
        console.error("Error al agendar cita:", err);
        res.status(500).json({ success: false, error: err.message });
    }
});


app.listen(PORT, () => {
    console.log(`🚀 Fidelio Backend Server active on http://localhost:${PORT}`);
});


// ============================================================================
// APPLE WALLET WEB SERVICE PROTOCOL & APNs
// ============================================================================

const apn = require('@parse/node-apn');

let apnProvider = null;
if (process.env.APPLE_SIGNER_CERT && process.env.APPLE_SIGNER_KEY) {
    try {
        apnProvider = new apn.Provider({
            cert: Buffer.from(process.env.APPLE_SIGNER_CERT, 'base64'),
            key: Buffer.from(process.env.APPLE_SIGNER_KEY, 'base64'),
            passphrase: process.env.APPLE_SIGNER_KEY_PASSPHRASE || '',
            production: true // Change to false if using development sandbox
        });
        console.log("🍏 APNs Provider Inicializado.");
    } catch(e) {
        console.error("Error inicializando APNs:", e);
    }
}

// Middleware to check Apple Auth Token
const checkAppleAuth = (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('ApplePass ')) {
        return res.status(401).send();
    }
    req.appleAuthToken = authHeader.replace('ApplePass ', '');
    next();
};

// 1. Register a Device
app.post('/api/wallet/v1/devices/:deviceLibraryIdentifier/registrations/:passTypeIdentifier/:serialNumber', checkAppleAuth, async (req, res) => {
    const { deviceLibraryIdentifier, passTypeIdentifier, serialNumber } = req.params;
    const { pushToken } = req.body;
    
    if (!pushToken) return res.status(400).send();
    
    try {
        // Find merchant from customer
        const { data: customer } = await supabase.from('customers').select('merchant_id').eq('id', serialNumber).single();
        if(!customer) return res.status(404).send();
        
        const { error } = await supabase.from('pass_registrations').upsert({
            device_library_identifier: deviceLibraryIdentifier,
            push_token: pushToken,
            serial_number: serialNumber,
            pass_type_identifier: passTypeIdentifier,
            merchant_id: customer.merchant_id,
            updated_at: new Date().toISOString()
        }, { onConflict: 'device_library_identifier, serial_number' });
        
        if (error) throw error;
        
        res.status(201).send(); // Or 200 if already exists
    } catch (err) {
        console.error("Error in Apple Wallet Registration:", err);
        res.status(500).send();
    }
});

// 2. Unregister a Device
app.delete('/api/wallet/v1/devices/:deviceLibraryIdentifier/registrations/:passTypeIdentifier/:serialNumber', checkAppleAuth, async (req, res) => {
    const { deviceLibraryIdentifier, passTypeIdentifier, serialNumber } = req.params;
    try {
        await supabase.from('pass_registrations').delete()
            .match({ device_library_identifier: deviceLibraryIdentifier, serial_number: serialNumber });
        res.status(200).send();
    } catch (err) {
        res.status(500).send();
    }
});

// 3. Get Serial Numbers for Updated Passes
// This gets hit when the device receives an empty APNs push
app.get('/api/wallet/v1/devices/:deviceLibraryIdentifier/registrations/:passTypeIdentifier', async (req, res) => {
    const { deviceLibraryIdentifier, passTypeIdentifier } = req.params;
    const passesUpdatedSince = req.query.passesUpdatedSince;
    
    try {
        // En una implementación real, compararíamos `passesUpdatedSince` con la fecha de la última actualización de la tarjeta (ej. un sello nuevo o campaña push).
        // Por simplicidad, devolveremos todos los pases que tenga el dispositivo y dejamos que Apple decida actualizarlos.
        const { data, error } = await supabase.from('pass_registrations')
            .select('serial_number, updated_at')
            .eq('device_library_identifier', deviceLibraryIdentifier)
            .eq('pass_type_identifier', passTypeIdentifier);
            
        if (error || !data || data.length === 0) return res.status(204).send(); // 204 No Content
        
        let serialNumbers = data.map(d => d.serial_number);
        // We can just return the latest updated_at as the new tag
        let lastUpdated = data[0].updated_at;
        
        res.json({
            serialNumbers: serialNumbers,
            lastUpdated: new Date().getTime().toString()
        });
    } catch (err) {
        console.error(err);
        res.status(500).send();
    }
});

// 4. Download Updated Pass
app.get('/api/wallet/v1/passes/:passTypeIdentifier/:serialNumber', checkAppleAuth, async (req, res) => {
    const { passTypeIdentifier, serialNumber } = req.params;
    
    try {
        const { PKPass } = require('passkit-generator');
        
        const wwdr = process.env.APPLE_WWDR_CERT;
        const signerCert = process.env.APPLE_SIGNER_CERT;
        const signerKey = process.env.APPLE_SIGNER_KEY;
        const signerKeyPassphrase = process.env.APPLE_SIGNER_KEY_PASSPHRASE;
        const teamIdentifier = process.env.APPLE_TEAM_ID;
        
        const { data: customer } = await supabase.from('customers').select('*').eq('id', serialNumber).single();
        if (!customer) return res.status(404).send();
        
        const { data: merchant } = await supabase.from('merchants').select('*').eq('id', customer.merchant_id).single();
        if (!merchant) return res.status(404).send();
        
        // Find latest active push campaign for this merchant to inject into pass
        const { data: latestPush } = await supabase.from('push_campaigns')
            .select('*').eq('merchant_id', merchant.id).order('created_at', { ascending: false }).limit(1);

        let pushTitle = '';
        let pushBody = '';
        if (latestPush && latestPush.length > 0) {
            pushTitle = latestPush[0].title;
            pushBody = latestPush[0].body;
        }

        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };
        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,
                serialNumber: serialNumber,
                teamIdentifier: teamIdentifier,
                webServiceURL: "https://fidelio-41j9.onrender.com/api/wallet",
                authenticationToken: serialNumber.replace(/-/g, '').substring(0, 16),
                organizationName: merchant.business_name || "Mi Negocio",
                description: `Pase de Lealtad de ${merchant.business_name}`,
                logoText: merchant.business_name,
                foregroundColor: "rgb(255, 255, 255)",
                backgroundColor: "rgb(255, 255, 255)",
                labelColor: "rgb(139, 92, 246)",
                coupon: {
                    headerFields: [
                        { key: "stamps", label: "SELLOS", value: `${customer.stamps_count} / ${merchant.stamps_required}` }
                    ],
                    primaryFields: [
                        { key: "reward", label: "RECOMPENSA", value: "Activa" }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || 'Invitado' }
                    ],
                    auxiliaryFields: [
                        { key: "member", label: "NIVEL", value: "VIP" }
                    ],
                    backFields: [
                        { key: "promo", label: pushTitle || "Promociones", value: pushBody || "¡Visítanos pronto y acumula más sellos!", changeMessage: "%@" }
                    ]
                },
                barcodes: [{
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: "Mostrar para escanear"
                }]
            }))
        }, certs);

        // Try to fetch custom logo if any, otherwise use default
        try {
            const fs = require('fs');
            const logoPath = require('path').join(__dirname, 'fidelio_logo_white.png');
            if(fs.existsSync(logoPath)) pass.addBuffer('logo.png', fs.readFileSync(logoPath));
        } catch(e) {}
        
        const passBuffer = await pass.getAsBuffer();
        res.setHeader('Content-Type', 'application/vnd.apple.pkpass');
        res.setHeader('Content-Disposition', `attachment; filename=${merchant.business_name.replace(/\s+/g, '_')}.pkpass`);
        res.send(passBuffer);
        
    } catch (err) {
        console.error("Error generating updated pass:", err);
        res.status(500).send();
    }
});

// 5. Log Errors from Apple
app.post('/api/wallet/v1/log', (req, res) => {
    console.error("Apple Wallet Error Logs:", req.body.logs);
    res.status(200).send();
});

// ============================================================================
// TRIGGER MARKETING PUSH API
// ============================================================================
app.post('/api/push/send', apiLimiter, requireMerchantAuth, async (req, res) => {
    const { title, body } = req.body;
    if (!title || !body) return res.status(400).json({ error: 'Faltan título o cuerpo de la campaña' });
    
    try {
        // 1. Guardar campaña en DB
        const { error: insertErr } = await supabase.from('push_campaigns').insert([{
            merchant_id: req.merchantId,
            title,
            body,
            status: 'sent'
        }]);
        if (insertErr) throw insertErr;
        
        // 2. Traer tokens de APNs de los clientes de este comercio
        const { data: registrations } = await supabase.from('pass_registrations').select('push_token').eq('merchant_id', req.merchantId);
        
        if (!registrations || registrations.length === 0) {
            return res.json({ success: true, message: "Campaña guardada, pero no hay iPhones registrados para Push." });
        }
        
        const tokens = registrations.map(r => r.push_token);
        
        // 3. Mandar APNs ping (Notificación vacía que activa el Pass Web Service)
        if (apnProvider) {
            let note = new apn.Notification();
            // Para tarjetas Wallet, no enviamos mensaje, enviamos un payload vacío y un apns-push-type "background" o omitido.
            // Para actualizar el pass, enviamos el payload vacío (según docs de Apple).
            let result = await apnProvider.send(note, tokens);
            console.log(`[APNs] Push Enviado. Exitosos: ${result.sent.length}, Fallidos: ${result.failed.length}`);
        } else {
            console.warn("APNs provider no está configurado. La campaña se guardó pero no se mandó ping a Apple.");
        }
        
        res.json({ success: true, message: `Campaña enviada a ${tokens.length} dispositivos.` });
    } catch (err) {
        console.error("Error enviando push:", err);
        res.status(500).json({ error: err.message });
    }
});


