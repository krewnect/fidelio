const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const env = fs.readFileSync('.env', 'utf-8');
const supabaseUrl = env.match(/SUPABASE_URL=(.*)/)[1].trim();
const supabaseKey = env.match(/SUPABASE_ANON_KEY=(.*)/)[1].trim();
const supabase = createClient(supabaseUrl, supabaseKey);

async function test() {
    // 1. Authenticate as the DEMO user
    const { data: authData, error: authErr } = await supabase.auth.signInWithPassword({
        email: 'demoprofessional@fideliorewards.com',
        password: 'password' // We don't know the password!
    });
    console.log(authErr);
}
test();
