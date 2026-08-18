require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function create() {
    const { data, error } = await supabase.storage.createBucket('logos', { public: true });
    if (error) console.error(error);
    else console.log('Bucket created:', data);
}
create();
