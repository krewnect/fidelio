import re

with open('pass.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                // 3. Fetch Customer
                const { data: realCustomer, error: cErr } = await supabase
                    .from('customers')
                    .select('*')
                    .eq('id', customerId)
                    .single();

                if (cErr || !realCustomer) throw new Error("Cliente no encontrado");
                customer = realCustomer;
            }

            // 4. Fetch Campaign
            const { data: campaign, error: campErr } = await supabase
                .from('campaigns')
                .select('*')
                .eq('id', campaignId)
                .single();
                
            if (campErr || !campaign) throw new Error("Campaña no encontrada");

            // 5. Fetch Merchant for fallback/business_type
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

replacement = """                // Fetch all data via backend API to bypass RLS safely
                const apiRes = await fetch(`/api/wallet/data?c=${customerId}&camp=${campaignId}`);
                const apiData = await apiRes.json();
                
                if (!apiData.success) {
                    throw new Error(apiData.error || "Pase no válido");
                }
                
                customer = apiData.customer;
                campaign = apiData.campaign;
                merchant = apiData.merchant;
            } else {
                // If DEMO, we must still fetch campaign data manually via backend (we pass c=DEMO)
                // Wait, if c=DEMO, backend will fail. Let's make backend return mock if c=DEMO, or just fetch campaign here via backend
                // ACTUALLY, let's just make the backend handle DEMO! 
            }
"""

# Actually, the logic is getting messy. Let's replace the whole data fetch block cleanly.

target_full = """                // 3. Fetch Customer
                const { data: realCustomer, error: cErr } = await supabase
                    .from('customers')
                    .select('*')
                    .eq('id', customerId)
                    .single();

                if (cErr || !realCustomer) throw new Error("Cliente no encontrado");
                customer = realCustomer;
            }

            // 4. Fetch Campaign
            const { data: campaign, error: campErr } = await supabase
                .from('campaigns')
                .select('*')
                .eq('id', campaignId)
                .single();
                
            if (campErr || !campaign) throw new Error("Campaña no encontrada");

            // 5. Fetch Merchant for fallback/business_type
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

replacement_full = """            
                let campaign, merchant;
                
                if (customerId === 'DEMO') {
                    // Fetch just the campaign via API by passing a special flag or just query supabase directly since campaign might be public?
                    // Actually, let's just use the backend endpoint and let the backend handle the DEMO logic!
                }
"""

# Better yet, I will rewrite the entire script tag section from "let customer = null;" down to "merchant = realMerchant;"
