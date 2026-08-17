import re

def patch_schema():
    with open('schema.sql', 'r') as f:
        sql = f.read()

    # Merchants
    sql = sql.replace('CREATE POLICY "Comercios_Select" ON public.merchants FOR SELECT USING (true);',
                      'CREATE POLICY "Comercios_Select" ON public.merchants FOR SELECT USING (id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')
    sql = sql.replace('CREATE POLICY "Comercios_Update" ON public.merchants FOR UPDATE USING (true);',
                      'CREATE POLICY "Comercios_Update" ON public.merchants FOR UPDATE USING (id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')

    # Customers
    sql = sql.replace('CREATE POLICY "Clientes_Select" ON public.customers FOR SELECT USING (true);',
                      'CREATE POLICY "Clientes_Select" ON public.customers FOR SELECT USING (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')
    sql = sql.replace('CREATE POLICY "Clientes_Insert" ON public.customers FOR INSERT WITH CHECK (true);',
                      'CREATE POLICY "Clientes_Insert" ON public.customers FOR INSERT WITH CHECK (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')
    sql = sql.replace('CREATE POLICY "Clientes_Update" ON public.customers FOR UPDATE USING (true);',
                      'CREATE POLICY "Clientes_Update" ON public.customers FOR UPDATE USING (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')

    # Transactions
    sql = sql.replace('CREATE POLICY "Transacciones_Select" ON public.transactions FOR SELECT USING (true);',
                      'CREATE POLICY "Transacciones_Select" ON public.transactions FOR SELECT USING (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')
    sql = sql.replace('CREATE POLICY "Transacciones_Insert" ON public.transactions FOR INSERT WITH CHECK (true);',
                      'CREATE POLICY "Transacciones_Insert" ON public.transactions FOR INSERT WITH CHECK (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')

    # Promo codes
    sql = sql.replace('CREATE POLICY "Promo_Codes_Update" ON public.promo_codes FOR UPDATE USING (true);',
                      'CREATE POLICY "Promo_Codes_Update" ON public.promo_codes FOR UPDATE USING (auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')
    sql = sql.replace('CREATE POLICY "Promo_Codes_Insert" ON public.promo_codes FOR INSERT WITH CHECK (true);',
                      'CREATE POLICY "Promo_Codes_Insert" ON public.promo_codes FOR INSERT WITH CHECK (auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')

    # Campaigns
    sql = sql.replace('CREATE POLICY "Campaigns_Select" ON public.campaigns FOR SELECT USING (true);',
                      'CREATE POLICY "Campaigns_Select" ON public.campaigns FOR SELECT USING (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')
    sql = sql.replace('CREATE POLICY "Campaigns_Insert" ON public.campaigns FOR INSERT WITH CHECK (true);',
                      'CREATE POLICY "Campaigns_Insert" ON public.campaigns FOR INSERT WITH CHECK (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')
    sql = sql.replace('CREATE POLICY "Campaigns_Update" ON public.campaigns FOR UPDATE USING (true);',
                      'CREATE POLICY "Campaigns_Update" ON public.campaigns FOR UPDATE USING (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')
    sql = sql.replace('CREATE POLICY "Campaigns_Delete" ON public.campaigns FOR DELETE USING (true);',
                      'CREATE POLICY "Campaigns_Delete" ON public.campaigns FOR DELETE USING (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\');')

    # Customer Campaigns
    sql = sql.replace('CREATE POLICY "Customer_Campaigns_Select" ON public.customer_campaigns FOR SELECT USING (true);',
                      'CREATE POLICY "Customer_Campaigns_Select" ON public.customer_campaigns FOR SELECT USING ( EXISTS (SELECT 1 FROM public.campaigns WHERE id = campaign_id AND (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\')) );')
    sql = sql.replace('CREATE POLICY "Customer_Campaigns_Insert" ON public.customer_campaigns FOR INSERT WITH CHECK (true);',
                      'CREATE POLICY "Customer_Campaigns_Insert" ON public.customer_campaigns FOR INSERT WITH CHECK ( EXISTS (SELECT 1 FROM public.campaigns WHERE id = campaign_id AND (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\')) );')
    sql = sql.replace('CREATE POLICY "Customer_Campaigns_Update" ON public.customer_campaigns FOR UPDATE USING (true);',
                      'CREATE POLICY "Customer_Campaigns_Update" ON public.customer_campaigns FOR UPDATE USING ( EXISTS (SELECT 1 FROM public.campaigns WHERE id = campaign_id AND (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\')) );')
    sql = sql.replace('CREATE POLICY "Customer_Campaigns_Delete" ON public.customer_campaigns FOR DELETE USING (true);',
                      'CREATE POLICY "Customer_Campaigns_Delete" ON public.customer_campaigns FOR DELETE USING ( EXISTS (SELECT 1 FROM public.campaigns WHERE id = campaign_id AND (merchant_id = auth.uid() OR auth.jwt()->>\'email\' = \'hola@fideliorewards.com\')) );')

    with open('schema.sql', 'w') as f:
        f.write(sql)

if __name__ == "__main__":
    patch_schema()
