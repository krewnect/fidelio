const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
async function run() {
    const { data: merch } = await supabase.from('merchants').select('id').ilike('business_name', '%demo professional%').single();
    await supabase.from('campaigns').update({ type: 'stamps' }).eq('merchant_id', merch.id);
    console.log("Updated all campaigns to stamps!");
}
run();
