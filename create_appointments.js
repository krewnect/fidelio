require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_KEY);

async function run() {
    const sql = `
    CREATE TABLE IF NOT EXISTS public.appointments (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        merchant_id UUID REFERENCES public.merchants(id) ON DELETE CASCADE,
        customer_id UUID REFERENCES public.customers(id) ON DELETE CASCADE,
        campaign_id UUID REFERENCES public.campaigns(id) ON DELETE CASCADE,
        appointment_date DATE NOT NULL,
        appointment_time TIME NOT NULL,
        status TEXT DEFAULT 'pending', -- pending, confirmed, cancelled
        notes TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
    );
    ALTER TABLE public.appointments ENABLE ROW LEVEL SECURITY;
    
    DROP POLICY IF EXISTS "Merchants can view their appointments" ON public.appointments;
    CREATE POLICY "Merchants can view their appointments" ON public.appointments FOR SELECT USING (merchant_id = auth.uid());
    
    DROP POLICY IF EXISTS "Merchants can update appointments" ON public.appointments;
    CREATE POLICY "Merchants can update appointments" ON public.appointments FOR UPDATE USING (merchant_id = auth.uid());
    
    DROP POLICY IF EXISTS "Anyone can insert appointments" ON public.appointments;
    CREATE POLICY "Anyone can insert appointments" ON public.appointments FOR INSERT WITH CHECK (true);
    `;
    const { error } = await supabase.rpc('exec_sql', { sql_query: sql });
    if (error) {
        console.log("RPC exec_sql failed, trying direct query if possible", error);
        // Fallback for direct postgres if needed
    } else {
        console.log("Created appointments table successfully via RPC.");
    }
}
run();
