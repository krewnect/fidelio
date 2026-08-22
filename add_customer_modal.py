import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

modal_html = """
    <!-- CUSTOMER PROFILE MODAL -->
    <div id="modal-customer-profile" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); backdrop-filter:blur(5px); z-index:9999; align-items:center; justify-content:center; font-family:var(--font-main);">
        <div style="background:#ffffff; width:95%; max-width:550px; max-height:85vh; border-radius:20px; padding:0; position:relative; box-shadow:0 25px 50px -12px rgba(0,0,0,0.3); display:flex; flex-direction:column; overflow:hidden;">
            <!-- Header -->
            <div style="background:var(--bg-main); padding:24px; border-bottom:1px solid #e5e7eb; display:flex; justify-content:space-between; align-items:flex-start;">
                <div style="display:flex; align-items:center; gap:16px;">
                    <div id="cp-avatar" style="width:60px; height:60px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:800;"></div>
                    <div>
                        <h2 id="cp-name" style="margin:0; font-size:22px; font-weight:800; color:#111827;">Nombre del Cliente</h2>
                        <div id="cp-id" style="color:var(--text-muted); font-size:13px; font-family:monospace; margin-top:4px;">ID</div>
                    </div>
                </div>
                <button onclick="document.getElementById('modal-customer-profile').style.display='none'" style="background:#f3f4f6; border:none; width:36px; height:36px; border-radius:50%; color:#4b5563; cursor:pointer;"><i class="fa-solid fa-times"></i></button>
            </div>
            
            <!-- Body -->
            <div style="padding:24px; overflow-y:auto; flex:1; background:#f9fafb;">
                <!-- KPIs -->
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:24px;">
                    <div style="background:#ffffff; padding:16px; border-radius:12px; border:1px solid #e5e7eb; display:flex; flex-direction:column; gap:4px;">
                        <span style="color:var(--text-muted); font-size:12px; font-weight:700; text-transform:uppercase;">Nivel Actual</span>
                        <span id="cp-tier" style="font-size:16px; font-weight:800;">-</span>
                    </div>
                    <div style="background:#ffffff; padding:16px; border-radius:12px; border:1px solid #e5e7eb; display:flex; flex-direction:column; gap:4px;">
                        <span style="color:var(--text-muted); font-size:12px; font-weight:700; text-transform:uppercase;">Monedero (Cash)</span>
                        <span id="cp-balance" style="font-size:18px; font-weight:800; color:#10b981;">$0.00 MXN</span>
                    </div>
                    <div style="background:#ffffff; padding:16px; border-radius:12px; border:1px solid #e5e7eb; display:flex; flex-direction:column; gap:4px;">
                        <span style="color:var(--text-muted); font-size:12px; font-weight:700; text-transform:uppercase;">Total Gastado (LTV)</span>
                        <span id="cp-spent" style="font-size:18px; font-weight:800;">$0.00 MXN</span>
                    </div>
                    <div style="background:#ffffff; padding:16px; border-radius:12px; border:1px solid #e5e7eb; display:flex; flex-direction:column; gap:4px;">
                        <span style="color:var(--text-muted); font-size:12px; font-weight:700; text-transform:uppercase;">Visitas Registradas</span>
                        <span id="cp-visits" style="font-size:18px; font-weight:800; color:var(--accent-violet);">0 Visitas</span>
                    </div>
                </div>

                <!-- Detalles Personales -->
                <h3 style="font-size:14px; font-weight:800; color:#111827; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;">Información de Contacto</h3>
                <div style="background:#ffffff; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden; margin-bottom:24px;">
                    <div style="padding:12px 16px; border-bottom:1px solid #e5e7eb; display:flex; justify-content:space-between;">
                        <span style="color:var(--text-muted); font-size:13px;"><i class="fa-solid fa-phone" style="width:20px;"></i> Teléfono</span>
                        <strong id="cp-phone" style="font-size:13px; color:#111827;">-</strong>
                    </div>
                    <div style="padding:12px 16px; border-bottom:1px solid #e5e7eb; display:flex; justify-content:space-between;">
                        <span style="color:var(--text-muted); font-size:13px;"><i class="fa-solid fa-envelope" style="width:20px;"></i> Correo Electrónico</span>
                        <strong id="cp-email" style="font-size:13px; color:#111827;">-</strong>
                    </div>
                    <div style="padding:12px 16px; display:flex; justify-content:space-between;">
                        <span style="color:var(--text-muted); font-size:13px;"><i class="fa-solid fa-cake-candles" style="width:20px;"></i> Cumpleaños</span>
                        <strong id="cp-bday" style="font-size:13px; color:#111827;">-</strong>
                    </div>
                </div>

                <!-- Actividad -->
                <h3 style="font-size:14px; font-weight:800; color:#111827; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;">Actividad y Frecuencia</h3>
                <div style="background:#ffffff; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden;">
                    <div style="padding:12px 16px; border-bottom:1px solid #e5e7eb; display:flex; justify-content:space-between;">
                        <span style="color:var(--text-muted); font-size:13px;"><i class="fa-solid fa-calendar-plus" style="width:20px;"></i> Registro inicial</span>
                        <strong id="cp-anniv" style="font-size:13px; color:#111827;">-</strong>
                    </div>
                    <div style="padding:12px 16px; border-bottom:1px solid #e5e7eb; display:flex; justify-content:space-between;">
                        <span style="color:var(--text-muted); font-size:13px;"><i class="fa-solid fa-clock-rotate-left" style="width:20px;"></i> Última visita</span>
                        <strong id="cp-last-visit" style="font-size:13px; color:#111827;">-</strong>
                    </div>
                    <div style="padding:12px 16px; display:flex; justify-content:space-between;">
                        <span style="color:var(--text-muted); font-size:13px;"><i class="fa-solid fa-wave-square" style="width:20px;"></i> Estado</span>
                        <div id="cp-status" style="font-size:13px;">-</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

html = html.replace('<!-- ADD CUSTOMER MODAL -->', modal_html + '\n    <!-- ADD CUSTOMER MODAL -->')

# Cache bust
html = re.sub(r'src="dashboard\.js\?v=\d+"', 'src="dashboard.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
