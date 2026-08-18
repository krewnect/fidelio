const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

async function test() {
    const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
    const { data, error } = await supabase.from('merchants').select('*').limit(1).single();
    console.log("Anon Error:", error);
    console.log("Anon Data:", data ? data.id : null);
}
test();
