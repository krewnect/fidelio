require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function check() {
    const payload = {
        id: 'camp_12345',
        merchant_id: 'b1234567-1234-1234-1234-123456789012', // I don't have the real merchantId, let me query one
        type: 'stamps',
        name: 'Test Campaign',
        color_primary: '#000000',
        color_accent: '#ffffff',
        rules_config: {}
    };

    const { data: merchants } = await supabase.from('merchants').select('id').limit(1);
    if (merchants && merchants.length > 0) {
        payload.merchant_id = merchants[0].id;
        console.log("Using merchant_id:", payload.merchant_id);
        const { data, error } = await supabase.from('campaigns').upsert([payload]).select().single();
        console.log("UPSERT RESULT:", error ? error : data);
    } else {
        console.log("No merchants found");
    }
}
check();
