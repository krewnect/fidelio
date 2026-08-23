require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: campaigns } = await supabase.from('campaigns').select('*').eq('merchant_id', 'befdfa2f-f455-475d-a17d-d5e63c043552');
    console.log("ADMIN CAMPAIGNS:", campaigns.length);
}
check();
