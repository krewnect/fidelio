import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Patch openAdminMerchant
old_open = """            // 1. Fetch Merchant Details
            const { data: m, error: mErr } = await window.supabaseClient.from('merchants').select('business_name, plan_status, created_at, custom_price').eq('id', merchantId).single();
            if (mErr) throw mErr;
            
            document.getElementById('admin-merchant-name').textContent = m.business_name;
            document.getElementById('admin-merchant-id').textContent = merchantId;
            document.getElementById('admin-merchant-created').textContent = new Date(m.created_at).toLocaleDateString();
            document.getElementById('admin-merchant-status').textContent = m.plan_status.toUpperCase();
            document.getElementById('admin-custom-price').value = m.custom_price || "";"""

new_open = """            // 1. Fetch Merchant Details (Including new expiry column safely in case it doesn't exist yet)
            const { data: m, error: mErr } = await window.supabaseClient.from('merchants').select('business_name, plan_status, created_at, custom_price, custom_price_expires_at').eq('id', merchantId).single();
            if (mErr) throw mErr;
            
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
                    expiryLabel.style.color = "var(--accent-violet)";
                } else {
                    expiryLabel.textContent = "El precio especial ha expirado (se cobrará normal)";
                    expiryLabel.style.color = "#ef4444";
                }
            } else if (m.custom_price) {
                expiryLabel.textContent = "Vigencia: Vitalicia (Lifetime)";
                expiryLabel.style.color = "#10b981";
            } else {
                expiryLabel.textContent = "";
            }"""

js = js.replace(old_open, new_open)

# Patch saveAdminCustomPrice
old_save = """    window.saveAdminCustomPrice = async function() {
        if (window.fidelioAdminRole !== 'admin' && window.fidelioAdminRole !== 'super_admin') return;
        const id = document.getElementById('admin-current-merchant-id').value;
        const priceVal = document.getElementById('admin-custom-price').value;
        const customPrice = priceVal ? parseFloat(priceVal) : null;
        
        const { error } = await window.supabaseClient.from('merchants').update({ custom_price: customPrice }).eq('id', id);
        if (error) {
            window.showToast("Error al guardar precio", "error");
        } else {
            window.showToast("Precio personalizado actualizado", "success");
        }
    };"""

new_save = """    window.saveAdminCustomPrice = async function() {
        if (window.fidelioAdminRole !== 'admin' && window.fidelioAdminRole !== 'super_admin') return;
        const id = document.getElementById('admin-current-merchant-id').value;
        const priceVal = document.getElementById('admin-custom-price').value;
        const monthsVal = document.getElementById('admin-custom-price-months').value;
        
        const customPrice = priceVal ? parseFloat(priceVal) : null;
        let expiresAt = null;
        
        if (customPrice && monthsVal) {
            const months = parseInt(monthsVal);
            if (months > 0) {
                const date = new Date();
                date.setMonth(date.getMonth() + months);
                expiresAt = date.toISOString();
            }
        }
        
        const { error } = await window.supabaseClient.from('merchants').update({ 
            custom_price: customPrice,
            custom_price_expires_at: expiresAt
        }).eq('id', id);
        
        if (error) {
            window.showToast("Error al guardar precio", "error");
            console.error(error);
        } else {
            window.showToast("Precio personalizado actualizado", "success");
            // Refresh visual status
            openAdminMerchant(id);
        }
    };"""

js = js.replace(old_save, new_save)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS logic patched.")
