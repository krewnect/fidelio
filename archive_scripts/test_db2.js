require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function check() {
    const { data } = await supabase.from('merchants').select('*').limit(1);
    console.log("COLUMNS:", Object.keys(data[0]));
}
check();
