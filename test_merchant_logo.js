const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
async function run() {
    const { data: merch } = await supabase.from('merchants').select('id, business_name, logo_url, banner_url, color_primary').ilike('business_name', '%demo professional%').single();
    console.log(JSON.stringify(merch, null, 2));
}
run();
