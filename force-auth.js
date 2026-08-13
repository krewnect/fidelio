require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function setup() {
    // 1. Create a demo merchant if it doesn't exist
    const { data: merchants } = await supabase.from('merchants').select('*');
    let merchantId;
    if (!merchants || merchants.length === 0) {
        console.log("Creating dummy merchant...");
        const { data: newM, error: e1 } = await supabase.from('merchants').insert([{
            business_name: 'Restaurante Demo'
        }]).select();
        if (e1) { console.log("Error creating merchant", e1); return; }
        merchantId = newM[0].id;
    } else {
        merchantId = merchants[0].id;
    }

    // 2. Create the cashier user
    console.log("Using Merchant ID:", merchantId);
    
    // First, let's just make sure demo@fidelio.com works as a fallback by updating its password
    const { data: users } = await supabase.auth.admin.listUsers();
    let demoUser = users.users.find(u => u.email === 'demo@fidelio.com');
    if (demoUser) {
        await supabase.auth.admin.updateUserById(demoUser.id, { password: 'demo12345', user_metadata: { merchant_id: merchantId } });
        console.log("Updated demo@fidelio.com to demo12345");
    }

    // Now create mesero@fidelio.com
    const { data: mesero, error: e2 } = await supabase.auth.admin.createUser({
        email: 'mesero@fidelio.com',
        password: 'mesero12345',
        email_confirm: true,
        user_metadata: { role: 'staff', merchant_id: merchantId }
    });

    if (e2 && e2.message.includes('already registered')) {
        let meseroUser = users.users.find(u => u.email === 'mesero@fidelio.com');
        if (meseroUser) {
            await supabase.auth.admin.updateUserById(meseroUser.id, { password: 'mesero12345', user_metadata: { role: 'staff', merchant_id: merchantId } });
            console.log("Updated mesero@fidelio.com to mesero12345");
        }
    } else if (e2) {
        console.log("Error creating mesero:", e2);
    } else {
        console.log("Created mesero@fidelio.com / mesero12345");
    }
}
setup();
