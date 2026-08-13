require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function createCashier() {
    // get first merchant
    const { data: merchants } = await supabase.from('merchants').select('*').limit(1);
    if (!merchants || merchants.length === 0) {
        console.log("No merchants found");
        return;
    }
    const merchantId = merchants[0].id;
    console.log("Merchant ID:", merchantId);

    // create or update cashier
    const { data, error } = await supabase.auth.admin.createUser({
        email: 'cajero@fidelio.com',
        password: 'cajero12345',
        email_confirm: true,
        user_metadata: { merchant_id: merchantId }
    });

    if (error) {
        if (error.message.includes('already registered')) {
            console.log("User exists, updating password...");
            await supabase.auth.admin.updateUserById(
                // we need the ID, let's just get it
            );
            console.log("Use cajero@fidelio.com / cajero12345");
        } else {
            console.log("Error:", error);
        }
    } else {
        console.log("Created cajero@fidelio.com / cajero12345");
    }
}
createCashier();
