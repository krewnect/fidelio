import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the button
old_btn = '<button class="btn btn-primary" style="width:100%; justify-content:center; padding:16px; font-size:16px; border-radius:12px; background:#111827; border:none; color:white; font-weight:700;"><i class="fa-solid fa-cloud-arrow-up"></i> Guardar Diseño</button>'
new_btn = '<button id="btn-save-design-push" class="btn btn-primary" style="width:100%; justify-content:center; padding:16px; font-size:16px; border-radius:12px; background:#111827; border:none; color:white; font-weight:700;"><i class="fa-solid fa-cloud-arrow-up"></i> Guardar y Actualizar Tarjetas</button>'
html = html.replace(old_btn, new_btn)

# 2. Add Modal HTML before </body>
modal_html = """
    <!-- OVER-THE-AIR PUSH MODAL -->
    <div id="push-update-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); backdrop-filter:blur(5px); z-index:9999; align-items:center; justify-content:center; font-family:var(--font-main);">
        <div style="background:white; width:480px; border-radius:24px; padding:32px; box-shadow: 0 25px 50px rgba(0,0,0,0.25); position:relative; overflow:hidden;">
            
            <div id="push-modal-step-1">
                <div style="width:50px; height:50px; border-radius:50%; background:rgba(139, 92, 246, 0.1); display:flex; align-items:center; justify-content:center; color:var(--accent-violet); font-size:20px; margin-bottom:20px;">
                    <i class="fa-solid fa-tower-broadcast"></i>
                </div>
                <h2 style="font-size:22px; font-weight:800; color:#111827; margin-bottom:8px; letter-spacing:-0.5px;">Actualización Over-the-Air</h2>
                <p style="font-size:14px; color:#6b7280; margin-bottom:24px; line-height:1.5;">Tienes <strong>1,428 tarjetas activas</strong> instaladas en los dispositivos de tus clientes. ¿Deseas aplicar estos cambios de diseño a todas ellas inmediatamente?</p>
                
                <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:32px;">
                    <label style="display:flex; align-items:flex-start; gap:12px; padding:16px; border:1px solid #e5e7eb; border-radius:12px; cursor:pointer; transition:var(--transition);" class="hover-border-violet">
                        <input type="radio" name="push_type" value="silent" checked style="margin-top:4px;">
                        <div>
                            <strong style="display:block; font-size:14px; color:#111827; margin-bottom:2px;">Actualización Silenciosa</strong>
                            <span style="font-size:12px; color:#6b7280;">El diseño se actualizará en segundo plano sin molestar al usuario.</span>
                        </div>
                    </label>
                    <label style="display:flex; align-items:flex-start; gap:12px; padding:16px; border:1px solid #e5e7eb; border-radius:12px; cursor:pointer; transition:var(--transition);" class="hover-border-violet">
                        <input type="radio" name="push_type" value="notify" style="margin-top:4px;">
                        <div>
                            <strong style="display:block; font-size:14px; color:#111827; margin-bottom:2px;">Notificación de Pantalla de Bloqueo</strong>
                            <span style="font-size:12px; color:#6b7280;">El teléfono vibrará mostrando: "El diseño de tu tarjeta ha sido actualizado".</span>
                        </div>
                    </label>
                </div>
                
                <div style="display:flex; gap:12px; justify-content:flex-end;">
                    <button id="btn-cancel-push" class="btn btn-secondary" style="padding:10px 20px;">Cancelar</button>
                    <button id="btn-confirm-push" class="btn btn-primary" style="background:#111827; padding:10px 20px;"><i class="fa-brands fa-apple"></i> <i class="fa-brands fa-google"></i> Sincronizar Ahora</button>
                </div>
            </div>
            
            <div id="push-modal-step-2" style="display:none; text-align:center; padding:20px 0;">
                <div style="width:64px; height:64px; margin:0 auto 20px auto; position:relative;">
                    <div style="position:absolute; width:100%; height:100%; border:4px solid #f3f4f6; border-radius:50%;"></div>
                    <div style="position:absolute; width:100%; height:100%; border:4px solid var(--accent-violet); border-radius:50%; border-top-color:transparent; animation:spin 1s linear infinite;"></div>
                </div>
                <h2 style="font-size:20px; font-weight:700; color:#111827; margin-bottom:8px;">Contactando a APNs y Google...</h2>
                <p style="font-size:13px; color:#6b7280; margin-bottom:16px;">Sincronizando diseño con los teléfonos de los clientes.</p>
                <div style="width:100%; height:6px; background:#f3f4f6; border-radius:3px; overflow:hidden;">
                    <div id="push-progress-bar" style="width:0%; height:100%; background:var(--accent-violet); transition:width 0.2s;"></div>
                </div>
                <div id="push-progress-text" style="font-size:11px; font-weight:700; color:#9ca3af; margin-top:8px; text-transform:uppercase; letter-spacing:1px;">0 / 1,428</div>
            </div>
            
            <div id="push-modal-step-3" style="display:none; text-align:center; padding:20px 0;">
                <div style="width:64px; height:64px; border-radius:50%; background:#10B981; color:white; display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 20px auto;">
                    <i class="fa-solid fa-check"></i>
                </div>
                <h2 style="font-size:22px; font-weight:800; color:#111827; margin-bottom:8px; letter-spacing:-0.5px;">¡Tarjetas Actualizadas!</h2>
                <p style="font-size:14px; color:#6b7280; margin-bottom:24px;">Todas las tarjetas han recibido el nuevo diseño exitosamente a través de Over-the-Air (OTA).</p>
                <button id="btn-close-push" class="btn btn-primary" style="width:100%; justify-content:center; background:#111827;">Entendido</button>
            </div>
            
            <style>
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                .hover-border-violet:hover { border-color:var(--accent-violet) !important; background:rgba(139, 92, 246, 0.02); }
            </style>
        </div>
    </div>
</body>"""

html = html.replace('</body>', modal_html)

with open('index.html', 'w') as f:
    f.write(html)
