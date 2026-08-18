require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data, error } = await supabase.from('merchants').select('appointment_settings').limit(1);
    console.log(typeof data[0].appointment_settings, data[0].appointment_settings);
}
check();
