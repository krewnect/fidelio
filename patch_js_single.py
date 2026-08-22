import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the NPE
old = """            // 1. Fetch Merchant Details
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
            
            document.getElementById('admin-merchant-name').textContent = m.business_name;"""

new = """            // 1. Fetch Merchant Details
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
            
            document.getElementById('admin-merchant-name').textContent = m.business_name;"""

if old in js:
    js = js.replace(old, new)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched.")
else:
    print("Not found.")
