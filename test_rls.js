const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

async function test() {
    const configRes = await fetch('http://localhost:3000/api/config');
    const config = await configRes.json();
    const supabase = createClient(config.supabaseUrl, config.supabaseAnonKey);
    const { data, error } = await supabase.from('merchants').select('*').limit(1).single();
    console.log("Anon Error:", error);
    console.log("Anon Data:", data ? data.id : null);
}
test();
