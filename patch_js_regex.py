import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern = r"// 1\. Fetch Merchant Details.*?document\.getElementById\('admin-merchant-name'\)\.textContent = m\.business_name;"

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

js = re.sub(pattern, new, js, flags=re.DOTALL)
with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS regex patched.")
