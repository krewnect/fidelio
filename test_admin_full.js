require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

async function check() {
    const payload = {
        id: generateUUID(),
        merchant_id: '13a3adbb-0f3e-4807-8b65-a43d98a9601c',
        type: "stamps",
        name: "Nueva Campaña",
        description: "",
        color_primary: "#000000",
        color_accent: "#8b5cf6",
        logo_url: null,
        banner_url: null,
        stamp_icon_url: "fa-star",
        custom_cta_label: "Premio Gratis",
        rules_config: {
            cashback_percent: 10,
            stamps_total: 5,
            vip_tiers: { bronce: {}, plata: {}, oro: {} },
            show_appointment_btn: false,
            show_payment_btn: false
        }
    };

    const { data, error } = await supabase.from('campaigns').upsert([payload]).select().single();
    console.log("UPSERT ERROR:", error);
    console.log("DATA:", data ? data.id : null);
}
check();
