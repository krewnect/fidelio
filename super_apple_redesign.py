import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the CSS for a true Apple-like layout
css_target = r'\.tab-builder-container \{ display: flex; height: calc\(100vh - 100px\); overflow: hidden; background: #f8fafc; margin: -24px; \}'
css_replacement = """.tab-builder-container { display: flex; height: calc(100vh - 100px); overflow: hidden; background: #ffffff; margin: -24px; }
                    .builder-preview-area { flex: 1; display: flex; align-items: center; justify-content: center; position: relative; background: #f8fafc; height: 100%; overflow: hidden; }
                    .builder-sidebar { 
                        width: 50%; 
                        max-width: 650px; 
                        background: #ffffff; 
                        overflow-y: auto; 
                        padding: 50px 60px; 
                        display:flex; 
                        flex-direction:column; 
                        z-index:10; 
                        border-right: 1px solid rgba(0,0,0,0.05);
                        box-shadow: 10px 0 30px rgba(0,0,0,0.02);
                    }
                    .builder-sidebar::-webkit-scrollbar { width: 6px; }
                    .builder-sidebar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
                    
                    /* Apple-like form sections */
                    .apple-section {
                        margin-bottom: 40px;
                    }
                    .apple-section-header {
                        font-size: 18px;
                        font-weight: 700;
                        letter-spacing: -0.5px;
                        color: #111827;
                        margin-bottom: 24px;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                        border-bottom: 1px solid #f1f5f9;
                        padding-bottom: 12px;
                    }
                    .apple-section-header i { color: #8b5cf6; }
                    
                    .apple-input-group {
                        margin-bottom: 20px;
                    }
                    .apple-label {
                        font-size: 12px;
                        font-weight: 700;
                        color: #64748b;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 8px;
                        display: block;
                    }
                    .apple-input {
                        width: 100%;
                        background: #f8fafc;
                        border: 1px solid #e2e8f0;
                        border-radius: 12px;
                        padding: 16px;
                        font-size: 15px;
                        color: #0f172a;
                        font-weight: 500;
                        transition: all 0.2s ease;
                    }
                    .apple-input:focus {
                        outline: none;
                        background: #ffffff;
                        border-color: #8b5cf6;
                        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
                    }
                    
                    /* Clean Premium Buttons */
                    .apple-btn-primary {
                        background: #111827;
                        color: white;
                        border: none;
                        border-radius: 14px;
                        padding: 18px;
                        font-size: 16px;
                        font-weight: 700;
                        width: 100%;
                        cursor: pointer;
                        transition: all 0.2s;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        gap: 10px;
                    }
                    .apple-btn-primary:hover {
                        background: #1f2937;
                        transform: translateY(-2px);
                        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                    }"""

html = re.sub(css_target + r'.*?\.premium-section-title \{ \n                        font-size: 22px; ', css_replacement + '\n                    .premium-section-title { \n                        font-size: 22px; ', html, flags=re.DOTALL)


# 2. Extract and replace the LEFT SIDEBAR HTML
sidebar_target = r'<!-- LEFT SIDEBAR: CONTROLS -->.*?<!-- RIGHT AREA: PHOTOREALISTIC IPHONE -->'
new_sidebar = """<!-- LEFT SIDEBAR: CONTROLS -->
                    <div class="builder-sidebar">
                        
                        <div style="margin-bottom: 40px;">
                            <button onclick="document.querySelector('.nav-tab[data-tab=\\'tab-campaigns\\']').click()" style="background:transparent; border:none; color:#64748b; font-size:13px; font-weight:700; cursor:pointer; margin-bottom:16px; display:flex; align-items:center; gap:6px; padding:0; transition:color 0.2s; text-transform:uppercase; letter-spacing:0.5px;" onmouseover="this.style.color='#111827'" onmouseout="this.style.color='#64748b'">
                                <i class="fa-solid fa-arrow-left"></i> Volver
                            </button>
                            <h1 style="font-size: 32px; font-weight: 800; letter-spacing: -1.5px; color: #111827; margin: 0;">Diseñador Mágico</h1>
                            <p style="font-size: 15px; color: #64748b; margin-top: 8px; line-height: 1.5;">Configura la tarjeta digital Wallet de tu negocio. Todos los cambios se reflejan al instante en la vista previa derecha.</p>
                            
                            <div style="margin-top:24px; background: linear-gradient(135deg, rgba(139,92,246,0.1) 0%, rgba(59,130,246,0.1) 100%); padding:20px 24px; border-radius:16px; display:flex; align-items:center; gap:20px; border:1px solid rgba(139,92,246,0.2);">
                                <div style="font-size:32px; filter:drop-shadow(0 4px 6px rgba(139,92,246,0.3)); animation: float 3s ease-in-out infinite;">🤖</div>
                                <div style="flex:1;">
                                    <h4 style="margin:0 0 4px; font-size:16px; font-weight:800; color:#1e1b4b;">Copiloto de Marketing IA</h4>
                                    <p style="margin:0; font-size:13px; color:#475569; line-height:1.4;">Deja que la IA analice tu industria y configure la estrategia perfecta por ti.</p>
                                </div>
                                <button onclick="triggerAIMagicDesign()" style="background:linear-gradient(135deg, #8b5cf6, #3b82f6); color:white; border:none; padding:12px 20px; border-radius:12px; font-weight:700; font-size:14px; cursor:pointer; transition:transform 0.2s; box-shadow:0 4px 15px rgba(139,92,246,0.3);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                                    ¡Haz Magia! ✨
                                </button>
                            </div>
                        </div>

                        <!-- 1. IDENTIDAD -->
                        <div class="apple-section">
                            <div class="apple-section-header"><i class="fa-solid fa-store"></i> Identidad de Marca</div>
                            
                            <div class="apple-input-group">
                                <label class="apple-label">Nombre del Negocio / Especialista</label>
                                <input type="text" id="rest-name" class="apple-input" value="Mi Negocio">
                            </div>
                            
                            <div style="display:flex; gap:16px;">
                                <div class="apple-input-group" style="flex:1;">
                                    <label class="apple-label">Categoría</label>
                                    <input type="text" id="business-category-input" class="apple-input" value="Mi Negocio / Especialidad">
                                </div>
                                <div class="apple-input-group" style="flex:1;">
                                    <label class="apple-label">Ícono Decorativo</label>
                                    <select id="rest-icon" class="apple-input">
                                        <option value="fa-crown" selected>Corona (VIP)</option>
                                        <option value="fa-stethoscope">Salud / Médico</option>
                                        <option value="fa-scissors">Estética / Spa</option>
                                        <option value="fa-dumbbell">Gym / Fitness</option>
                                        <option value="fa-burger">Gastronomía</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="apple-input-group">
                                <label class="apple-label">Logo del Negocio</label>
                                <div style="display:flex; align-items:center; gap:16px;">
                                    <div style="flex:1; border: 2px dashed #cbd5e1; background:#f8fafc; border-radius:12px; padding:20px; text-align:center; cursor:pointer; transition:all 0.2s;" onmouseover="this.style.borderColor='#8b5cf6'" onmouseout="this.style.borderColor='#cbd5e1'" onclick="document.getElementById('logo-file-input').click()">
                                        <input type="file" id="logo-file-input" accept="image/png, image/jpeg" style="display:none;">
                                        <i class="fa-solid fa-cloud-arrow-up" style="color:#94a3b8; font-size:20px; margin-bottom:8px;"></i>
                                        <div style="font-size:13px; color:#64748b; font-weight:600;">Haz clic para subir imagen</div>
                                    </div>
                                    <button id="btn-remove-logo" style="display:none; background:#fee2e2; color:#ef4444; border:none; padding:12px; border-radius:12px; font-weight:700; cursor:pointer;">Quitar</button>
                                </div>
                            </div>
                        </div>

                        <!-- 2. RECOMPENSAS -->
                        <div class="apple-section">
                            <div class="apple-section-header"><i class="fa-solid fa-gift"></i> Mecánica de Lealtad</div>
                            
                            <div style="display:flex; gap:16px;">
                                <div class="apple-input-group" style="flex:1;">
                                    <label class="apple-label">Meta de Sellos</label>
                                    <input type="number" id="stamps-total" class="apple-input" value="10" min="1" max="20" onchange="if(window.updatePassRender) window.updatePassRender()">
                                </div>
                                <div class="apple-input-group" style="flex:2;">
                                    <label class="apple-label">Instrucción al Cliente</label>
                                    <input type="text" id="unified-desc" class="apple-input" value="Acumula visitas para ganar." oninput="if(window.updateUnifiedDesc) window.updateUnifiedDesc(this.value)">
                                </div>
                            </div>
                            
                            <div class="apple-input-group">
                                <label class="apple-label">¿Qué premio van a ganar al llenar la tarjeta?</label>
                                <input type="text" id="unified-reward" class="apple-input" value="Felicidades, ganaste un premio" oninput="if(window.updateUnifiedReward) window.updateUnifiedReward(this.value)">
                            </div>
                        </div>

                        <!-- 3. APARIENCIA -->
                        <div class="apple-section">
                            <div class="apple-section-header"><i class="fa-solid fa-palette"></i> Diseño y Colores</div>
                            
                            <div style="display:flex; gap:24px; margin-bottom:20px;">
                                <div class="apple-input-group">
                                    <label class="apple-label">Color Principal</label>
                                    <input type="color" id="color-primary" style="-webkit-appearance:none; border:none; width:50px; height:50px; border-radius:12px; cursor:pointer; padding:0; background:transparent;" value="#1e1b4b">
                                </div>
                                <div class="apple-input-group">
                                    <label class="apple-label">Color Acento</label>
                                    <input type="color" id="color-accent" style="-webkit-appearance:none; border:none; width:50px; height:50px; border-radius:12px; cursor:pointer; padding:0; background:transparent;" value="#8b5cf6">
                                </div>
                            </div>
                            
                            <div class="apple-input-group">
                                <label class="apple-label">Banner Wallet (Opcional)</label>
                                <div style="display:flex; align-items:center; gap:16px;">
                                    <div style="flex:1; border: 2px dashed #cbd5e1; background:#f8fafc; border-radius:12px; padding:20px; text-align:center; cursor:pointer; transition:all 0.2s;" onmouseover="this.style.borderColor='#8b5cf6'" onmouseout="this.style.borderColor='#cbd5e1'" onclick="document.getElementById('banner-file-input').click()">
                                        <input type="file" id="banner-file-input" accept="image/png, image/jpeg" style="display:none;">
                                        <i class="fa-regular fa-image" style="color:#94a3b8; font-size:20px; margin-bottom:8px;"></i>
                                        <div style="font-size:13px; color:#64748b; font-weight:600;">Subir imagen ancha (1125x432 px)</div>
                                    </div>
                                    <button id="btn-remove-banner" style="display:none; background:#fee2e2; color:#ef4444; border:none; padding:12px; border-radius:12px; font-weight:700; cursor:pointer;">Quitar</button>
                                </div>
                            </div>
                        </div>

                        <!-- 4. CITAS Y PAGOS (PRO) -->
                        <div class="apple-section plan-professional-only" style="background: linear-gradient(135deg, #f8fafc, #f3e8ff); padding: 24px; border-radius: 20px; border: 1px solid #e9d5ff;">
                            <div class="apple-section-header" style="border-bottom:none; margin-bottom:12px; padding-bottom:0;"><i class="fa-solid fa-calendar-check"></i> Integración Wallet <span style="background:#8b5cf6; color:white; font-size:10px; padding:4px 8px; border-radius:6px; margin-left:8px; letter-spacing:1px;">PRO</span></div>
                            <p style="font-size:13px; color:#64748b; margin-bottom:20px; line-height:1.5;">Agrega botones interactivos al reverso de tu tarjeta para que tus clientes agenden o paguen con un toque.</p>
                            
                            <div class="apple-input-group">
                                <label class="apple-label"><i class="fa-regular fa-calendar-plus" style="margin-right:6px;"></i> Botón 'Agendar Cita'</label>
                                <select id="builder-btn-appointment" class="apple-input" style="background:white;">
                                    <option value="no">Desactivado</option>
                                    <option value="yes">Activar botón de Reservas</option>
                                </select>
                            </div>
                            
                            <div class="apple-input-group" style="margin-bottom:0;">
                                <label class="apple-label"><i class="fa-solid fa-credit-card" style="margin-right:6px;"></i> Botón 'Pagar Cita'</label>
                                <select id="builder-btn-payment" class="apple-input" style="background:white;">
                                    <option value="no">Desactivado</option>
                                    <option value="yes">Activar botón de Pago</option>
                                </select>
                            </div>
                        </div>

                        <!-- 5. TÉRMINOS LEGALES -->
                        <div class="apple-section" style="margin-bottom:20px;">
                            <div class="apple-input-group">
                                <label class="apple-label">Términos Legales (Reverso)</label>
                                <textarea id="rest-terms" class="apple-input" style="height:80px; resize:vertical;">Las recompensas no son transferibles ni canjeables por efectivo.</textarea>
                            </div>
                            <!-- Hidden inputs required by JS bindings -->
                            <div style="display:none;">
                                <input type="text" id="stamps-reward" value="">
                                <textarea id="pass-policies"></textarea>
                                <select id="program-type-select"><option value="cashback"></option><option value="stamps" selected></option></select>
                                <input type="text" id="rest-desc" value="">
                            </div>
                        </div>
                        
                        <div style="margin-top:auto; padding-top:16px;">
                            <button id="btn-save-design-push" class="apple-btn-primary"><i class="fa-solid fa-cloud-arrow-up"></i> Guardar y Publicar Diseño</button>
                        </div>
                    </div>
                    
                    <!-- RIGHT AREA: PHOTOREALISTIC IPHONE -->"""

html = re.sub(sidebar_target, new_sidebar, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
