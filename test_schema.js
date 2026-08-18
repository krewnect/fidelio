require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: cols } = await supabase.rpc('get_table_schema', { table_name: 'campaigns' });
    console.log(cols);
}
check();
