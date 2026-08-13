-- Eschema inicial de la Base de Datos para Fidelio (Supabase) V2 (Corregido)

-- 1. Tabla de Comercios (Merchants)
CREATE TABLE public.merchants (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    business_name TEXT NOT NULL,
    industry TEXT DEFAULT 'restaurant',
    plan_status TEXT DEFAULT 'trial',
    stripe_customer_id TEXT,
    
    -- Configuración de Diseño
    color_primary TEXT DEFAULT '#1e1b4b',
    color_accent TEXT DEFAULT '#8b5cf6',
    logo_url TEXT,
    banner_url TEXT,
    
    -- Configuración de Lealtad
    cashback_percent NUMERIC DEFAULT 10.0,
    stamps_total INTEGER DEFAULT 5,
    stamps_reward_text TEXT DEFAULT 'Premio Gratis'
);

ALTER TABLE public.merchants ENABLE ROW LEVEL SECURITY;

-- 2. Tabla de Clientes (Customers)
CREATE TABLE public.customers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    merchant_id UUID REFERENCES public.merchants(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    birthday DATE,
    
    -- Saldos Actuales
    balance_cashback NUMERIC DEFAULT 0.0,
    stamps_count INTEGER DEFAULT 0,
    vip_tier TEXT DEFAULT 'Bronce',
    
    UNIQUE(merchant_id, email)
);

ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;

-- 3. Tabla de Transacciones (Transactions)
CREATE TABLE public.transactions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    merchant_id UUID REFERENCES public.merchants(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES public.customers(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    transaction_type TEXT NOT NULL, 
    amount_spent NUMERIC DEFAULT 0.0,
    cashback_earned NUMERIC DEFAULT 0.0,
    cashback_redeemed NUMERIC DEFAULT 0.0,
    stamps_earned INTEGER DEFAULT 0,
    
    notes TEXT
);

ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;

-- Políticas de Seguridad (RLS)
CREATE POLICY "Comercios_Select" ON public.merchants FOR SELECT USING (true);
CREATE POLICY "Comercios_Update" ON public.merchants FOR UPDATE USING (true);

CREATE POLICY "Clientes_Select" ON public.customers FOR SELECT USING (true);
CREATE POLICY "Clientes_Insert" ON public.customers FOR INSERT WITH CHECK (true);
CREATE POLICY "Clientes_Update" ON public.customers FOR UPDATE USING (true);

CREATE POLICY "Transacciones_Select" ON public.transactions FOR SELECT USING (true);
CREATE POLICY "Transacciones_Insert" ON public.transactions FOR INSERT WITH CHECK (true);

-- 4. Tabla de Códigos Promocionales (Suscripciones SaaS)
CREATE TABLE public.promo_codes (
    code TEXT PRIMARY KEY,
    reward_type TEXT NOT NULL, -- '1_month_free', 'lifetime_free', 'discount'
    discount_pct NUMERIC DEFAULT 0,
    max_uses INTEGER DEFAULT 1,
    used_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.promo_codes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Promo_Codes_Select" ON public.promo_codes FOR SELECT USING (true);
CREATE POLICY "Promo_Codes_Update" ON public.promo_codes FOR UPDATE USING (true);
CREATE POLICY "Promo_Codes_Insert" ON public.promo_codes FOR INSERT WITH CHECK (true);
