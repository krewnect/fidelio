require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: campaigns, error } = await supabase
        .from('campaigns')
        .select('id, name, created_at')
        .eq('merchant_id', '13a3adbb-0f3e-4807-8b65-a43d98a9601c')
        .order('created_at', { ascending: false });
    console.log("HOLA CAMPAIGNS:", campaigns);
}
check();
