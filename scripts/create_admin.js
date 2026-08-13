require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error("Missing Supabase credentials in .env");
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function createAdmin() {
  const email = 'hola@fideliorewards.com';
  const password = 'FidelioAdmin2026!';

  console.log(`Creating admin user: ${email}`);

  // Create user
  const { data, error } = await supabase.auth.signUp({
    email: email,
    password: password,
  });

  if (error) {
    if (error.message.includes('User already registered') || error.message.includes('already exists')) {
        console.log("User already exists!");
    } else {
        console.error("Error creating user:", error);
    }
  } else {
    console.log("Admin user created successfully!");
    console.log("User ID:", data.user?.id);
  }
}

createAdmin();
