import re

with open('pass.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add a full screen overlay for appointments / messages
overlay_html = """
    <!-- FULL SCREEN ACTION OVERLAY -->
    <div id="action-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; padding:24px; overflow-y:auto; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="max-width:400px; margin:0 auto; padding-top:40px;">
            <button onclick="window.history.back()" style="background:none; border:none; font-size:24px; margin-bottom:20px; cursor:pointer;"><i class="fa-solid fa-arrow-left"></i></button>
            <h1 id="action-title" style="font-size:24px; font-weight:800; margin-bottom:8px; color:#111827;">Agendar Cita</h1>
            <p id="action-subtitle" style="font-size:14px; color:#6b7280; margin-bottom:24px;">Selecciona la fecha y hora para tu cita.</p>
            
            <div id="action-content">
                <!-- content injected by JS -->
            </div>
        </div>
    </div>
"""

if "<!-- FULL SCREEN ACTION OVERLAY -->" not in html:
    html = html.replace('<body>', '<body>\n' + overlay_html)

# Inject the JS logic
js_logic = """
            // HANDLE ACTIONS (APPOINTMENTS / PAYMENTS)
            const urlParams = new URLSearchParams(window.location.search);
            const action = urlParams.get('action');
            
            if (action) {
                document.getElementById('action-overlay').style.display = 'block';
                const contentDiv = document.getElementById('action-content');
                
                if (action === 'payment') {
                    document.getElementById('action-title').textContent = 'Procesando Pago...';
                    document.getElementById('action-subtitle').textContent = 'Serás redirigido a la pasarela de pago seguro en un momento.';
                    contentDiv.innerHTML = '<div style="text-align:center; padding:40px;"><i class="fa-solid fa-spinner fa-spin" style="font-size:40px; color:#cbd5e1;"></i></div>';
                    
                    setTimeout(() => {
                        let payUrl = null;
                        if (campaign.rules_config && campaign.rules_config.payment_url) {
                            payUrl = campaign.rules_config.payment_url;
                        } else if (campaign.stripe_payment_link) {
                            payUrl = campaign.stripe_payment_link;
                        } else if (campaign.custom_cta_url) {
                            payUrl = campaign.custom_cta_url;
                        }
                        
                        if (payUrl && (payUrl.startsWith('http://') || payUrl.startsWith('https://'))) {
                            window.location.href = payUrl;
                        } else {
                            contentDiv.innerHTML = '<div style="padding:20px; background:#fef2f2; color:#b91c1c; border-radius:12px; font-size:14px;"><i class="fa-solid fa-triangle-exclamation"></i> El comercio aún no ha configurado su enlace de pago. Por favor contáctalos directamente.</div>';
                            document.getElementById('action-title').textContent = 'Enlace no disponible';
                            document.getElementById('action-subtitle').textContent = '';
                        }
                    }, 1500);
                    return; // Stop loading the rest of the pass UI
                }
                
                if (action === 'appointment') {
                    document.getElementById('action-title').textContent = 'Agendar Cita';
                    contentDiv.innerHTML = `
                        <form id="appointment-form" onsubmit="submitAppointment(event)">
                            <div style="margin-bottom:16px;">
                                <label style="display:block; font-size:12px; font-weight:700; color:#374151; margin-bottom:6px;">FECHA DESEADA</label>
                                <input type="date" id="appt-date" required style="width:100%; padding:12px; border:1px solid #d1d5db; border-radius:8px; font-size:16px;">
                            </div>
                            <div style="margin-bottom:24px;">
                                <label style="display:block; font-size:12px; font-weight:700; color:#374151; margin-bottom:6px;">HORA DESEADA</label>
                                <input type="time" id="appt-time" required style="width:100%; padding:12px; border:1px solid #d1d5db; border-radius:8px; font-size:16px;">
                            </div>
                            <div style="margin-bottom:24px;">
                                <label style="display:block; font-size:12px; font-weight:700; color:#374151; margin-bottom:6px;">NOTAS O SERVICIO REQUERIDO</label>
                                <textarea id="appt-notes" rows="3" placeholder="Ej. Corte de cabello, Revisión dental..." style="width:100%; padding:12px; border:1px solid #d1d5db; border-radius:8px; font-size:16px; resize:none;"></textarea>
                            </div>
                            <button type="submit" id="appt-submit-btn" style="width:100%; padding:16px; background:#111827; color:white; border:none; border-radius:12px; font-weight:700; font-size:16px; cursor:pointer;">
                                Solicitar Cita
                            </button>
                        </form>
                    `;
                    
                    // Attach submit handler globally
                    window.submitAppointment = async function(e) {
                        e.preventDefault();
                        const btn = document.getElementById('appt-submit-btn');
                        btn.disabled = true;
                        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Enviando...';
                        
                        try {
                            const date = document.getElementById('appt-date').value;
                            const time = document.getElementById('appt-time').value;
                            const notes = document.getElementById('appt-notes').value;
                            
                            const res = await fetch('/api/appointments', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({
                                    customerId: customerId,
                                    campaignId: campaignId,
                                    date: date,
                                    time: time,
                                    notes: notes
                                })
                            });
                            
                            const data = await res.json();
                            if (data.success) {
                                document.getElementById('action-content').innerHTML = `
                                    <div style="text-align:center; padding:40px 20px;">
                                        <i class="fa-solid fa-circle-check" style="font-size:64px; color:#10b981; margin-bottom:16px;"></i>
                                        <h2 style="font-size:20px; font-weight:800; color:#111827; margin-bottom:8px;">¡Solicitud Enviada!</h2>
                                        <p style="font-size:14px; color:#4b5563;">Tu solicitud de cita ha sido recibida. El comercio se pondrá en contacto contigo para confirmarla.</p>
                                    </div>
                                `;
                            } else {
                                alert('Hubo un error al enviar tu solicitud: ' + data.error);
                                btn.disabled = false;
                                btn.innerHTML = 'Solicitar Cita';
                            }
                        } catch (err) {
                            alert('Error de conexión.');
                            btn.disabled = false;
                            btn.innerHTML = 'Solicitar Cita';
                        }
                    };
                    return; // Stop loading normal pass UI
                }
            }
"""

if "// HANDLE ACTIONS (APPOINTMENTS / PAYMENTS)" not in html:
    html = html.replace('document.getElementById("pass-container").style.display = "block";', js_logic + '\n                document.getElementById("pass-container").style.display = "block";')

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(html)
