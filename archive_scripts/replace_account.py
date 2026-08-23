with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# We will find the exact boundaries using string finding.
start_str = "<!-- ACCOUNT SETTINGS TAB -->"
end_str = "<!-- SOPORTE TAB -->"

start_idx = html.find(start_str)
end_idx = html.find(end_str)

new_html = """<!-- ACCOUNT SETTINGS TAB -->
            <section id="tab-account" class="tab-content">
                <div class="workspace-header" style="margin-bottom: 40px; border-bottom: 1px solid var(--surface-light); padding-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                        <div>
                            <span class="workspace-eyebrow" style="color:var(--accent-violet); letter-spacing: 1px;">PREFERENCES & SETTINGS</span>
                            <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 8px;">Mi Cuenta</h1>
                            <p style="color: var(--text-muted); font-size: 15px;">Administra tu perfil, marca y preferencias de negocio.</p>
                        </div>
                    </div>
                </div>
                
                <div style="max-width: 950px; display: grid; grid-template-columns: 280px 1fr; gap: 40px; margin-bottom: 60px;">
                    
                    <!-- Left Column: Navigation / Summary -->
                    <div style="display: flex; flex-direction: column; gap: 24px;">
                        <div class="premium-card" style="background: var(--surface); border-radius: 20px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid var(--border-soft); text-align: center;">
                            <div style="position:relative; width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 16px; background: linear-gradient(135deg, var(--accent-violet), #c084fc); display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 800; color: white; box-shadow: 0 8px 16px rgba(139, 92, 246, 0.2);">
                                <span id="acc-avatar-letter">N</span>
                                <div style="position:absolute; bottom: 0; right: 0; background: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; color: var(--accent-violet); font-size: 14px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                                    <i class="fa-solid fa-camera"></i>
                                </div>
                            </div>
                            <h3 id="acc-summary-name" style="font-size: 18px; font-weight: 800; margin-bottom: 4px; color: var(--text-main);">Tu Negocio</h3>
                            <p id="acc-summary-tier" style="font-size: 13px; color: var(--fidelio-violet); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Plan Profesional</p>
                        </div>

                        <div style="background: transparent;">
                            <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
                                <li><a href="#section-profile" style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 12px; color: var(--text-main); text-decoration: none; font-weight: 600; background: var(--surface); box-shadow: 0 2px 4px rgba(0,0,0,0.02);"><i class="fa-solid fa-address-card" style="color: var(--accent-violet); width: 20px;"></i> Perfil Público</a></li>
                                <li><a href="#section-portal" style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 12px; color: var(--text-muted); text-decoration: none; font-weight: 600; transition: all 0.2s;"><i class="fa-solid fa-paintbrush" style="width: 20px;"></i> Branding del Portal</a></li>
                                <li><a href="#section-security" style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 12px; color: var(--text-muted); text-decoration: none; font-weight: 600; transition: all 0.2s;"><i class="fa-solid fa-shield-halved" style="width: 20px;"></i> Seguridad y Acceso</a></li>
                                <li><a href="#section-notifications" style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 12px; color: var(--text-muted); text-decoration: none; font-weight: 600; transition: all 0.2s;"><i class="fa-solid fa-bell" style="width: 20px;"></i> Notificaciones</a></li>
                            </ul>
                        </div>
                    </div>

                    <!-- Right Column: Settings Sections -->
                    <div style="display: flex; flex-direction: column; gap: 32px;">
                        
                        <!-- Perfil Público -->
                        <div id="section-profile" class="premium-card" style="background: var(--surface); border-radius: 20px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid var(--border-soft);">
                            <div style="margin-bottom: 24px;">
                                <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">Perfil Público</h3>
                                <p style="font-size: 13px; color: var(--text-muted);">Esta información será visible para tus clientes en el menú de la aplicación y tarjetas de Wallet.</p>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                <div class="form-group" style="grid-column: 1 / -1;">
                                    <label style="display:block; margin-bottom:8px; font-weight:600; font-size:13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">Nombre de tu Negocio / Marca</label>
                                    <input type="text" id="acc-business-name" class="fidelio-input" placeholder="Ej: Dr. Juan Pérez, Studio Beauty..." style="font-size: 15px; padding: 14px 16px; border-radius: 12px;">
                                </div>
                                <div class="form-group" style="grid-column: 1 / -1;">
                                    <label style="display:block; margin-bottom:8px; font-weight:600; font-size:13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">Giro Comercial o Profesión</label>
                                    <input type="text" id="acc-business-category" class="fidelio-input" placeholder="Ej: Dentista, Estilista, Barbería..." style="font-size: 15px; padding: 14px 16px; border-radius: 12px;">
                                </div>
                            </div>
                            <div style="margin-top: 24px; text-align: right; border-top: 1px solid var(--border-soft); padding-top: 24px;">
                                <button id="btn-save-acc-profile" class="btn btn-primary" style="background: linear-gradient(135deg, var(--accent-violet), #c084fc); border: none; padding: 12px 24px; font-weight: 600; border-radius: 12px; box-shadow: 0 4px 12px rgba(139,92,246,0.3);"><i class="fa-solid fa-check"></i> Guardar Perfil</button>
                            </div>
                        </div>

                        <!-- Branding del Portal -->
                        <div id="section-portal" class="premium-card" style="background: var(--surface); border-radius: 20px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid var(--border-soft);">
                            <div style="margin-bottom: 24px;">
                                <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">Branding y Captación</h3>
                                <p style="font-size: 13px; color: var(--text-muted);">Personaliza cómo luce tu portal público de registro y los datos que le pides a nuevos clientes.</p>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px;">
                                <div style="background: var(--bg-main); padding: 20px; border-radius: 16px; border: 1px solid var(--border-soft);">
                                    <label style="display:block; margin-bottom:12px; font-weight:700; font-size:13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">Color Primario (Botones)</label>
                                    <div style="display:flex; align-items:center; gap: 12px;">
                                        <input type="color" id="portal-color-primary" class="fidelio-input" value="#8b5cf6" style="padding: 0; width: 48px; height: 48px; cursor: pointer; border-radius: 8px; border: none;">
                                        <span style="font-size: 13px; color: var(--text-muted); font-family: monospace; font-weight: 600;">#8b5cf6</span>
                                    </div>
                                </div>
                                <div style="background: var(--bg-main); padding: 20px; border-radius: 16px; border: 1px solid var(--border-soft);">
                                    <label style="display:block; margin-bottom:12px; font-weight:700; font-size:13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">Logotipo del Negocio</label>
                                    <input type="file" id="portal-logo-upload" accept="image/*" style="font-size: 12px; width: 100%;">
                                    <div id="portal-logo-preview" style="margin-top: 16px; display: none; align-items:center; gap:12px; background: white; padding: 8px; border-radius: 12px; border: 1px solid var(--border-soft);">
                                        <img src="" id="portal-logo-img" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                                        <span style="font-size:12px; font-weight: 700; color: #10b981;"><i class="fa-solid fa-circle-check"></i> Activo</span>
                                    </div>
                                </div>
                            </div>
                            
                            <h4 style="font-size: 13px; font-weight: 700; margin-bottom: 16px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">Campos de Registro</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                                <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px; background: var(--bg-main); border-radius: 12px; border: 1px solid var(--border-soft);">
                                    <div style="display:flex; align-items:center; gap:12px;">
                                        <div style="width:32px; height:32px; border-radius:8px; background:white; display:flex; align-items:center; justify-content:center; color:var(--text-muted); box-shadow:0 2px 4px rgba(0,0,0,0.05);"><i class="fa-solid fa-user"></i></div>
                                        <div style="font-weight: 600; font-size: 14px; color: var(--text-main);">Nombre</div>
                                    </div>
                                    <div style="font-size: 10px; font-weight: 800; color: #10b981; background: rgba(16,185,129,0.1); padding: 4px 8px; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Fijo</div>
                                </div>
                                <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px; background: var(--bg-main); border-radius: 12px; border: 1px solid var(--border-soft);">
                                    <div style="display:flex; align-items:center; gap:12px;">
                                        <div style="width:32px; height:32px; border-radius:8px; background:white; display:flex; align-items:center; justify-content:center; color:var(--text-muted); box-shadow:0 2px 4px rgba(0,0,0,0.05);"><i class="fa-solid fa-envelope"></i></div>
                                        <div style="font-weight: 600; font-size: 14px; color: var(--text-main);">Correo</div>
                                    </div>
                                    <div style="font-size: 10px; font-weight: 800; color: #10b981; background: rgba(16,185,129,0.1); padding: 4px 8px; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Fijo</div>
                                </div>
                                <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px; background: var(--surface); border-radius: 12px; border: 1px solid var(--border-soft); box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                                    <div style="display:flex; align-items:center; gap:12px;">
                                        <div style="width:32px; height:32px; border-radius:8px; background:rgba(139, 92, 246, 0.1); display:flex; align-items:center; justify-content:center; color:var(--accent-violet);"><i class="fa-solid fa-phone"></i></div>
                                        <div style="font-weight: 600; font-size: 14px; color: var(--text-main);">WhatsApp</div>
                                    </div>
                                    <label class="toggle-switch" style="position:relative; display:inline-block; width:44px; height:24px; margin:0;">
                                        <input type="checkbox" id="req-phone" checked style="opacity:0; width:0; height:0;">
                                        <span class="slider round" style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:#10b981; transition:.4s; border-radius:34px;"></span>
                                        <span class="knob" id="req-phone-knob" style="position:absolute; content:''; height:18px; width:18px; left:22px; bottom:3px; background-color:white; transition:.4s; border-radius:50%; box-shadow:0 2px 4px rgba(0,0,0,0.2);"></span>
                                    </label>
                                </div>
                                <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px; background: var(--surface); border-radius: 12px; border: 1px solid var(--border-soft); box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                                    <div style="display:flex; align-items:center; gap:12px;">
                                        <div style="width:32px; height:32px; border-radius:8px; background:rgba(139, 92, 246, 0.1); display:flex; align-items:center; justify-content:center; color:var(--accent-violet);"><i class="fa-solid fa-cake-candles"></i></div>
                                        <div style="font-weight: 600; font-size: 14px; color: var(--text-main);">Cumpleaños</div>
                                    </div>
                                    <label class="toggle-switch" style="position:relative; display:inline-block; width:44px; height:24px; margin:0;">
                                        <input type="checkbox" id="req-birthday" checked style="opacity:0; width:0; height:0;">
                                        <span class="slider round" style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:#10b981; transition:.4s; border-radius:34px;"></span>
                                        <span class="knob" id="req-birthday-knob" style="position:absolute; content:''; height:18px; width:18px; left:22px; bottom:3px; background-color:white; transition:.4s; border-radius:50%; box-shadow:0 2px 4px rgba(0,0,0,0.2);"></span>
                                    </label>
                                </div>
                            </div>
                            <div style="text-align: right; border-top: 1px solid var(--border-soft); padding-top: 24px;">
                                <button id="btn-save-form-fields" class="btn btn-primary" style="background: linear-gradient(135deg, var(--accent-violet), #c084fc); border: none; padding: 12px 24px; font-weight: 600; border-radius: 12px; box-shadow: 0 4px 12px rgba(139,92,246,0.3);"><i class="fa-solid fa-check"></i> Guardar Configuración</button>
                            </div>
                        </div>

                        <!-- Seguridad -->
                        <div id="section-security" class="premium-card" style="background: var(--surface); border-radius: 20px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid var(--border-soft);">
                            <div style="margin-bottom: 24px;">
                                <h3 style="font-size: 1.25rem; font-weight: 800; color: var(--text-main); margin-bottom: 8px;">Seguridad y Acceso</h3>
                                <p style="font-size: 13px; color: var(--text-muted);">Controla tus credenciales de inicio de sesión.</p>
                            </div>
                            
                            <div class="form-group" style="margin-bottom: 20px;">
                                <label style="display:block; margin-bottom:8px; font-weight:600; font-size:13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">Correo Electrónico (Login)</label>
                                <div style="position: relative;">
                                    <i class="fa-solid fa-envelope" style="position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: var(--text-muted);"></i>
                                    <input type="email" id="acc-email" class="fidelio-input" placeholder="tu@correo.com" style="font-size: 15px; padding: 14px 16px 14px 44px; background: var(--bg-main); border-radius: 12px;" readonly>
                                </div>
                                <span style="font-size: 11px; color: var(--text-muted); margin-top: 6px; display: block;"><i class="fa-solid fa-circle-info" style="margin-right: 4px;"></i> Contacta a soporte si necesitas migrar tu correo administrador.</span>
                            </div>
                            <div class="form-group" style="margin-bottom: 24px;">
                                <label style="display:block; margin-bottom:8px; font-weight:600; font-size:13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">Actualizar Contraseña</label>
                                <div style="position: relative;">
                                    <i class="fa-solid fa-lock" style="position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: var(--text-muted);"></i>
                                    <input type="password" id="acc-password" class="fidelio-input" placeholder="••••••••" style="font-size: 15px; padding: 14px 16px 14px 44px; border-radius: 12px;">
                                </div>
                                <span style="font-size: 11px; color: var(--text-muted); display: block; margin-top: 6px;">Déjalo en blanco para conservar tu contraseña actual.</span>
                            </div>
                            <div style="text-align: right; border-top: 1px solid var(--border-soft); padding-top: 24px;">
                                <button id="btn-save-account" class="btn btn-secondary" style="background: var(--surface); color: var(--text-main); border: 1px solid var(--border-soft); padding: 12px 24px; font-weight: 600; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);"><i class="fa-solid fa-shield-halved"></i> Actualizar Seguridad</button>
                            </div>
                        </div>

                    </div>
                </div>
            </section>
"""

html = html[:start_idx] + new_html + html[end_idx:]

# Cache bust
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

