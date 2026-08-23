import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

appointments_routes = """
// ==========================================
// APPOINTMENTS (Citas Médicas / Servicios)
// ==========================================

// Cliente solicita una cita
app.post('/api/appointments/request', apiLimiter, async (req, res) => {
    const { customer_id, campaign_id, date, time, notes } = req.body;
    
    if (!customer_id || !campaign_id || !date || !time) {
        return res.status(400).json({ error: 'Faltan datos obligatorios' });
    }

    try {
        // 1. Obtener la campaña para saber de qué merchant es
        const { data: campaign, error: cErr } = await supabase.from('campaigns').select('merchant_id').eq('id', campaign_id).single();
        if (cErr || !campaign) throw new Error("Campaña no encontrada");

        // 2. Obtener el cliente
        const { data: customer, error: custErr } = await supabase.from('customers').select('name, email, phone').eq('id', customer_id).single();
        if (custErr || !customer) throw new Error("Cliente no encontrado");

        // 3. Formatear la fecha
        const appointment_date = new Date(`${date}T${time}:00`).toISOString();

        // 4. Insertar la cita
        const { data: appointment, error: appErr } = await supabase.from('appointments').insert([{
            merchant_id: campaign.merchant_id,
            customer_id: customer_id,
            customer_name: customer.name || 'Cliente sin nombre',
            customer_phone: customer.phone,
            customer_email: customer.email,
            appointment_date: appointment_date,
            status: 'pending',
            notes: notes || ''
        }]).select().single();

        if (appErr) throw appErr;

        res.json({ success: true, appointment });
    } catch (err) {
        console.error("Error creando cita:", err);
        res.status(500).json({ error: err.message });
    }
});

// Profesional actualiza estado de la cita (Aceptar o Cancelar)
app.post('/api/appointments/:id/status', apiLimiter, requireMerchantAuth, async (req, res) => {
    const { id } = req.params;
    const { status } = req.body; // 'confirmed', 'cancelled', 'completed'
    
    try {
        const { data, error } = await supabase.from('appointments')
            .update({ status: status, updated_at: new Date().toISOString() })
            .eq('id', id)
            .eq('merchant_id', req.merchantId)
            .select().single();
            
        if (error) throw error;
        res.json({ success: true, data });
    } catch (err) {
        console.error("Error actualizando cita:", err);
        res.status(500).json({ error: err.message });
    }
});

// Profesional solicita pago por Stripe para la cita
app.post('/api/appointments/:id/request-payment', apiLimiter, requireMerchantAuth, async (req, res) => {
    const { id } = req.params;
    
    try {
        // Obtenemos el payment_link de la campaña actual (o del merchant)
        // Por simplicidad, tomaremos el stripe_payment_link del merchant
        const { data: merchant, error: mErr } = await supabase.from('merchants').select('stripe_payment_link').eq('id', req.merchantId).single();
        
        if (mErr || !merchant || !merchant.stripe_payment_link) {
            throw new Error("No tienes un enlace de pago configurado en la pestaña Stripe.");
        }

        const { data, error } = await supabase.from('appointments')
            .update({ status: 'payment_requested', notes: `PAGO REQUERIDO: ${merchant.stripe_payment_link}`, updated_at: new Date().toISOString() })
            .eq('id', id)
            .eq('merchant_id', req.merchantId)
            .select().single();
            
        if (error) throw error;
        res.json({ success: true, payment_link: merchant.stripe_payment_link, data });
    } catch (err) {
        console.error("Error solicitando pago de cita:", err);
        res.status(500).json({ error: err.message });
    }
});
"""

if "/api/appointments" not in js:
    # Insert before module.exports or at the end
    js = js.replace('const PORT = process.env.PORT || 3000;', appointments_routes + '\n\nconst PORT = process.env.PORT || 3000;')
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Appointments routes added to app.js")
else:
    print("Routes already exist")
