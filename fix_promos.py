import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html = """<button class="fidelio-btn-primary"><i class="fa-solid fa-check"></i> Aplicar</button>"""
new_html = """<button class="fidelio-btn-primary" onclick="window.applyUpsellPromo()"><i class="fa-solid fa-check"></i> Aplicar</button>"""

if old_html in html:
    html = html.replace(old_html, new_html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html patched.")

# 2. Update dashboard_v2.js
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_js = """        if (data.current_uses >= data.max_uses) {
            return window.showToast('Este código ha superado su límite de usos', 'error');
        }

        const btnUpsell = document.getElementById('btn-upsell-stripe');
        
        if (data.reward_type === 'free_branches') {
            window.showToast(`¡Código aplicado! Tienes ${data.free_branches_count} sucursales extra gratis.`, 'success');
            btnUpsell.innerHTML = '<i class="fa-solid fa-check"></i> Activar Sucursales Gratis';
            btnUpsell.onclick = async () => {
                await window.supabaseClient.from('promo_codes').update({ current_uses: data.current_uses + 1 }).eq('code', code);
                window.showToast('Sucursales habilitadas', 'success');
                setTimeout(() => window.location.reload(), 1500);
            };
        } else if (data.reward_type === 'custom_branch_price') {
            window.showToast(`¡Código aplicado! Precio preferencial de $${data.custom_branch_price} USD.`, 'success');
            btnUpsell.innerHTML = `<i class="fa-brands fa-stripe"></i> Pagar $${data.custom_branch_price} USD / mes`;
            // Si tuvieras un link específico para esto en la DB, podrías reemplazarlo aquí.
        } else if (data.reward_type === 'lifetime_free' || (data.reward_type === 'discount' && data.discount_pct === 100)) {
            window.showToast('¡Felicidades! Tienes acceso ilimitado gratuito.', 'success');
            btnUpsell.innerHTML = '<i class="fa-solid fa-check"></i> Activar Licencia Gratuita';
            btnUpsell.onclick = async () => {
                await window.supabaseClient.from('promo_codes').update({ current_uses: data.current_uses + 1 }).eq('code', code);
                window.showToast('Licencia habilitada', 'success');
                setTimeout(() => window.location.reload(), 1500);
            };"""

new_js = """        if (data.used_count >= data.max_uses) {
            return window.showToast('Este código ha superado su límite de usos', 'error');
        }

        const btnUpsell = document.getElementById('btn-upsell-stripe');
        
        if (data.reward_type === 'free_branches') {
            window.showToast(`¡Código aplicado! Tienes ${data.free_branches_count} sucursales extra gratis.`, 'success');
            btnUpsell.innerHTML = '<i class="fa-solid fa-check"></i> Activar Sucursales Gratis';
            btnUpsell.onclick = async () => {
                await window.supabaseClient.from('promo_codes').update({ used_count: data.used_count + 1 }).eq('code', code);
                window.showToast('Sucursales habilitadas', 'success');
                setTimeout(() => window.location.reload(), 1500);
            };
        } else if (data.reward_type === 'custom_branch_price') {
            window.showToast(`¡Código aplicado! Precio preferencial de $${data.custom_branch_price} USD.`, 'success');
            btnUpsell.innerHTML = `<i class="fa-brands fa-stripe"></i> Pagar $${data.custom_branch_price} USD / mes`;
        } else if (data.reward_type === 'lifetime_free' || (data.reward_type === 'discount' && data.discount_pct >= 100)) {
            window.showToast('¡Felicidades! Tienes acceso ilimitado gratuito.', 'success');
            btnUpsell.innerHTML = '<i class="fa-solid fa-check"></i> Activar Licencia Gratuita';
            btnUpsell.onclick = async () => {
                await window.supabaseClient.from('promo_codes').update({ used_count: data.used_count + 1 }).eq('code', code);
                await window.supabaseClient.from('merchants').update({ plan_status: 'active_lifetime' }).eq('id', window.fidelioState.tenantId);
                window.showToast('Licencia habilitada', 'success');
                setTimeout(() => window.location.reload(), 1500);
            };"""

if old_js in js:
    js = js.replace(old_js, new_js)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v2.js patched.")
else:
    print("Failed to patch JS.")

