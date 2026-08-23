require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

async function check() {
    const payload = {
        id: generateUUID(),
        merchant_id: '13a3adbb-0f3e-4807-8b65-a43d98a9601c', // hola@fideliorewards.com
        type: 'stamps'
    };

    const { data, error } = await supabase.from('campaigns').upsert([payload]).select().single();
    console.log("UPSERT ERROR:", error);
    console.log("DATA:", data);
}
check();
