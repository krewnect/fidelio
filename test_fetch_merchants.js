require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY);

async function check() {
    const { data: merchants, error } = await supabase.from('merchants').select('*');
    if (error) console.log(error);
    console.log("MERCHANTS:");
    console.log(merchants.map(m => ({ id: m.id, email: m.email })));
}
check();
