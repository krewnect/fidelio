require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: users, error } = await supabase.auth.admin.listUsers();
    const user = users.users.find(u => u.id === '65dd91a2-7210-43ea-8bef-da72d375df80');
    console.log("USER:", user ? user.email : "Not found");
}
check();
