import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

target = """app.get('/api/wallet/data', async (req, res) => {
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
});"""

replacement = """app.get('/api/wallet/data', async (req, res) => {
    const { c, camp } = req.query;
    if (!c || !camp) return res.status(400).json({ success: false, error: "Parámetros faltantes" });

    try {
        let customer = null;
        let merchant = null;
        
        // Fetch Campaign
        const { data: campaign, error: campErr } = await supabase
            .from('campaigns')
            .select('*')
            .eq('id', camp)
            .single();
            
        if (campErr || !campaign) return res.status(404).json({ success: false, error: "Campaña no encontrada" });

        if (c === 'DEMO') {
            customer = {
                id: 'DEMO',
                full_name: 'Invitado Demo',
                name: 'Invitado',
                vip_tier: 'DEMO',
                balance_cashback: 0,
                stamps_count: 3,
                visits: 1,
                merchant_id: campaign.merchant_id
            };
        } else {
            const { data: realCust, error: cErr } = await supabase
                .from('customers')
                .select('*')
                .eq('id', c)
                .single();
                
            if (cErr || !realCust) return res.status(404).json({ success: false, error: "Cliente no encontrado" });
            customer = realCust;
        }

        const { data: realMerchant } = await supabase
            .from('merchants')
            .select('business_name, business_type')
            .eq('id', customer.merchant_id)
            .single();
            
        merchant = realMerchant || { business_name: 'Mi Negocio' };

        res.json({
            success: true,
            customer,
            campaign,
            merchant
        });
    } catch (e) {
        res.status(500).json({ success: false, error: e.message });
    }
});"""

app_js = app_js.replace(target, replacement)
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
