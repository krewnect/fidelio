const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
async function run() {
    const { data: merch } = await supabase.from('merchants').select('id').ilike('business_name', '%demo professional%').single();
    const { data: camps } = await supabase.from('campaigns').select('id, created_at, logo_url, banner_url, color_primary').eq('merchant_id', merch.id).order('created_at', { ascending: false });
    console.log(`Total camps: ${camps.length}`);
    console.log(JSON.stringify(camps.slice(0, 3), null, 2));
}
run();
