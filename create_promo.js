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
        .insert([{ 
            code: 'BUSINESSDEMO',
            discount_pct: 100,
            reward_type: 'lifetime_free',
            target_plan: 'business',
            max_uses: 100,
            used_count: 0,
            is_active: true
        }]);
        
    if (error) {
        console.error("Error creating promo code:", error);
    } else {
        console.log("Successfully created BUSINESSDEMO promo code.");
    }
}

run();
