require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: users, error } = await supabase.auth.admin.listUsers();
    console.log("USERS:");
    console.log(users.users.map(u => ({ id: u.id, email: u.email })));
}
check();
