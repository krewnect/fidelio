require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function test() {
    let slug = 'demoprofessional';
    const { data, error } = await supabase
        .from('merchants')
        .select('*')
        .filter('appointment_settings->landing_prefs->>username', 'eq', slug)
        .limit(1)
        .single();
    console.log("Error:", error);
    console.log("Data:", data ? data.id : null);
}
test();
