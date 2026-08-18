require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: merchant } = await supabase.from('merchants').select('*').eq('id', '65dd91a2-7210-43ea-8bef-da72d375df80').single();
    console.log("MERCHANT:", merchant);
}
check();
