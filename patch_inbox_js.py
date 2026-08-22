import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update loadInbox to calculate SLA timer
old_inbox = """        window.currentInboxTickets = filteredData;
        tbody.innerHTML = '';
        filteredData.forEach((t, index) => {
            const date = new Date(t.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric', hour:'2-digit', minute:'2-digit' });
            let statusBadge = t.status === 'abierto' ? '<span class="menu-badge" style="background:#ef4444;color:#fff;font-size:10px;">ABIERTO</span>' : '<span class="menu-badge" style="background:#10b981;color:#fff;font-size:10px;">RESUELTO</span>';
            
            tbody.innerHTML += `
                <div style="display: grid; grid-template-columns: 1fr 2fr 3fr 1fr 1fr; gap: 16px; padding: 16px; border-bottom: 1px solid var(--border-soft); align-items: center; ${t.status === 'resuelto' ? 'opacity: 0.6;' : ''}">
                    <div>
                        <div style="font-size:12px; font-family:monospace; color:var(--text-main); font-weight:700;">#${t.id.substring(0,8)}</div>
                        <div style="font-size:11px; color:var(--text-muted);">${date}</div>
                    </div>
                    <div>
                        <div style="font-weight:700; color:var(--text-main); font-size:13px;">${t.email || 'Desconocido'}</div>
                        <div style="font-size:11px; color:var(--text-muted);">${t.merchant_id || 'Visitante'}</div>
                    </div>
                    <div>
                        <div style="font-weight:700; color:var(--text-main); font-size:13px;">${t.subject}</div>
                        <div style="font-size:12px; color:var(--text-muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:250px;">${t.message}</div>
                    </div>
                    <div>${statusBadge}</div>
                    <div style="text-align: right; display:flex; justify-content:flex-end; gap:8px;">
                        <button class="fidelio-btn-secondary" style="padding:6px 10px;" onclick="viewTicketDetail(${index})" title="Ver Detalle"><i class="fa-solid fa-eye" style="color:var(--accent-violet);"></i></button>
                        ${t.status === 'abierto' ? `<button class="fidelio-btn-secondary" style="padding:6px 10px;" onclick="resolveTicket('${t.id}')" title="Marcar Resuelto"><i class="fa-solid fa-check" style="color:#10b981;"></i></button>` : ''}
                    </div>
                </div>
            `;
        });"""

new_inbox = """        window.currentInboxTickets = filteredData;
        tbody.innerHTML = '';
        
        let openCount = 0;
        
        filteredData.forEach((t, index) => {
            const date = new Date(t.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric', hour:'2-digit', minute:'2-digit' });
            let statusBadge = t.status === 'abierto' ? '<span class="menu-badge" style="background:#ef4444;color:#fff;font-size:10px;">ABIERTO</span>' : '<span class="menu-badge" style="background:#10b981;color:#fff;font-size:10px;">RESUELTO</span>';
            
            let slaBadge = '';
            if (t.status === 'abierto') {
                openCount++;
                const hoursDiff = (new Date() - new Date(t.created_at)) / (1000 * 60 * 60);
                if (hoursDiff < 24) {
                    slaBadge = `<div style="color: #10b981; font-size:10px; font-weight:800; display:flex; align-items:center; gap:4px; margin-top:6px;"><i class="fa-solid fa-clock"></i> ${Math.floor(hoursDiff)}h (Verde)</div>`;
                } else if (hoursDiff < 72) {
                    slaBadge = `<div style="color: #f59e0b; font-size:10px; font-weight:800; display:flex; align-items:center; gap:4px; margin-top:6px;"><i class="fa-solid fa-clock"></i> ${Math.floor(hoursDiff)}h (Naranja)</div>`;
                } else {
                    slaBadge = `<div style="color: #ef4444; font-size:10px; font-weight:800; display:flex; align-items:center; gap:4px; margin-top:6px;"><i class="fa-solid fa-triangle-exclamation"></i> ${Math.floor(hoursDiff)}h (CRÍTICO)</div>`;
                }
            } else {
                slaBadge = `<div style="color: #6B7280; font-size:10px; font-weight:600; display:flex; align-items:center; gap:4px; margin-top:6px;"><i class="fa-solid fa-check-double"></i> Cerrado</div>`;
            }
            
            tbody.innerHTML += `
                <div style="display: grid; grid-template-columns: 1fr 2fr 3fr 1fr 1fr; gap: 16px; padding: 16px; border-bottom: 1px solid var(--border-soft); align-items: center; ${t.status === 'resuelto' ? 'opacity: 0.6;' : ''}">
                    <div>
                        <div style="font-size:12px; font-family:monospace; color:var(--text-main); font-weight:700;">#${t.id.substring(0,8)}</div>
                        <div style="font-size:11px; color:var(--text-muted);">${date}</div>
                    </div>
                    <div>
                        <div style="font-weight:700; color:var(--text-main); font-size:13px;">${t.email || 'Desconocido'}</div>
                        <div style="font-size:11px; color:var(--text-muted);">${t.merchant_id || 'Visitante'}</div>
                    </div>
                    <div>
                        <div style="font-weight:700; color:var(--text-main); font-size:13px;">${t.subject}</div>
                        <div style="font-size:12px; color:var(--text-muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:250px;">${t.message}</div>
                    </div>
                    <div>
                        ${statusBadge}
                        ${slaBadge}
                    </div>
                    <div style="text-align: right; display:flex; justify-content:flex-end; gap:8px;">
                        <button class="fidelio-btn-secondary" style="padding:6px 10px;" onclick="viewTicketDetail(${index})" title="Ver Detalle"><i class="fa-solid fa-eye" style="color:var(--accent-violet);"></i></button>
                        ${t.status === 'abierto' ? `<button class="fidelio-btn-secondary" style="padding:6px 10px;" onclick="resolveTicket('${t.id}')" title="Marcar Resuelto"><i class="fa-solid fa-check" style="color:#10b981;"></i></button>` : ''}
                    </div>
                </div>
            `;
        });
        
        // Update sidebar badge
        const badge = document.getElementById('inbox-alert-badge');
        if (badge) {
            if (openCount > 0) {
                badge.style.display = 'inline-block';
                badge.textContent = openCount;
            } else {
                badge.style.display = 'none';
            }
        }
"""

if old_inbox in js:
    js = js.replace(old_inbox, new_inbox)
else:
    print("WARNING: Could not patch old_inbox")


# 2. Add an initialization loop for updateInboxAlert
update_func = """
    window.checkInboxAlerts = async function() {
        if (window.fidelioAdminRole !== 'admin' && window.fidelioAdminRole !== 'super_admin') return;
        const { count, error } = await window.supabaseClient.from('support_tickets').select('*', { count: 'exact', head: true }).eq('status', 'abierto');
        if (!error) {
            const badge = document.getElementById('inbox-alert-badge');
            if (badge) {
                if (count > 0) {
                    badge.style.display = 'inline-flex';
                    badge.textContent = count;
                } else {
                    badge.style.display = 'none';
                }
            }
        }
    };
    
    // Check alerts periodically
    setInterval(checkInboxAlerts, 60000); // Check every 60 seconds
    
    // Also check on load
    setTimeout(checkInboxAlerts, 3000);
"""

anchor = "window.setAdminPlanStatus = async function(status) {"
if anchor in js:
    js = js.replace(anchor, update_func + "\n    " + anchor)
else:
    print("WARNING: Could not inject update_func")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS Inbox SLA patched.")
