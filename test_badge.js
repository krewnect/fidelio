const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const env = fs.readFileSync('.env', 'utf-8');
const supabaseUrl = env.match(/SUPABASE_URL=(.*)/)[1].trim();
const supabaseKey = env.match(/SUPABASE_SERVICE_ROLE_KEY=(.*)/)[1].trim();
const supabase = createClient(supabaseUrl, supabaseKey);

async function test() {
    // Simulate what dashboard.js does
    const { data: transactions } = await supabase.from('transactions').select('*').eq('merchant_id', '6ebd41a1-d0e3-4547-8ffd-930b07623c76');
    const { data: merchantData } = await supabase.from('merchants').select('appointment_settings').eq('id', '6ebd41a1-d0e3-4547-8ffd-930b07623c76').single();
    
    let processed = merchantData.appointment_settings.processed_appointments || [];
    const pendingCitas = transactions.filter(t => t.transaction_type === 'appointment_request' && !processed.includes(t.id)).length;
    
    console.log("Pending citas for DEMO user:", pendingCitas);
}
test();
