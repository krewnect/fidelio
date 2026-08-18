require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function check() {
    const { data: campaigns, error } = await supabase.from('campaigns').select('*').order('created_at', { ascending: false }).limit(2);
    console.log("LAST 2 CAMPAIGNS:");
    console.log(JSON.stringify(campaigns, null, 2));
}
check();
