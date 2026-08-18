require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
async function run() {
    const { data, error } = await supabase.from('promo_codes').update({ used_count: 0, max_uses: 100 }).eq('code', 'DEMOP01');
    console.log("Data:", data);
    console.log("Error:", error);
}
run();
