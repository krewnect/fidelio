require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data, error } = await supabase.from('customers').select('*').limit(1);
    if (error) console.log("NO CUSTOMERS TABLE", error);
    else console.log("CUSTOMERS TABLE:", data[0] ? Object.keys(data[0]) : "Empty, but exists");
}
check();
