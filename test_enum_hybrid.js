require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { error } = await supabase.from('campaigns').insert([{ id: '00000000-0000-0000-0000-000000000001', merchant_id: '13a3adbb-0f3e-4807-8b65-a43d98a9601c', name: 'Test', type: 'hybrid' }]);
    console.log("INSERT HYBRID TYPE ERROR:", error);
}
check();
