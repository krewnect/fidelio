import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define the new modal HTML
merchant_modal_html = """
    <!-- MODAL CONTROL DE NEGOCIOS (SUPER ADMIN) -->
    <div id="modal-admin-merchant" class="fidelio-modal" style="display: none; align-items: center; justify-content: center; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); backdrop-filter: blur(5px); z-index: 100000; opacity: 0; transition: opacity 0.3s;">
        <div class="modal-content" style="background: #ffffff; border-radius: 24px; width: 90%; max-width: 800px; max-height: 90vh; overflow-y: auto; position: relative; transform: scale(0.95); transition: transform 0.3s; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);">
            <!-- Encabezado -->
            <div style="background: linear-gradient(135deg, var(--bg-deep) 0%, #f3e8ff 100%); padding: 32px; border-bottom: 1px solid var(--border-soft); position: relative;">
                <button onclick="closeModal('modal-admin-merchant')" style="position: absolute; top: 24px; right: 24px; background: white; border: 1px solid var(--border-soft); width: 32px; height: 32px; border-radius: 50%; cursor: pointer; color: var(--text-muted); display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-sm);"><i class="fa-solid fa-xmark"></i></button>
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div style="width: 56px; height: 56px; background: white; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 24px; color: var(--accent-violet); box-shadow: var(--shadow-sm);">
                        <i class="fa-solid fa-store"></i>
                    </div>
                    <div>
                        <div class="workspace-eyebrow" style="margin-bottom: 4px;">PANEL DE CONTROL (SUPER ADMIN)</div>
                        <h2 id="admin-merchant-name" style="margin: 0; font-size: 24px; color: var(--text-main); font-weight: 800; letter-spacing: -0.5px;">Nombre del Negocio</h2>
                        <div style="margin-top: 6px; display: flex; gap: 8px; align-items: center;">
                            <span id="admin-merchant-status" class="menu-badge" style="background: var(--accent-violet); color: white;">Trial</span>
                            <span id="admin-merchant-id" style="font-size: 11px; color: var(--text-muted); font-family: monospace; background: white; padding: 2px 6px; border-radius: 4px; border: 1px solid var(--border-glass);">ID</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Contenido Principal -->
            <div style="padding: 32px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                
                <!-- Columna Izquierda: Métricas -->
                <div style="display: flex; flex-direction: column; gap: 16px;">
                    <h3 style="font-size: 14px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;"><i class="fa-solid fa-chart-line"></i> Desempeño Operativo</h3>
                    
                    <div style="background: var(--bg-main); border: 1px solid var(--border-soft); border-radius: 16px; padding: 20px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-bottom: 4px;">Tarjetas Descargadas</div>
                            <div id="admin-merchant-passes" style="font-size: 28px; font-weight: 800; color: var(--text-main); letter-spacing: -1px;">0</div>
                        </div>
                        <div style="width: 48px; height: 48px; background: rgba(139,92,246,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--accent-violet); font-size: 20px;">
                            <i class="fa-brands fa-apple"></i>
                        </div>
                    </div>

                    <div style="background: var(--bg-main); border: 1px solid var(--border-soft); border-radius: 16px; padding: 20px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-bottom: 4px;">Escaneos Totales</div>
                            <div id="admin-merchant-scans" style="font-size: 28px; font-weight: 800; color: var(--text-main); letter-spacing: -1px;">0</div>
                        </div>
                        <div style="width: 48px; height: 48px; background: rgba(16,185,129,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #10b981; font-size: 20px;">
                            <i class="fa-solid fa-barcode"></i>
                        </div>
                    </div>
                </div>

                <!-- Columna Derecha: Gestión y Suscripción -->
                <div style="display: flex; flex-direction: column; gap: 16px;">
                    <h3 style="font-size: 14px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;"><i class="fa-solid fa-money-check-dollar"></i> Suscripción y Facturación</h3>
                    
                    <div style="background: white; border: 1px solid var(--border-soft); border-radius: 16px; padding: 20px; box-shadow: var(--shadow-sm);">
                        
                        <div style="margin-bottom: 16px;">
                            <label style="display: block; font-size: 12px; font-weight: 600; color: var(--text-muted); margin-bottom: 6px;">Precio Mensual Personalizado (MXN)</label>
                            <div style="display: flex; gap: 8px;">
                                <input type="number" id="admin-custom-price" placeholder="Ej. 990" style="flex: 1; padding: 10px 14px; border-radius: 8px; border: 1px solid var(--border-soft); background: var(--bg-input); font-family: inherit; font-size: 14px; outline: none; transition: var(--transition);">
                                <button onclick="saveAdminCustomPrice()" class="fidelio-btn-primary" style="padding: 10px 16px; border-radius: 8px;"><i class="fa-solid fa-save"></i> Guardar</button>
                            </div>
                            <small style="display: block; font-size: 11px; color: var(--text-muted); margin-top: 6px;">Si está vacío, paga el precio estándar en Stripe.</small>
                        </div>

                        <hr style="border: none; border-top: 1px solid var(--border-soft); margin: 20px 0;">

                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <button onclick="addAdminTrialDays(15)" style="width: 100%; background: rgba(59,130,246,0.1); color: #3b82f6; border: 1px solid rgba(59,130,246,0.2); padding: 12px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px;">
                                <i class="fa-solid fa-calendar-plus"></i> Extender 15 Días de Prueba
                            </button>
                            <button onclick="setAdminPlanStatus('lifetime_free')" style="width: 100%; background: rgba(139,92,246,0.1); color: var(--accent-violet); border: 1px solid rgba(139,92,246,0.2); padding: 12px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px;">
                                <i class="fa-solid fa-gift"></i> Otorgar Cuenta Gratis (Lifetime)
                            </button>
                            <button onclick="setAdminPlanStatus('active')" style="width: 100%; background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.2); padding: 12px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px;">
                                <i class="fa-solid fa-check-double"></i> Forzar Cuenta Activa (Pagada)
                            </button>
                            <button onclick="setAdminPlanStatus('expired')" style="width: 100%; background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); padding: 12px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 8px;">
                                <i class="fa-solid fa-lock"></i> Bloquear Acceso (Expirado)
                            </button>
                        </div>
                    </div>

                </div>
            </div>
            
            <input type="hidden" id="admin-current-merchant-id">
        </div>
    </div>
"""

# Insert modal at the end of the body just before scripts
anchor = "<!-- SCRIPTS -->"
if anchor in html:
    html = html.replace(anchor, merchant_modal_html + "\n    " + anchor)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Modal injected into index.html")
else:
    print("Could not find anchor in index.html")

