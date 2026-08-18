require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: campaigns } = await supabase.from('campaigns').select('*').eq('merchant_id', '6ebd41a1-d0e3-4547-8ffd-930b07623c76');
    console.log("DEMO CAMPAIGNS:", campaigns);
}
check();
