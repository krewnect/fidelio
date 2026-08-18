const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    let slug = 'demoprofessional';
    const { data, error } = await supabase
        .from('merchants')
        .select('*')
        .filter('appointment_settings->landing_prefs->>username', 'eq', slug)
        .limit(1)
        .single();
    console.log(error, data ? data.id : null);
}
check();
