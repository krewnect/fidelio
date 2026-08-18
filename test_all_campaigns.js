require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: campaigns } = await supabase.from('campaigns').select('id, merchant_id, name, created_at').order('created_at', { ascending: false }).limit(10);
    console.log("ALL DB CAMPAIGNS:");
    console.log(campaigns);
}
check();
