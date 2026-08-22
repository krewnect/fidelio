import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Fix the checkPlanPermissions for professional-only tabs
old_pro_only = """            // Toggle Professional-only tabs
            document.querySelectorAll('.plan-professional-only').forEach(el => {
                if(isAdmin) {
                    el.style.display = ''; // Admin ve TODO
                } else if(isBusiness && plan !== 'professional') {
                    el.style.display = 'none'; // Solo ocultar si es 100% negocio y NO profesional
                } else {
                    el.style.display = ''; // Mostrar por defecto para professionals
                }
            });"""

new_pro_only = """            // Toggle Professional-only tabs
            document.querySelectorAll('.plan-professional-only').forEach(el => {
                if(plan === 'professional') {
                    el.style.display = '';
                } else {
                    el.style.display = 'none'; 
                }
            });"""

if old_pro_only in js:
    js = js.replace(old_pro_only, new_pro_only)
    print("Patched checkPlanPermissions")
else:
    print("Could not find old_pro_only")

# 2. Fix applyUpsellPromo crashing and failing to set business_type
old_upsell = """            btnUpsell.onclick = async () => {
                await window.supabaseClient.from('promo_codes').update({ used_count: data.used_count + 1 }).eq('code', code);
                await window.supabaseClient.from('merchants').update({ plan_status: 'active_lifetime' }).eq('id', window.fidelioState.tenantId);
                window.showToast('Licencia habilitada', 'success');"""

new_upsell = """            btnUpsell.onclick = async () => {
                await window.supabaseClient.from('promo_codes').update({ used_count: data.used_count + 1 }).eq('code', code);
                await window.supabaseClient.from('merchants').update({ plan_status: 'active_lifetime', business_type: data.target_plan || 'business' }).eq('id', state.tenantId);
                window.showToast('Licencia habilitada', 'success');"""

if old_upsell in js:
    js = js.replace(old_upsell, new_upsell)
    print("Patched applyUpsellPromo")
else:
    print("Could not find old_upsell")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
