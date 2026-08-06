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
let supabase;

if (supabaseUrl && supabaseKey) {
    supabase = createClient(supabaseUrl, supabaseKey);
    console.log('✅ Conectado a Supabase');
} else {
    console.log('⚠️ Supabase no configurado aún (Faltan variables en .env)');
}

// --- AUTH MIDDLEWARE ---
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
    req.merchantId = user.id;
    next();
};

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

        res.json({ 
            success: true, 
            newBalance, 
            pointsEarned: earned, 
            amountRedeemed: redeemed 
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

// Middleware de Seguridad Básica
app.use(helmet({
    contentSecurityPolicy: false // Desactivado temporalmente para permitir scripts CDN como Supabase
}));

const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutos
    max: 100, // Límite de 100 peticiones por IP cada 15 min
    message: { error: 'Demasiadas peticiones, por favor intenta más tarde.' }
});

app.use('/api/', apiLimiter);

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Servir archivos estáticos (Frontend)
app.use(express.static(path.join(__dirname, '/'), { index: false }));

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

// Generar Pase de Wallet (Endpoint de prueba)
app.post('/api/wallet/generate', (req, res) => {
    const { customerName, customerEmail, passType } = req.body;
    // TODO: Implementar lógica con passkit-generator para Apple y API para Google
    res.json({ 
        success: true, 
        message: 'Pase en proceso de generación', 
        data: { customerName, passType } 
    });
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
