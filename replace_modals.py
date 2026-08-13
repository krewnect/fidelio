import re

with open('index.html', 'r') as f:
    html = f.read()

new_modals = """    <!-- ADD BRANCH MODAL (PREMIUM) -->
    <div id="modal-add-branch" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); backdrop-filter:blur(5px); z-index:9999; align-items:center; justify-content:center; font-family:var(--font-main);">
        <div style="background:white; width:500px; border-radius:24px; padding:32px; box-shadow: 0 25px 50px rgba(0,0,0,0.25); position:relative;">
            
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:24px;">
                <div>
                    <h2 style="font-size:22px; font-weight:800; color:#111827; margin-bottom:4px; letter-spacing:-0.5px;">Añadir Sucursal</h2>
                    <p style="font-size:13px; color:var(--text-muted);">Registra una nueva ubicación para la red de Apple Wallet.</p>
                </div>
                <button onclick="document.getElementById('modal-add-branch').style.display='none'" style="background:none; border:none; font-size:20px; color:#9ca3af; cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <div class="form-group">
                <label>Nombre de la Sucursal</label>
                <input type="text" id="branch-name" class="premium-input" placeholder="Ej. Centro Histórico">
            </div>
            
            <div class="form-group">
                <label>Gerente o Encargado</label>
                <input type="text" id="branch-manager" class="premium-input" placeholder="Ej. Roberto Ordóñez">
            </div>
            
            <div class="form-row-2">
                <div class="form-group">
                    <label>Teléfono</label>
                    <input type="text" id="branch-phone" class="premium-input" placeholder="Ej. 55 1234 5678">
                </div>
                <div class="form-group">
                    <label>Enlace Google Maps</label>
                    <input type="url" id="branch-maps-url" class="premium-input" placeholder="https://g.page/r/...">
                </div>
            </div>
            
            <div class="form-row-2" style="margin-bottom:8px;">
                <div class="form-group">
                    <label>Latitud (GPS)</label>
                    <input type="text" id="branch-lat" class="premium-input" placeholder="Ej. 19.4326">
                </div>
                <div class="form-group">
                    <label>Longitud (GPS)</label>
                    <input type="text" id="branch-lng" class="premium-input" placeholder="Ej. -99.1332">
                </div>
            </div>
            <p style="font-size:11px; color:#9ca3af; margin-bottom:20px; margin-top:-16px;">* Apple Wallet usará estas coordenadas para enviar una notificación cuando el cliente pase cerca.</p>
            
            <div class="form-group">
                <label>Notas de Uso Interno</label>
                <textarea id="branch-notes" class="premium-input" rows="2" placeholder="Información interna para el corporativo..."></textarea>
            </div>
            
            <button id="btn-submit-branch" class="btn btn-primary" style="width:100%; justify-content:center; padding:14px;"><i class="fa-solid fa-check"></i> Guardar Sucursal</button>
        </div>
    </div>

    <!-- UPSELL PREMIUM MODAL -->
    <div id="modal-upsell-branches" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); backdrop-filter:blur(5px); z-index:9999; align-items:center; justify-content:center; font-family:var(--font-main);">
        <div style="background:white; width:480px; border-radius:24px; padding:40px; box-shadow: 0 25px 50px rgba(0,0,0,0.25); position:relative; text-align:center;">
            <button onclick="document.getElementById('modal-upsell-branches').style.display='none'" style="position:absolute; top:20px; right:20px; background:none; border:none; font-size:20px; color:#9ca3af; cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            
            <div style="width:64px; height:64px; border-radius:16px; background:linear-gradient(135deg, #1e1b4b 0%, #8b5cf6 100%); display:flex; align-items:center; justify-content:center; color:white; font-size:28px; margin:0 auto 24px auto; box-shadow: 0 10px 20px rgba(139, 92, 246, 0.3);">
                <i class="fa-solid fa-crown"></i>
            </div>
            
            <h2 style="font-size:24px; font-weight:800; color:#111827; margin-bottom:12px; letter-spacing:-0.5px;">Desbloquea Sucursales Ilimitadas</h2>
            <p style="font-size:15px; color:var(--text-muted); margin-bottom:32px; line-height:1.5;">Has alcanzado el límite de <strong>20 sucursales activas</strong> en tu plan actual. Expande la red de tu franquicia a nivel nacional.</p>
            
            <div style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:16px; padding:20px; margin-bottom:32px; text-align:left;">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                    <i class="fa-solid fa-check text-amber" style="color:#8b5cf6;"></i>
                    <span style="font-size:14px; font-weight:600; color:#111827;">Sucursales Ilimitadas</span>
                </div>
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
                    <i class="fa-solid fa-check text-amber" style="color:#8b5cf6;"></i>
                    <span style="font-size:14px; font-weight:600; color:#111827;">Estadísticas consolidadas corporativas</span>
                </div>
                <div style="display:flex; align-items:center; gap:12px;">
                    <i class="fa-solid fa-check text-amber" style="color:#8b5cf6;"></i>
                    <span style="font-size:14px; font-weight:600; color:#111827;">Soporte Dedicado 24/7</span>
                </div>
            </div>
            
            <button class="btn btn-primary" style="width:100%; justify-content:center; padding:16px; font-size:16px; background:#635BFF; border:none; margin-bottom:12px;"><i class="fa-brands fa-stripe"></i> Pagar $99 USD / mes</button>
            <a href="mailto:hola@fidelio.com" class="btn btn-secondary" style="width:100%; justify-content:center; text-decoration:none;"><i class="fa-regular fa-envelope"></i> Contactar a Ventas</a>
        </div>
    </div>"""

pattern = r'<!-- ADD BRANCH MODAL -->.*?</div>\s*<!-- ADD CUSTOMER MODAL -->'
html = re.sub(pattern, new_modals + '\n    <!-- ADD CUSTOMER MODAL -->', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
