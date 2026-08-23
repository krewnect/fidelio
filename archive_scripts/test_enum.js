require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: cols } = await supabase.rpc('get_table_schema', { table_name: 'campaigns' });
    console.log(cols);
    
    // If rpc fails, try to just insert a garbage type and see the error
    const { error } = await supabase.from('campaigns').insert([{ id: '00000000-0000-0000-0000-000000000000', merchant_id: '13a3adbb-0f3e-4807-8b65-a43d98a9601c', name: 'Test', type: 'garbage_type' }]);
    console.log("INSERT GARBAGE TYPE ERROR:", error);
}
check();
