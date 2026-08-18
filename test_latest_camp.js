const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
async function run() {
    const { data: merch } = await supabase.from('merchants').select('id').ilike('business_name', '%demo professional%').single();
    const { data: camps } = await supabase.from('campaigns').select('*').eq('merchant_id', merch.id).order('created_at', { ascending: false }).limit(2);
    console.log(JSON.stringify(camps, null, 2));
}
run();
