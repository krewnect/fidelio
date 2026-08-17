import re

with open('pass.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update the appointment modal
old_modal = """    <div class="modal-overlay" id="appointment-modal">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h3 style="margin:0; font-size:18px;">Agendar Cita o Servicio</h3>
                <i class="fa-solid fa-xmark" style="cursor:pointer; color:var(--text-muted);" onclick="closeAppointmentModal()"></i>
            </div>
            
            <p style="color:var(--text-muted); font-size:14px; margin-bottom:20px;">
                Selecciona la fecha y hora para tu próxima visita.
            </p>
            
            <div style="margin-bottom:15px;">
                <label style="display:block; margin-bottom:5px; font-size:14px; font-weight:600;">Fecha</label>
                <input type="date" class="form-input" style="width:100%;">
            </div>
            
            <div style="margin-bottom:20px;">
                <label style="display:block; margin-bottom:5px; font-size:14px; font-weight:600;">Hora Sugerida</label>
                <input type="time" class="form-input" style="width:100%;">
            </div>
            
            <button class="btn-wallet" style="background:var(--primary); color:white; border:none;" onclick="alert('Solicitud enviada al profesional. Te confirmarán en breve.'); closeAppointmentModal();">
                Enviar Solicitud
            </button>
        </div>
    </div>"""

new_modal = """    <div class="modal-overlay" id="appointment-modal">
        <div class="modal-content">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h3 style="margin:0; font-size:18px;">Agendar Cita o Servicio</h3>
                <i class="fa-solid fa-xmark" style="cursor:pointer; color:var(--text-muted);" onclick="closeAppointmentModal()"></i>
            </div>
            
            <p style="color:var(--text-muted); font-size:14px; margin-bottom:20px;">
                Selecciona la fecha y hora. El profesional revisará tu solicitud y te confirmará por correo/teléfono o te enviará un link de pago para asegurar tu lugar.
            </p>
            
            <div style="margin-bottom:15px;">
                <label style="display:block; margin-bottom:5px; font-size:14px; font-weight:600;">Fecha</label>
                <input type="date" id="appointment-date" class="form-input" style="width:100%;">
            </div>
            
            <div style="margin-bottom:15px;">
                <label style="display:block; margin-bottom:5px; font-size:14px; font-weight:600;">Hora Sugerida</label>
                <input type="time" id="appointment-time" class="form-input" style="width:100%;">
            </div>
            
            <div style="margin-bottom:20px;">
                <label style="display:block; margin-bottom:5px; font-size:14px; font-weight:600;">Notas Adicionales (Opcional)</label>
                <textarea id="appointment-notes" class="form-input" rows="2" style="width:100%; resize:none;" placeholder="Ej. Es mi primera consulta..."></textarea>
            </div>
            
            <button class="btn-wallet" id="btn-submit-appointment" style="background:var(--primary); color:white; border:none;" onclick="submitAppointmentRequest()">
                Enviar Solicitud
            </button>
        </div>
    </div>"""

# Ensure we replace exactly
if "Agendar Cita o Servicio" in html and "appointment-date" not in html:
    html = html.replace(old_modal, new_modal)

# Add the JS function
js_function = """
        async function submitAppointmentRequest() {
            const date = document.getElementById('appointment-date').value;
            const time = document.getElementById('appointment-time').value;
            const notes = document.getElementById('appointment-notes').value;
            
            if (!date || !time) {
                alert("Por favor selecciona fecha y hora.");
                return;
            }
            if (!customerId || !campaignId) {
                alert("No se pudo identificar al cliente.");
                return;
            }
            
            const btn = document.getElementById('btn-submit-appointment');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Enviando...';
            btn.disabled = true;
            
            try {
                const response = await fetch('/api/appointments/request', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ customer_id: customerId, campaign_id: campaignId, date, time, notes })
                });
                
                const data = await response.json();
                if (data.success) {
                    alert('¡Solicitud enviada con éxito! El profesional se pondrá en contacto pronto.');
                    closeAppointmentModal();
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (err) {
                alert('Error de red. Intenta de nuevo.');
                console.error(err);
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }
"""

if "submitAppointmentRequest" not in html:
    html = html.replace("function openAppointmentModal() {", js_function + "\n        function openAppointmentModal() {")

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("pass.html updated with Appointment Request Logic")
