require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function check() {
    const { data: cols } = await supabase.rpc('get_table_schema', { table_name: 'campaigns' });
    console.log(cols);
    
    // We can also query pg_constraint
    // But since we can't easily query raw SQL, let's just test which ones work
    const typesToTest = ["cashback", "stamps", "discount", "coupons", "custom", "membership", "multipass", "certificates", "hybrid"];
    for(let t of typesToTest) {
        const { error } = await supabase.from('campaigns').insert([{ id: '00000000-0000-0000-0000-00000000001'+typesToTest.indexOf(t), merchant_id: '13a3adbb-0f3e-4807-8b65-a43d98a9601c', name: 'Test', type: t }]);
        if(error) console.log(t, "FAILS:", error.message);
        else console.log(t, "WORKS");
    }
}
check();
