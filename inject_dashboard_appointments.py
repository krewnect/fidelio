import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

appointments_js = """
// =====================================
// APPOINTMENTS MODULE
// =====================================

async function loadAppointments() {
    try {
        const container = document.getElementById('appointments-list-container');
        if (!container) return;
        
        container.innerHTML = '<div style="text-align:center; padding:20px; color:var(--text-muted);">Cargando citas...</div>';
        
        const { data, error } = await window.supabaseClient
            .from('appointments')
            .select('*')
            .eq('merchant_id', window.merchantSession.user.id)
            .order('appointment_date', { ascending: true });
            
        if (error) throw error;
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:var(--text-muted);"><i class="fa-solid fa-calendar-xmark" style="font-size:24px; margin-bottom:10px;"></i><br>No tienes citas agendadas.</div>';
            return;
        }
        
        let html = '';
        data.forEach(app => {
            const dateObj = new Date(app.appointment_date);
            const dateStr = dateObj.toLocaleDateString();
            const timeStr = dateObj.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            let statusBadge = '';
            let actionBtns = '';
            
            if (app.status === 'pending') {
                statusBadge = '<span style="background:var(--accent-orange); color:white; padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold;">Pendiente</span>';
                actionBtns = `
                    <button class="btn btn-outline" style="padding:6px 12px; font-size:12px; border-color:#10b981; color:#10b981;" onclick="updateAppointmentStatus('${app.id}', 'confirmed')"><i class="fa-solid fa-check"></i> Aceptar</button>
                    <button class="btn btn-primary" style="padding:6px 12px; font-size:12px; background:var(--primary); border:none;" onclick="requestAppointmentPayment('${app.id}')"><i class="fa-brands fa-stripe"></i> Solicitar Pago</button>
                `;
            } else if (app.status === 'confirmed') {
                statusBadge = '<span style="background:#10b981; color:white; padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold;">Aceptada</span>';
            } else if (app.status === 'payment_requested') {
                statusBadge = '<span style="background:var(--primary); color:white; padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold;">Pago Solicitado</span>';
            } else if (app.status === 'completed') {
                statusBadge = '<span style="background:var(--surface-light); color:var(--text-muted); padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold;">Completada</span>';
            }
            
            html += `
            <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:16px; display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; gap:15px; align-items:center;">
                    <div style="background:rgba(139,92,246,0.1); width:50px; height:50px; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:var(--primary);">
                        <span style="font-size:16px; font-weight:bold; line-height:1;">${dateObj.getDate()}</span>
                        <span style="font-size:10px; text-transform:uppercase;">${dateObj.toLocaleString('default', { month: 'short' })}</span>
                    </div>
                    <div>
                        <div style="font-weight:bold; font-size:16px; margin-bottom:4px;">${app.customer_name} ${statusBadge}</div>
                        <div style="font-size:13px; color:var(--text-muted);"><i class="fa-regular fa-clock"></i> ${timeStr} | <i class="fa-solid fa-phone"></i> ${app.customer_phone || 'Sin tel.'}</div>
                        ${app.notes ? `<div style="font-size:12px; color:var(--text-muted); margin-top:5px; background:rgba(255,255,255,0.05); padding:6px; border-radius:6px;">${app.notes}</div>` : ''}
                    </div>
                </div>
                <div style="display:flex; gap:10px; flex-direction:column; align-items:flex-end;">
                    ${actionBtns}
                </div>
            </div>`;
        });
        
        container.innerHTML = html;
    } catch (err) {
        console.error("Error cargando citas:", err);
    }
}

async function updateAppointmentStatus(id, status) {
    if (!confirm('¿Seguro que deseas aceptar esta cita?')) return;
    try {
        const res = await fetch(`/api/appointments/${id}/status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.merchantSession.access_token}`
            },
            body: JSON.stringify({ status })
        });
        const data = await res.json();
        if (data.success) {
            alert('Cita actualizada con éxito.');
            loadAppointments();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (e) {
        console.error(e);
        alert('Error de red');
    }
}

async function requestAppointmentPayment(id) {
    if (!confirm('Esto enviará una solicitud de pago al cliente con tu Link de Stripe. ¿Continuar?')) return;
    try {
        const res = await fetch(`/api/appointments/${id}/request-payment`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${window.merchantSession.access_token}`
            }
        });
        const data = await res.json();
        if (data.success) {
            alert('Pago solicitado con éxito. Estado actualizado.');
            loadAppointments();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (e) {
        console.error(e);
        alert('Error de red');
    }
}

window.updateAppointmentStatus = updateAppointmentStatus;
window.requestAppointmentPayment = requestAppointmentPayment;
"""

if "function loadAppointments" not in js:
    js = js.replace('// --- INBOX THEMES ---', appointments_js + '\n// --- INBOX THEMES ---')
    
    # Also we need to call loadAppointments when clicking the tab
    # Assuming standard tab click handling logic handles it, or we inject it into the tab logic:
    js = js.replace("if (tabId === 'tab-loyalty') {", "if (tabId === 'tab-appointments') { loadAppointments(); }\n                if (tabId === 'tab-loyalty') {")
    
    with open('dashboard.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Appointments JS injected to dashboard.js")
else:
    print("Appointments JS already exists")
