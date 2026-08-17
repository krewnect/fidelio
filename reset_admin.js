const { createClient } = require('@supabase/supabase-js');
const supabaseUrl = 'https://sjkgpyalbqqsfndekgtb.supabase.co';
const serviceRoleKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqa2dweWFsYnFxc2ZuZGVrZ3RiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NjAzNDMyMywiZXhwIjoyMTAxNjEwMzIzfQ.qNAxx3XiVAIppbpN8YEqqP4VlqZapk2rko3pk_Lq0hk';

const supabase = createClient(supabaseUrl, serviceRoleKey);

async function run() {
  const { data, error } = await supabase.auth.admin.listUsers();
  if (error) return console.error(error);
  const adminUser = data.users.find(u => u.email === 'hola@fideliorewards.com');
  if (adminUser) {
    const { data: updated, error: updateError } = await supabase.auth.admin.updateUserById(adminUser.id, {
      password: 'Admin123456!'
    });
    if (updateError) {
      console.error("Error resetting:", updateError);
    } else {
      console.log("Password reset successfully to Admin123456!");
    }
  } else {
    console.log("User not found");
  }
}
run();
