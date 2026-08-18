require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function check() {
    const { data: campaigns, error } = await supabase.from('campaigns').select('id, name, type, created_at').order('created_at', { ascending: false }).limit(5);
    console.log("RECENT CAMPAIGNS ACROSS ALL MERCHANTS:");
    console.log(campaigns);
}
check();
