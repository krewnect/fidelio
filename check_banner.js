const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

async function check() {
    const { data } = await supabase.from('campaigns').select('banner_url, name').eq('id', '0b72b4a0-5681-482a-95d8-f8664497af99').single();
    console.log(data);
}
check();
