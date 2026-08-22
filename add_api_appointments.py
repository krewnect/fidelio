import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

api_code = """
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

"""

if "/api/appointments" not in app_js:
    # Insert before the catch-all route at the bottom if possible, or just before module.exports
    if "app.listen(" in app_js:
        app_js = app_js.replace("app.listen(", api_code + "\napp.listen(")
    else:
        app_js += "\n" + api_code

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
