require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: merchant } = await supabase.from('merchants').select('business_type').eq('id', '13a3adbb-0f3e-4807-8b65-a43d98a9601c').single();
    console.log("HOLA PLAN:", merchant);
}
check();
