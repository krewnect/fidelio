const { createClient } = require('@supabase/supabase-js');
const supabaseUrl = 'https://sjkgpyalbqqsfndekgtb.supabase.co';
const serviceRoleKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqa2dweWFsYnFxc2ZuZGVrZ3RiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NjAzNDMyMywiZXhwIjoyMTAxNjEwMzIzfQ.qNAxx3XiVAIppbpN8YEqqP4VlqZapk2rko3pk_Lq0hk';
const supabase = createClient(supabaseUrl, serviceRoleKey);

async function run() {
  const { data: users } = await supabase.auth.admin.listUsers();
  const admin = users.users.find(u => u.email === 'hola@fideliorewards.com');
  if (!admin) return console.log("Admin not found");

  const { data: existing } = await supabase.from('merchants').select('id').eq('id', admin.id).single();
  if (existing) {
    console.log("Master merchant already exists!");
    return;
  }

  const { data, error } = await supabase.from('merchants').insert({
    id: admin.id,
    business_name: 'Fidelio Oficial',
    points_ratio: 10,
    cashback_percentage: 5,
    plan_type: 'founder'
  });
  if (error) console.error("Error creating merchant:", error);
  else console.log("Master merchant created successfully!");
}
run();
