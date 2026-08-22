import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

api_code = """
// ------------------------------------------------------------
// API: Get Wallet Data (Public for pass.html)
// ------------------------------------------------------------
app.get('/api/wallet/data', async (req, res) => {
    const { c, camp } = req.query;
    if (!c || !camp) return res.status(400).json({ success: false, error: "Parámetros faltantes" });

    try {
        const { data: customer, error: cErr } = await supabase
            .from('customers')
            .select('*')
            .eq('id', c)
            .single();
            
        if (cErr || !customer) return res.status(404).json({ success: false, error: "Cliente no encontrado" });

        const { data: campaign, error: campErr } = await supabase
            .from('campaigns')
            .select('*')
            .eq('id', camp)
            .single();
            
        if (campErr || !campaign) return res.status(404).json({ success: false, error: "Campaña no encontrada" });

        const { data: merchant, error: mErr } = await supabase
            .from('merchants')
            .select('business_name, business_type')
            .eq('id', customer.merchant_id)
            .single();

        res.json({
            success: true,
            customer,
            campaign,
            merchant
        });
    } catch (e) {
        res.status(500).json({ success: false, error: e.message });
    }
});
"""

if "/api/wallet/data" not in app_js:
    if "app.listen(" in app_js:
        app_js = app_js.replace("app.listen(", api_code + "\napp.listen(")
    else:
        app_js += "\n" + api_code

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
