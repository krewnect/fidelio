const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');

async function check() {
    try {
        const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
        const supabase = createClient(config.supabaseUrl, config.supabaseAnonKey);
        const { data, error } = await supabase.storage.listBuckets();
        console.log("Buckets:", data);
        if (error) console.error("Error:", error);
    } catch(e) {
        console.error("Exception:", e);
    }
}
check();
