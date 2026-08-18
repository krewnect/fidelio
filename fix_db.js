const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
async function test() {
    const { data: merch } = await supabase.from('merchants').select('id, appointment_settings').ilike('business_name', '%demo professional%').single();
    
    // Set portal_color to yellow!
    const settings = merch.appointment_settings || {};
    settings.landing_prefs = settings.landing_prefs || {};
    settings.landing_prefs.portal_color = '#eab308'; // Tailwind Yellow 500
    
    await supabase.from('merchants').update({ appointment_settings: settings }).eq('id', merch.id);
    
    // Also set all their 13 campaigns to yellow just to be safe
    await supabase.from('campaigns').update({ color_primary: '#eab308' }).eq('merchant_id', merch.id);
}
test();
