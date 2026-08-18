const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
async function test() {
    const { data: merch } = await supabase.from('merchants').select('id, business_name').ilike('business_name', '%demo professional%').single();
    const { data: camps } = await supabase.from('campaigns').select('id, type').eq('merchant_id', merch.id);
    console.log(camps.map(c => c.type));
}
test();
