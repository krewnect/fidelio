require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    let payload = {
        id: '12345678-1234-1234-1234-123456789012',
        merchant_id: '13a3adbb-0f3e-4807-8b65-a43d98a9601c',
        type: 'stamps', // because they are professional
        name: 'Nueva Campaña',
        description: "",
        color_primary: "#000000",
        color_accent: "#8b5cf6",
        logo_url: null,
        banner_url: null,
        stamp_icon_url: "fa-burger",
        custom_cta_label: "Premio",
        rules_config: {
            cashback_percent: 10,
            stamps_total: 5,
            vip_tiers: { bronce: {}, plata: {}, oro: {} },
            show_appointment_btn: false,
            show_payment_btn: false
        }
    };
    
    // Coerce types to avoid violating campaigns_type_check constraint
    const allowedTypes = ['cashback', 'stamps', 'membership', 'multipass'];
    if (!allowedTypes.includes(payload.type)) {
        if (payload.type === 'certificates') payload.type = 'multipass';
        else payload.type = 'cashback'; // maps hybrid, discount, coupons, custom
    }

    const { data, error } = await supabase
        .from('campaigns')
        .upsert([payload])
        .select()
        .single();
        
    console.log("UPSERT RESULT:", error, data);
}
check();
