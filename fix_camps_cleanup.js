const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);

async function run() {
    const { data: merch } = await supabase.from('merchants').select('id').ilike('business_name', '%demo professional%').single();
    const { data: camps } = await supabase.from('campaigns').select('id, created_at').eq('merchant_id', merch.id).order('created_at', { ascending: false });
    
    if (camps.length > 1) {
        const toDelete = camps.slice(1).map(c => c.id);
        const { error } = await supabase.from('campaigns').delete().in('id', toDelete);
        if (error) console.error("Error deleting:", error);
        else console.log(`Deleted ${toDelete.length} old campaigns.`);
    }
}
run();
