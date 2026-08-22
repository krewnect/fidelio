require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error("Missing Supabase credentials in .env");
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function run() {
    const { data, error } = await supabase
        .from('promo_codes')
        .update({ is_active: false, max_uses: 0 })
        .eq('code', 'DEMOP01');
        
    if (error) {
        console.error("Error updating promo code:", error);
    } else {
        console.log("Successfully killed DEMOP01 promo code.", data);
    }
}

run();
