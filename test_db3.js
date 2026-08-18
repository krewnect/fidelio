const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
async function run() {
    const { data: merch } = await supabase.from('merchants').select('id, appointment_settings').ilike('business_name', '%demo professional%').single();
    console.log(JSON.stringify(merch.appointment_settings, null, 2));
}
run();
