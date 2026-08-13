require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: merchants, error: mError } = await supabase.from('merchants').select('*');
    console.log("Merchants:", merchants, mError);
    
    const { data: users, error: uError } = await supabase.auth.admin.listUsers();
    console.log("Users:");
    if (users && users.users) {
        users.users.forEach(u => console.log(u.email));
    }
}
check();
