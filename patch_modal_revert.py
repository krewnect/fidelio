import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove the broken backend fetch entirely and replace it with direct merchants query
old_js = """        try {
            // Fetch Owner Auth Details via secure backend API
            fetch('https://fidelio-41j9.onrender.com/api/admin/merchant-details/' + merchantId)
                .then(res => res.json())
                .then(user => {
                    const fullName = (user.first_name + ' ' + user.last_name).trim();
                    document.getElementById('admin-merchant-owner').textContent = fullName || 'No especificado';
                    document.getElementById('admin-merchant-email').textContent = user.email || 'No disponible';
                    document.getElementById('admin-merchant-phone').textContent = user.phone || 'No registrado';
                })
                .catch(err => {
                    document.getElementById('admin-merchant-owner').textContent = 'Error';
                    document.getElementById('admin-merchant-email').textContent = 'Error';
                    document.getElementById('admin-merchant-phone').textContent = 'Error';
                });

            // 1. Fetch Merchant Details
            const { data: m, error: mErr } = await window.supabaseClient.from('merchants').select('business_name, plan_status, created_at, custom_price, custom_price_expires_at').eq('id', merchantId).single();"""

new_js = """        try {
            // 1. Fetch Merchant Details
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
"""

if old_js in js:
    js = js.replace(old_js, new_js)
with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS reverted to direct DB query.")
