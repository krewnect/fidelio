require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);
async function run() {
    const { data } = await supabase.from('promo_codes').select('*').eq('code', 'BUSINESSDEMO');
    console.log(data);
}
run();
