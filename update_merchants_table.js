require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function run() {
  console.log("Fetching auth users...");
  const { data: usersData, error: authErr } = await supabase.auth.admin.listUsers();
  if (authErr) {
    console.error("Auth error:", authErr);
    return;
  }
  
  const users = usersData.users || [];
  console.log(`Found ${users.length} users. Migrating data to merchants...`);
  
  // Try to update one merchant to see if columns exist
  if (users.length > 0) {
      const u = users[0];
      const { error: testErr } = await supabase.from('merchants').update({
          owner_email: u.email
      }).eq('id', u.id);
      
      if (testErr && testErr.code === '42703') {
          console.error("Columns do not exist! We cannot write to them without altering the table.");
          return;
      }
  }
  
  console.log("Updating merchants...");
  let count = 0;
  for (const u of users) {
      const name = (u.user_metadata?.first_name || '') + ' ' + (u.user_metadata?.last_name || '');
      const { error } = await supabase.from('merchants').update({
          owner_email: u.email,
          owner_name: name.trim(),
          owner_phone: u.phone
      }).eq('id', u.id);
      if (!error) count++;
  }
  console.log(`Successfully updated ${count} merchants.`);
}
run();
