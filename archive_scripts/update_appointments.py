import re

# --- 1. Update index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_nav = '<button class="nav-tab plan-professional-only" data-tab="tab-appointments" id="nav-appointments"><i class="fa-solid fa-calendar-check"></i> Citas/Servicios</button>'
replacement_nav = '<button class="nav-tab plan-professional-only" data-tab="tab-appointments" id="nav-appointments"><i class="fa-solid fa-calendar-check"></i> Citas/Servicios <span class="menu-badge" id="appointments-count-badge" style="background:#ef4444; color:white; margin-left:8px; display:none;">0</span></button>'

if target_nav in html:
    html = html.replace(target_nav, replacement_nav)
else:
    print("WARNING: nav-appointments not found exactly in index.html")
    # try regex
    html = re.sub(r'(<button[^>]*id="nav-appointments"[^>]*>.*?Citas/Servicios)(</button>)', r'\1 <span class="menu-badge" id="appointments-count-badge" style="background:#ef4444; color:white; margin-left:8px; display:none;">0</span>\2', html)

# Bump cache buster for html
html = re.sub(r'src="dashboard\.js\?v=\d+"', 'src="dashboard.js?v=' + str(__import__('time').time()) + '"', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# --- 2. Update dashboard.js ---
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()


# A) Inject DB save into saveComplexSchedule
target_schedule = """        // Update UI Summary safely
        try {
            window.renderScheduleSummary();
        } catch (sumErr) {"""
replacement_schedule = """        // Update DB
        if (targetState.tenantId && window.supabaseClient) {
            let prefs = {};
            try { prefs = window.merchantData.appointment_settings.landing_prefs || {}; } catch(e){}
            let processed = [];
            try { processed = window.merchantData.appointment_settings.processed_appointments || []; } catch(e){}
            
            const newSettings = {
                schedules: targetState.schedules,
                landing_prefs: prefs,
                processed_appointments: processed
            };
            
            if (!window.merchantData) window.merchantData = {};
            window.merchantData.appointment_settings = newSettings;
            
            window.supabaseClient.from('merchants').update({
                appointment_settings: newSettings
            }).eq('id', targetState.tenantId).then(({error}) => {
                if (error) console.error("Error saving schedules to DB", error);
                else {
                    if (typeof showToast === 'function') showToast('Horarios guardados en la nube', 'success');
                }
            });
        }

        // Update UI Summary safely
        try {
            window.renderScheduleSummary();
        } catch (sumErr) {"""
js = js.replace(target_schedule, replacement_schedule)


# B) Update Dashboard Metrics
target_metrics = """        const scansToday = state.transactions.filter(t => new Date(t.created_at) >= yesterday).length;
        document.getElementById('metric-scans').textContent = scansToday;
    }"""
replacement_metrics = """        const scansToday = state.transactions.filter(t => new Date(t.created_at) >= yesterday).length;
        document.getElementById('metric-scans').textContent = scansToday;
        
        // Citas Pendientes
        let processed = [];
        try { processed = window.merchantData.appointment_settings.processed_appointments || []; } catch(e){}
        const pendingCitas = state.transactions.filter(t => t.transaction_type === 'appointment_request' && !processed.includes(t.id)).length;
        const apptBadge = document.getElementById('appointments-count-badge');
        if (apptBadge) {
            if (pendingCitas > 0) {
                apptBadge.style.display = 'inline-block';
                apptBadge.textContent = pendingCitas;
            } else {
                apptBadge.style.display = 'none';
            }
        }
    }"""
js = js.replace(target_metrics, replacement_metrics)


# C) Replace loadAppointments to use DB state and add markAppt logic
target_appt_func_start = "window.loadAppointments = function() {"
if target_appt_func_start in js:
    # Completely replace the end of file where I appended it
    js = re.sub(r'window\.loadAppointments = function\(\) \{.*$', '', js, flags=re.DOTALL)
else:
    pass # It might not be at the end, but I literally appended it in the last script

new_appt_logic = """
window.markAppointmentProcessed = async function(id, waLink) {
    if (!window.merchantData) return;
    if (!window.merchantData.appointment_settings) window.merchantData.appointment_settings = {};
    if (!window.merchantData.appointment_settings.processed_appointments) window.merchantData.appointment_settings.processed_appointments = [];
    
    if (!window.merchantData.appointment_settings.processed_appointments.includes(id)) {
        window.merchantData.appointment_settings.processed_appointments.push(id);
        
        // Guardar en Supabase
        if (window.supabaseClient) {
            window.supabaseClient.from('merchants').update({
                appointment_settings: window.merchantData.appointment_settings
            }).eq('id', window.merchantData.id).then(({error}) => {
                if (error) console.error("Error marking processed", error);
            });
        }
    }
    
    // Refresh UI
    if (typeof window.updateDashboardMetrics === 'function') window.updateDashboardMetrics();
    if (typeof window.loadAppointments === 'function') window.loadAppointments();
    
    // Abrir WhatsApp
    if (waLink && waLink !== '#') {
        window.open(waLink, '_blank');
    }
};

window.loadAppointments = function() {
    const container = document.getElementById('appointments-list-container');
    if (!container) return;

    if (!state.transactions) {
        container.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 20px;">Cargando citas...</p>';
        return;
    }

    let processed = [];
    try { processed = window.merchantData.appointment_settings.processed_appointments || []; } catch(e){}

    const appts = state.transactions
        .filter(t => t.transaction_type === 'appointment_request')
        .sort((a,b) => new Date(b.created_at) - new Date(a.created_at));

    if (appts.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 20px;"><i class="fa-solid fa-calendar-day"></i> Aún no tienes citas agendadas.</p>';
        return;
    }

    // Try to get payment link from the first campaign if exists
    let stripeLink = "";
    if (state.campaigns && state.campaigns.length > 0) {
        const rules = state.campaigns[0].rules_config || {};
        stripeLink = rules.payment_url || state.campaigns[0].custom_cta_url || "";
    }

    container.innerHTML = appts.map(t => {
        let details = {};
        try { details = JSON.parse(t.notes || "{}"); } catch(e){}
        const cust = state.customers.find(c => c.id === t.customer_id) || {};
        
        const dateRaw = details.date || 'Sin fecha';
        const timeRaw = details.time || 'Sin hora';
        const serviceNotes = details.notes || 'Ninguna';
        const name = cust.full_name || cust.name || 'Cliente Desconocido';
        const phone = cust.phone || '';
        
        let msg = `Hola ${name}, he recibido tu solicitud de cita para el día ${dateRaw} a las ${timeRaw}. Para confirmar tu lugar, por favor realiza el pago o anticipo aquí: ${stripeLink}`;
        const waLink = phone ? `https://wa.me/${phone.replace(/\\D/g,'')}?text=${encodeURIComponent(msg)}` : '#';
        
        const isProcessed = processed.includes(t.id);
        const badgeHtml = isProcessed 
            ? `<span style="background:#f3f4f6; color:#4b5563; font-size:11px; font-weight:700; padding:4px 8px; border-radius:12px;"><i class="fa-solid fa-check"></i> CONTACTADO</span>`
            : `<span style="background:#dbeafe; color:#1d4ed8; font-size:11px; font-weight:700; padding:4px 8px; border-radius:12px;">NUEVA SOLICITUD</span>`;

        return `
            <div style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:16px; display:flex; flex-direction:column; gap:12px; box-shadow:0 2px 5px rgba(0,0,0,0.02); opacity: ${isProcessed ? '0.7' : '1'};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <h3 style="margin:0 0 4px 0; font-size:16px; color:#111827;">${name}</h3>
                        <p style="margin:0; font-size:13px; color:#6b7280;"><i class="fa-solid fa-calendar-day"></i> ${dateRaw} a las ${timeRaw}</p>
                    </div>
                    ${badgeHtml}
                </div>
                <div style="background:#f9fafb; padding:12px; border-radius:8px; font-size:13px; color:#374151;">
                    <strong>Notas:</strong> ${serviceNotes}
                </div>
                <div style="display:flex; gap:8px; margin-top:4px;">
                    ${phone 
                        ? `<button onclick="markAppointmentProcessed('${t.id}', '${waLink}')" style="cursor:pointer; border:none; flex:1; text-align:center; background:#10b981; color:white; padding:10px; border-radius:8px; font-weight:600; font-size:14px;"><i class="fa-brands fa-whatsapp"></i> Confirmar y Cobrar</button>` 
                        : `<span style="flex:1; text-align:center; background:#f3f4f6; color:#9ca3af; padding:10px; border-radius:8px; font-size:14px;"><i class="fa-solid fa-phone-slash"></i> Sin teléfono</span>`}
                </div>
            </div>
        `;
    }).join('');
};
"""
js += new_appt_logic

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Done updating")
