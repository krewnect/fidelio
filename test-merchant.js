require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
async function run() {
    const { data: users } = await supabase.auth.admin.listUsers();
    const admin = users.users.find(u => u.email === 'admin@fidelio.com');
    if (!admin) return console.log("Admin not found");
    const { data: merchant } = await supabase.from('merchants').select('*').eq('id', admin.id).single();
    console.log(merchant);
}
run();
