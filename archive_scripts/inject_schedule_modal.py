import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the button
html = html.replace(
    '''<button class="btn btn-primary" onclick="alert('Configuración de horarios disponible en breve.')" style="background: var(--bg-input);"><i class="fa-solid fa-clock"></i> Configurar Horarios</button>''',
    '''<button class="btn btn-primary" onclick="document.getElementById('schedule-config-modal').style.display='flex';" style="background: var(--accent-violet) !important; color: #fff !important; border:none;"><i class="fa-solid fa-clock"></i> Configurar Horarios</button>'''
)

# 2. Inject the modal at the end of the file, just before </body>
schedule_modal = """
    <!-- SCHEDULE CONFIG MODAL -->
    <div class="modal-overlay" id="schedule-config-modal" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); z-index:9999; align-items:center; justify-content:center; backdrop-filter:blur(5px);">
        <div class="modal-content" style="background:var(--surface); width:90%; max-width:500px; border-radius:20px; padding:32px; position:relative; box-shadow:0 25px 50px rgba(0,0,0,0.25);">
            <button onclick="document.getElementById('schedule-config-modal').style.display='none'" style="position:absolute; top:20px; right:20px; background:none; border:none; font-size:24px; color:var(--text-muted); cursor:pointer;">&times;</button>
            
            <h2 style="font-size:24px; margin-bottom:8px; color:var(--text-main);"><i class="fa-solid fa-clock" style="color:var(--accent-violet); margin-right:8px;"></i> Horarios de Atención</h2>
            <p style="color:var(--text-muted); font-size:14px; margin-bottom:24px;">Define los días y horas en los que tus clientes pueden agendar citas o servicios.</p>
            
            <div style="display:flex; flex-direction:column; gap:16px; margin-bottom:32px;">
                <!-- Mon-Fri -->
                <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:16px; border-bottom:1px solid var(--border-soft);">
                    <div style="font-weight:600; font-size:15px; width:120px;">Lunes a Viernes</div>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <input type="time" class="premium-input" value="09:00" style="padding:8px;">
                        <span>a</span>
                        <input type="time" class="premium-input" value="18:00" style="padding:8px;">
                    </div>
                </div>
                <!-- Sat -->
                <div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:16px; border-bottom:1px solid var(--border-soft);">
                    <div style="font-weight:600; font-size:15px; width:120px;">Sábados</div>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <input type="time" class="premium-input" value="10:00" style="padding:8px;">
                        <span>a</span>
                        <input type="time" class="premium-input" value="14:00" style="padding:8px;">
                    </div>
                </div>
                <!-- Sun -->
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-weight:600; font-size:15px; width:120px;">Domingos</div>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <select class="premium-input" style="padding:8px; width:100%;">
                            <option value="closed">Cerrado</option>
                            <option value="open">Abierto</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="document.getElementById('schedule-config-modal').style.display='none'; if(typeof showToast === 'function') showToast('Horarios actualizados exitosamente.', 'success');" style="width:100%; justify-content:center; background:#8b5cf6 !important; color:#fff; border:none; padding:16px; font-size:16px; font-weight:700; border-radius:12px;">Guardar Horarios</button>
        </div>
    </div>
</body>
"""

html = html.replace('</body>', schedule_modal)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Appointments modal injected.")
