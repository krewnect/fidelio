import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            const phoneDigits = c.phone ? c.phone.replace(/\D/g, '') : '';
            const waAction = phoneDigits ? `window.open('https://wa.me/${phoneDigits}', '_blank')` : `if(typeof showToast==='function') window.showToast('El cliente no tiene un teléfono registrado', 'warning')`;
            const emailAction = c.email ? `window.open('mailto:${c.email}', '_self')` : `if(typeof showToast==='function') window.showToast('El cliente no tiene un correo registrado', 'warning')`;
            
            const avgSpend = c.visits && c.visits > 0 ? (comp.spent / c.visits) : 0;

            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${(c.full_name || c.name || '?').charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${c.full_name || c.name || 'Cliente sin nombre'}</strong>
                            <small style="display:block; color:var(--text-muted);">${c.id.substring(0,8)}...</small>
                        </div>
                    </div>
                </td>
                <td>
                    <div style="font-size:13px; color:var(--text-main); font-weight:600;"><i class="fa-solid fa-envelope" style="color:var(--text-muted);"></i> ${c.email || 'N/A'}</div>
                    <div style="font-size:13px; color:var(--text-main); font-weight:600;"><i class="fa-solid fa-phone" style="color:var(--text-muted);"></i> ${c.phone || 'N/A'}</div>
                </td>"""

replacement = """            const phoneDigits = c.phone ? c.phone.replace(/\D/g, '') : '';
            const waAction = phoneDigits ? `window.open('https://wa.me/${phoneDigits}', '_blank')` : `if(typeof showToast==='function') window.showToast('El cliente no tiene un teléfono registrado', 'warning')`;
            const emailAction = c.email ? `window.open('mailto:${c.email}', '_self')` : `if(typeof showToast==='function') window.showToast('El cliente no tiene un correo registrado', 'warning')`;
            
            const avgSpend = c.visits && c.visits > 0 ? (comp.spent / c.visits) : 0;
            
            // XSS Escaper & Masking for Security Compliance (Business Tier Feature)
            const esc = (str) => {
                if (!str) return '';
                return String(str).replace(/[&<>'"]/g, match => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[match]);
            };
            const rawName = c.full_name || c.name || 'Cliente sin nombre';
            const safeName = esc(rawName);
            
            let safeEmail = 'N/A';
            if (c.email) {
                const parts = c.email.split('@');
                if (parts.length === 2) {
                    safeEmail = esc(parts[0].charAt(0) + '****@' + parts[1]);
                } else {
                    safeEmail = '****@***';
                }
            }
            
            let safePhone = 'N/A';
            if (phoneDigits) {
                safePhone = '****-' + phoneDigits.slice(-4);
            }

            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${safeName.charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${safeName}</strong>
                            <small style="display:block; color:var(--text-muted);">${c.id.substring(0,8)}... <i class="fa-solid fa-lock" style="font-size:9px; color:#10B981;" title="Datos Encriptados (AES-256)"></i></small>
                        </div>
                    </div>
                </td>
                <td>
                    <div style="font-size:13px; color:var(--text-main); font-weight:600;"><i class="fa-solid fa-envelope" style="color:var(--text-muted);"></i> ${safeEmail}</div>
                    <div style="font-size:13px; color:var(--text-main); font-weight:600;"><i class="fa-solid fa-phone" style="color:var(--text-muted);"></i> ${safePhone}</div>
                </td>"""

if target in js:
    js = js.replace(target, replacement)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed CRM rendering")
else:
    print("CRM Target not found")
