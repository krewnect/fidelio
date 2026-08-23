import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

billing_func = """
    // 4. BILLING HISTORY
    window.loadBillingHistory = async function() {
        if (window.fidelioAdminRole !== 'admin' && window.fidelioAdminRole !== 'super_admin') return;
        const tbody = document.getElementById('billing-history-body');
        if (!tbody) return;
        
        tbody.innerHTML = '<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--text-muted);">Cargando...</td></tr>';
        
        const { data, error } = await window.supabaseClient.from('merchants').select('id, business_name, plan_status, created_at, custom_price').order('created_at', { ascending: false });
        if (error) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;
            return;
        }
        
        tbody.innerHTML = '';
        
        (data || []).forEach(m => {
            const createdDate = new Date(m.created_at);
            const now = new Date();
            const monthsActive = Math.max(0, Math.floor((now - createdDate) / (1000 * 60 * 60 * 24 * 30)));
            
            let planText = m.plan_status.toUpperCase();
            let tarifa = m.custom_price ? `$${m.custom_price} MXN` : 'Oficial Stripe';
            let ltv = 0;
            let estado = '<span style="color:#10b981;">Al Día</span>';
            
            if (m.plan_status === 'trial') {
                tarifa = '$0.00 MXN';
                ltv = '$0.00 MXN';
                estado = '<span style="color:#f59e0b;">Trial Activo</span>';
            } else if (m.plan_status === 'lifetime_free') {
                tarifa = '$0.00 MXN';
                ltv = '$0.00 MXN';
                estado = '<span style="color:#10b981;">Gratis</span>';
            } else if (m.plan_status === 'active') {
                let monthlyRate = m.custom_price ? m.custom_price : 999; // assuming base price if custom is null
                ltv = `$${(monthlyRate * monthsActive).toLocaleString()} MXN`;
                estado = '<span style="color:#10b981;">Pagado</span>';
            } else {
                ltv = 'N/A';
                estado = `<span style="color:#ef4444;">${planText}</span>`;
            }
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft); transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 12px 24px 12px 8px; white-space: nowrap;"><strong style="font-size: 14px;">${m.business_name}</strong></td>
                    <td style="padding: 12px 24px; white-space: nowrap; color: var(--text-muted);">${createdDate.toLocaleDateString()}</td>
                    <td style="padding: 12px 24px; white-space: nowrap;"><span class="menu-badge" style="background:var(--accent-violet);color:#fff;font-size:10px;">${planText}</span></td>
                    <td style="padding: 12px 24px; white-space: nowrap; font-variant-numeric: tabular-nums;">${tarifa}</td>
                    <td style="padding: 12px 24px; white-space: nowrap; font-weight:700; font-variant-numeric: tabular-nums;">${ltv}</td>
                    <td style="padding: 12px 8px; white-space: nowrap;">${estado}</td>
                </tr>
            `;
        });
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--text-muted);">No hay negocios registrados.</td></tr>';
        }
    };
"""

# Append to the end of the IIFE
# Let's just place it before window.loadMerchantsControl
old_anchor = "    // 3. MERCHANTS CONTROL"
if old_anchor in js:
    js = js.replace(old_anchor, billing_func + "\n" + old_anchor)
else:
    print("WARNING: Could not find anchor to inject JS")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS patched.")
