import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = "app.post(['/api/appointments', '/api/appointments/request'], apiLimiter, async (req, res) => {"
replacement = """const appointmentHandler = async (req, res) => {
    const customerId = req.body.customerId || req.body.customer_id;
    const campaignId = req.body.campaignId || req.body.campaign_id;
    const { date, time, notes } = req.body;
    
    if (!customerId || !campaignId || !date || !time) {
        return res.status(400).json({ success: false, error: "Faltan datos obligatorios" });
    }

    try {
        const { data: campaign, error: campErr } = await supabase
            .from('campaigns')
            .select('merchant_id')
            .eq('id', campaignId)
            .single();

        if (campErr || !campaign) {
            return res.status(404).json({ success: false, error: "Campaña no encontrada" });
        }

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
};
app.post('/api/appointments', apiLimiter, appointmentHandler);
app.post('/api/appointments/request', apiLimiter, appointmentHandler);
"""

# I need to match the whole old function and replace it.
# Let's just find the function block
old_func_pattern = r"app\.post\(\['/api/appointments', '/api/appointments/request'\], apiLimiter, async \(req, res\) => \{.*?\n\}\);\n"
js = re.sub(old_func_pattern, replacement, js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
