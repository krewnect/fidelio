import re

with open('pass.html', 'r', encoding='utf-8') as f:
    html = f.read()

action_logic = """
                // HANDLE ACTIONS (APPOINTMENTS / PAYMENTS)
                const action = urlParams.get('action');
                if (action) {
                    document.getElementById('action-overlay').style.display = 'block';
                    const contentDiv = document.getElementById('action-content');
                    
                    // Populate Action Overlay Branding here too just in case
                    if (merchant && merchant.business_name) {
                        document.getElementById('action-merchant-name').textContent = merchant.business_name;
                    }
                    const overlayLogo = document.getElementById('action-merchant-logo');
                    if (campaign.logo_url) {
                        overlayLogo.src = campaign.logo_url;
                        overlayLogo.style.display = 'block';
                    } else if (merchant) {
                        overlayLogo.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(merchant.business_name)}&background=fff&color=000`;
                        overlayLogo.style.display = 'block';
                    }
                    if (campaign.color_primary) {
                        document.getElementById('action-header').style.background = campaign.color_primary;
                    }
                    
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
                        return; // Stop loading normal pass UI
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
                                <button type="submit" id="appt-submit-btn" style="width:100%; padding:16px; background:var(--primary, #111827); color:white; border:none; border-radius:12px; font-weight:700; font-size:16px; cursor:pointer;">
                                    Solicitar Cita
                                </button>
                            </form>
                        `;
                        
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
                                        customerId: customer.id,
                                        campaignId: campaign.id,
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

html = html.replace('let merchant = apiData.merchant;', 'let merchant = apiData.merchant;\n' + action_logic)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(html)
