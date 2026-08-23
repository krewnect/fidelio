import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_js = """            // 1. Fetch Merchant Details
            const { data: m, error: mErr } = await window.supabaseClient.from('merchants').select('business_name, plan_status, created_at, custom_price, custom_price_expires_at, owner_name, owner_email, owner_phone').eq('id', merchantId).single();
            if (!mErr) {
                document.getElementById('admin-merchant-owner').textContent = m.owner_name || 'Pendiente de Sincronizar';
                document.getElementById('admin-merchant-email').textContent = m.owner_email || 'Pendiente de Sincronizar';
                document.getElementById('admin-merchant-phone').textContent = m.owner_phone || 'Pendiente de Sincronizar';
            } else {
                document.getElementById('admin-merchant-owner').textContent = 'Error DB';
                document.getElementById('admin-merchant-email').textContent = 'Error DB';
                document.getElementById('admin-merchant-phone').textContent = 'Error DB';
            }
            
            document.getElementById('admin-merchant-name').textContent = m.business_name;
            document.getElementById('admin-merchant-id').textContent = merchantId;
            document.getElementById('admin-merchant-created').textContent = new Date(m.created_at).toLocaleDateString();
            document.getElementById('admin-merchant-status').textContent = m.plan_status.toUpperCase();
            document.getElementById('admin-custom-price').value = m.custom_price || "";
            document.getElementById('admin-custom-price-months').value = ""; // Reset
            
            const expiryLabel = document.getElementById('admin-custom-price-expiry-label');
            if (m.custom_price && m.custom_price_expires_at) {
                const expDate = new Date(m.custom_price_expires_at);
                if (expDate > new Date()) {
                    expiryLabel.textContent = `Vence el: ${expDate.toLocaleDateString('es-MX')}`;
                } else {
                    expiryLabel.textContent = "Expirado";
                }
            } else {
                expiryLabel.textContent = "";
            }"""

new_js = """            // 1. Fetch Merchant Details
            const { data: m, error: mErr } = await window.supabaseClient.from('merchants').select('*').eq('id', merchantId).single();
            if (mErr) {
                document.getElementById('admin-merchant-owner').textContent = 'Error DB';
                document.getElementById('admin-merchant-email').textContent = 'Error DB';
                document.getElementById('admin-merchant-phone').textContent = 'Error DB';
                throw mErr;
            }
            
            document.getElementById('admin-merchant-owner').textContent = m.owner_name || 'No especificado';
            document.getElementById('admin-merchant-email').textContent = m.owner_email || 'No disponible';
            document.getElementById('admin-merchant-phone').textContent = m.owner_phone || 'No registrado';
            
            document.getElementById('admin-merchant-name').textContent = m.business_name;
            document.getElementById('admin-merchant-id').textContent = merchantId;
            document.getElementById('admin-merchant-created').textContent = new Date(m.created_at).toLocaleDateString();
            document.getElementById('admin-merchant-status').textContent = m.plan_status.toUpperCase();
            document.getElementById('admin-custom-price').value = m.custom_price || "";
            document.getElementById('admin-custom-price-months').value = ""; // Reset
            
            const expiryLabel = document.getElementById('admin-custom-price-expiry-label');
            if (m.custom_price && m.custom_price_expires_at) {
                const expDate = new Date(m.custom_price_expires_at);
                if (expDate > new Date()) {
                    expiryLabel.textContent = `Vence el: ${expDate.toLocaleDateString('es-MX')}`;
                } else {
                    expiryLabel.textContent = "Expirado";
                }
            } else {
                expiryLabel.textContent = "";
            }"""

if old_js in js:
    js = js.replace(old_js, new_js)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("JS fixed.")
else:
    print("WARNING: Could not find code to fix in JS")
