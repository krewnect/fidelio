require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function run() {
    const { data, error } = await supabase
        .from('merchants')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(1);
    if(error) console.error("DB Error:", error);
    console.log(JSON.stringify(data, null, 2));
}
run();
