require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function check() {
    const { data: campaigns, error } = await supabase
        .from('campaigns')
        .select('*')
        .eq('merchant_id', '65dd91a2-7210-43ea-8bef-da72d375df80')
        .order('created_at', { ascending: false });
    
    console.log("Returned Campaigns:", campaigns.length);
    console.log("Filtered length:", campaigns.filter(c => !['membership', 'multipass', 'certificates'].includes(c.type)).length);
}
check();
