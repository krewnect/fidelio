-- Asegurar la tabla de clientes contra modificaciones maliciosas

-- Primero, la Inserción de clientes
-- Solo permitiremos inserciones si vienen autenticadas por un admin/cajero o si es anónima desde el portal público
-- Como join.html usa el public anon key, el insert debe ser público, pero el update NO.
DROP POLICY IF EXISTS "Clientes_Insert" ON public.customers;
CREATE POLICY "Clientes_Insert" ON public.customers FOR INSERT WITH CHECK (true);

-- Segundo, la Modificación de clientes (Evitar que un cliente edite su propio balance_cashback)
DROP POLICY IF EXISTS "Clientes_Update" ON public.customers;
CREATE POLICY "Clientes_Update" ON public.customers FOR UPDATE USING (
    -- El usuario es el dueño del comercio
    auth.uid() = merchant_id 
    OR 
    -- El usuario es un cajero de este comercio
    (auth.jwt() -> 'user_metadata' ->> 'merchant_id')::uuid = merchant_id
);

-- Tercero, Transacciones
-- Solo el personal o el dueño pueden insertar transacciones
DROP POLICY IF EXISTS "Transacciones_Insert" ON public.transactions;
CREATE POLICY "Transacciones_Insert" ON public.transactions FOR INSERT WITH CHECK (
    auth.uid() = merchant_id 
    OR 
    (auth.jwt() -> 'user_metadata' ->> 'merchant_id')::uuid = merchant_id
);

DROP POLICY IF EXISTS "Transacciones_Select" ON public.transactions;
CREATE POLICY "Transacciones_Select" ON public.transactions FOR SELECT USING (
    auth.uid() = merchant_id 
    OR 
    (auth.jwt() -> 'user_metadata' ->> 'merchant_id')::uuid = merchant_id
);
