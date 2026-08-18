require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function check() {
    const { data: merchants } = await supabase.from('merchants').select('id, business_name, business_type, plan_status, slug').order('created_at', { ascending: false }).limit(5);
    console.log("RECENT MERCHANTS:");
    console.table(merchants);

    const { data: promos } = await supabase.from('promo_codes').select('*').limit(10);
    console.log("
PROMO CODES:");
    console.table(promos);
}

check();
