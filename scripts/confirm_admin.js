require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error("Missing Supabase SERVICE_ROLE_KEY credentials in .env");
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function confirmAdmin() {
  const userId = '13a3adbb-0f3e-4807-8b65-a43d98a9601c';

  console.log(`Confirming email for user: ${userId}`);

  // Auto-confirm email using admin API
  const { data, error } = await supabase.auth.admin.updateUserById(
    userId,
    { email_confirm: true }
  );

  if (error) {
    console.error("Error confirming user:", error);
  } else {
    console.log("Admin user email confirmed successfully!");
  }
}

confirmAdmin();
