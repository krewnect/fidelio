require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function run() {
    const { data: merchants } = await supabase.from('merchants').select('id, business_type').order('created_at', { ascending: false }).limit(1);
    if(merchants && merchants.length > 0) {
        const merchantId = merchants[0].id;
        const { data, error } = await supabase.from('merchants').update({ business_type: 'business', plan_status: 'active_lifetime', subscription_plan: 'founder' }).eq('id', merchantId);
        console.log("Updated to business:", error || "Success");
    }
}
run();
