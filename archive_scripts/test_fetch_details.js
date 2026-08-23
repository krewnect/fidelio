require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function check() {
    const { data: merchants } = await supabase.from('merchants').select('id').limit(1);
    if (merchants && merchants.length > 0) {
        const { data, error } = await supabase.from('campaigns').select('id, name, type, created_at').eq('merchant_id', merchants[0].id).order('created_at', { ascending: false });
        console.log("CAMPAIGNS:");
        console.log(data);
    }
}
check();
