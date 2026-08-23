require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function fix() {
    const { data: merchants, error } = await supabase.from('merchants').select('id, business_name, appointment_settings');
    if (error) {
        console.error("Error fetching merchants:", error);
        return;
    }
    
    for (const m of merchants) {
        let slug = (m.business_name || '').toLowerCase().replace(/[^a-z0-9]/g, '');
        if (!slug) slug = 'user' + Math.floor(Math.random() * 1000);
        
        let settings = m.appointment_settings || {};
        if (!settings.landing_prefs) settings.landing_prefs = {};
        settings.landing_prefs.username = slug;
        
        await supabase.from('merchants').update({ appointment_settings: settings }).eq('id', m.id);
        console.log(`Updated ${m.business_name} -> ${slug}`);
    }
    console.log("Done updating existing merchants.");
}
fix();
