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
CREATE POLICY "Comercios_Select" ON public.merchants FOR SELECT USING (id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');
CREATE POLICY "Comercios_Update" ON public.merchants FOR UPDATE USING (id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');

CREATE POLICY "Clientes_Select" ON public.customers FOR SELECT USING (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');
CREATE POLICY "Clientes_Insert" ON public.customers FOR INSERT WITH CHECK (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');
CREATE POLICY "Clientes_Update" ON public.customers FOR UPDATE USING (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');

CREATE POLICY "Transacciones_Select" ON public.transactions FOR SELECT USING (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');
CREATE POLICY "Transacciones_Insert" ON public.transactions FOR INSERT WITH CHECK (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');

-- 4. Tabla de Códigos Promocionales (Suscripciones SaaS)
CREATE TABLE public.promo_codes (
    code TEXT PRIMARY KEY,
    reward_type TEXT NOT NULL,
    target_plan TEXT DEFAULT 'business', -- '1_month_free', 'lifetime_free', 'discount'
    discount_pct NUMERIC DEFAULT 0,
    max_uses INTEGER DEFAULT 1,
    used_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    stripe_payment_link TEXT,
    free_branches_count INTEGER DEFAULT 0,
    custom_branch_price NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE public.promo_codes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Promo_Codes_Select" ON public.promo_codes FOR SELECT USING (true);
CREATE POLICY "Promo_Codes_Update" ON public.promo_codes FOR UPDATE USING (auth.jwt()->>'email' = 'hola@fideliorewards.com');
CREATE POLICY "Promo_Codes_Insert" ON public.promo_codes FOR INSERT WITH CHECK (auth.jwt()->>'email' = 'hola@fideliorewards.com');
-- Fase 1: Arquitectura Multi-Tarjeta (Pases)

-- 1. Crear tabla para las diferentes campañas (tarjetas) de cada negocio
CREATE TABLE public.campaigns (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    merchant_id uuid NOT NULL REFERENCES public.merchants(id) ON DELETE CASCADE,
    type text NOT NULL CHECK (type IN ('stamps', 'cashback', 'membership', 'coupon', 'multipass')),
    name text NOT NULL,
    description text,
    
    -- Configuración visual específica de esta campaña
    color_primary text,
    color_accent text,
    logo_url text,
    banner_url text,
    stamp_icon_url text, -- Permite subir un icono personalizado para los sellos
    background_image_url text, -- Permite una imagen de fondo completa (eventTicket)
    
    -- Customización de Landing/Botón
    custom_cta_label text, -- Ej. "Agendar Cita", "Comprar Servicio"
    custom_cta_url text, -- El link a donde dirige el botón
    
    -- Configuración de reglas (JSON flexible para soportar sellos, % cashback, etc.)
    rules_config jsonb NOT NULL DEFAULT '{}'::jsonb,
    
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now()
);

-- 1.5. Agregar campos de integración de Stripe a los comercios (merchants)
ALTER TABLE public.merchants 
ADD COLUMN IF NOT EXISTS stripe_pub_key text,
ADD COLUMN IF NOT EXISTS stripe_secret_key text;


-- 2. Políticas RLS (Row Level Security) para campaigns
ALTER TABLE public.campaigns ENABLE ROW LEVEL SECURITY;

-- Por simplicidad del MVP (igual que en merchants), permitimos acceso global por ahora
CREATE POLICY "Campaigns_Select" ON public.campaigns FOR SELECT USING (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');
CREATE POLICY "Campaigns_Insert" ON public.campaigns FOR INSERT WITH CHECK (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');
CREATE POLICY "Campaigns_Update" ON public.campaigns FOR UPDATE USING (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');
CREATE POLICY "Campaigns_Delete" ON public.campaigns FOR DELETE USING (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com');

-- 3. Crear tabla pivote para los pases guardados por los clientes
-- (Esto permite que un cliente guarde varias tarjetas del mismo negocio)
CREATE TABLE public.customer_campaigns (
    id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    customer_id uuid NOT NULL REFERENCES public.customers(id) ON DELETE CASCADE,
    campaign_id uuid NOT NULL REFERENCES public.campaigns(id) ON DELETE CASCADE,
    
    -- Progreso o balance actual específico para esta tarjeta
    current_balance numeric(10,2) DEFAULT 0, -- Sellos acumulados, saldo cashback, etc.
    
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    
    UNIQUE(customer_id, campaign_id)
);

ALTER TABLE public.customer_campaigns ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Customer_Campaigns_Select" ON public.customer_campaigns FOR SELECT USING ( EXISTS (SELECT 1 FROM public.campaigns WHERE id = campaign_id AND (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com')) );
CREATE POLICY "Customer_Campaigns_Insert" ON public.customer_campaigns FOR INSERT WITH CHECK ( EXISTS (SELECT 1 FROM public.campaigns WHERE id = campaign_id AND (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com')) );
CREATE POLICY "Customer_Campaigns_Update" ON public.customer_campaigns FOR UPDATE USING ( EXISTS (SELECT 1 FROM public.campaigns WHERE id = campaign_id AND (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com')) );
CREATE POLICY "Customer_Campaigns_Delete" ON public.customer_campaigns FOR DELETE USING ( EXISTS (SELECT 1 FROM public.campaigns WHERE id = campaign_id AND (merchant_id = auth.uid() OR auth.jwt()->>'email' = 'hola@fideliorewards.com')) );

-- 4. Opcional: Migración de datos
-- (Mover las configuraciones globales actuales de merchants a una campaña inicial por defecto)
INSERT INTO public.campaigns (merchant_id, type, name, description, color_primary, color_accent, logo_url, banner_url, rules_config)
SELECT 
    id, 
    'stamps', 
    business_name || ' Rewards', 
    'Tarjeta principal de lealtad', 
    color_primary, 
    color_accent, 
    logo_url, 
    banner_url, 
    jsonb_build_object(
        'stamps_total', stamps_total, 
        'stamps_reward_text', stamps_reward_text,
        'cashback_percent', cashback_percent
    )
FROM public.merchants;
