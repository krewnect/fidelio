import re

with open('pass.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                if (!customerId || !campaignId) {
                    throw new Error("Pase o campaña no encontrados");
                }

                // 3. Fetch Customer
                const { data: customer, error: cErr } = await supabase
                    .from('customers')
                    .select('*')
                    .eq('id', customerId)
                    .single();

                if (cErr || !customer) throw new Error("Cliente no encontrado");"""

replacement = """                if (!customerId || !campaignId) {
                    throw new Error("Pase o campaña no encontrados");
                }

                let customer = null;
                
                if (customerId === 'DEMO') {
                    // Mock data for demo passes
                    customer = {
                        id: 'DEMO',
                        full_name: 'Invitado Demo',
                        name: 'Invitado',
                        vip_tier: 'DEMO',
                        balance_cashback: 0,
                        stamps_count: 3,
                        visits: 1,
                        merchant_id: 'DEMO'
                    };
                } else {
                    // 3. Fetch Customer
                    const { data: realCustomer, error: cErr } = await supabase
                        .from('customers')
                        .select('*')
                        .eq('id', customerId)
                        .single();

                    if (cErr || !realCustomer) throw new Error("Cliente no encontrado");
                    customer = realCustomer;
                }"""

html = html.replace(target, replacement)

target2 = """                // 5. Fetch Merchant for fallback/business_type
                const { data: merchant, error: mErr } = await supabase
                    .from('merchants')
                    .select('business_name, business_type')
                    .eq('id', customer.merchant_id)
                    .single();"""

replacement2 = """                // 5. Fetch Merchant for fallback/business_type
                let merchant = null;
                if (customer.merchant_id === 'DEMO') {
                    merchant = { business_name: 'Mi Negocio (Demo)', business_type: 'professional' };
                } else {
                    const { data: realMerchant, error: mErr } = await supabase
                        .from('merchants')
                        .select('business_name, business_type')
                        .eq('id', customer.merchant_id)
                        .single();
                    merchant = realMerchant;
                }"""

html = html.replace(target2, replacement2)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(html)
