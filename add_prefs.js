require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function addCol() {
    const { error } = await supabase.rpc('execute_sql', { sql: 'ALTER TABLE merchants ADD COLUMN IF NOT EXISTS preferences JSONB DEFAULT \'{}\'::jsonb;' });
    if (error) {
        console.log("No RPC execute_sql, try direct rest/rpc? Or via PostgREST?");
    }
}
addCol();
