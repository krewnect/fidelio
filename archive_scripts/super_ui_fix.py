import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix the iPhone mockup being cut off
iphone_css = """                        <div class="iphone-pro-mockup" style="width: 320px; height: 650px;"""
iphone_css_new = """                        <div class="iphone-pro-mockup" style="width: 320px; min-height: 650px; padding-bottom: 20px;"""
html = html.replace(iphone_css, iphone_css_new)

# 2. Fix the missing "1. El Premio" by rewriting it completely to be a fresh card
target_el_premio = re.search(r'<!-- 0\. Reglas de Fidelización \(UNIFICADO\) -->.*?<div class="premium-divider"></div>', html, re.DOTALL)
if target_el_premio:
    new_el_premio = """<!-- 0. Reglas de Fidelización (UNIFICADO) -->
                        <div class="builder-card" style="border-left: 6px solid #8b5cf6;">
                            <div class="premium-section-title"><i class="fa-solid fa-gift" style="color:#8b5cf6;"></i> 1. El Premio</div>
                            <p class="premium-section-desc" style="color:#6b7280; font-size:13px; margin-bottom:20px;">Define qué ganan tus clientes al guardar esta tarjeta en su Apple Wallet.</p>
                            
                            <div style="display:flex; flex-direction:column; gap:20px; background:#f8fafc; padding:20px; border-radius:16px; border:1px solid #e2e8f0;">
                                <div>
                                    <label class="premium-label" style="font-weight:700;"><i class="fa-solid fa-trophy text-muted"></i> ¿Qué premio van a ganar?</label>
                                    <input type="text" id="unified-reward" class="premium-input" style="background:white;" placeholder="Ej: ¡Felicidades! Ganaste un Frappé Gratis." value="Felicidades, ganaste un premio" oninput="if(window.updateUnifiedReward) window.updateUnifiedReward(this.value)">
                                </div>
                                <div>
                                    <label class="premium-label" style="font-weight:700;"><i class="fa-solid fa-comment-dots text-muted"></i> Instrucciones Breves</label>
                                    <input type="text" id="unified-desc" class="premium-input" style="background:white;" placeholder="Ej: Acumula 10 sellos para ganar." value="Acumula visitas para ganar." oninput="if(window.updateUnifiedDesc) window.updateUnifiedDesc(this.value)">
                                </div>
                            </div>
                        </div>
                        
                        <div class="premium-divider"></div>\n"""
    html = html.replace(target_el_premio.group(0), new_el_premio)

# 3. Fix "Citas y Pagos" so it looks PREMIUM and not just naked inputs
target_citas = re.search(r'<!-- 2\.5 Citas y Pagos \(Professional Only\) -->.*?<div class="premium-divider plan-professional-only"></div>', html, re.DOTALL)
if target_citas:
    new_citas = """<!-- 2.5 Citas y Pagos (Professional Only) -->
                        <div class="builder-card plan-professional-only" style="margin-bottom:24px; background: linear-gradient(to right, #ffffff, #f3e8ff); border: 1px solid #e9d5ff;">
                            <div class="premium-section-title"><i class="fa-solid fa-calendar-check" style="color:#8b5cf6;"></i> Integración de Citas y Pagos <span style="background:#8b5cf6; color:white; font-size:10px; padding:3px 8px; border-radius:6px; margin-left:8px; font-weight:bold; letter-spacing:1px;">PRO</span></div>
                            <p style="font-size:13px; color:#4b5563; margin-bottom:20px;">Añade botones interactivos directamente en la tarjeta Wallet para que tus clientes agenden o paguen con un solo toque.</p>
                            
                            <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:20px; margin-bottom:10px;">
                                <div style="background:white; padding:16px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.03); border:1px solid #f1f5f9;">
                                    <label class="premium-label" style="font-weight:700;"><i class="fa-regular fa-calendar-plus" style="color:#8b5cf6;"></i> Botón 'Agendar Cita'</label>
                                    <select id="builder-btn-appointment" class="premium-input" style="background:#f8fafc; cursor:pointer;">
                                        <option value="no">No, ocultar botón</option>
                                        <option value="yes">Sí, habilitar botón en la tarjeta</option>
                                    </select>
                                </div>
                                <div style="background:white; padding:16px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.03); border:1px solid #f1f5f9;">
                                    <label class="premium-label" style="font-weight:700;"><i class="fa-solid fa-credit-card" style="color:#10b981;"></i> Botón 'Pagar Cita'</label>
                                    <select id="builder-btn-payment" class="premium-input" style="background:#f8fafc; cursor:pointer;">
                                        <option value="no">No, ocultar botón</option>
                                        <option value="yes">Sí, habilitar botón en la tarjeta</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div class="premium-divider plan-professional-only"></div>\n"""
    html = html.replace(target_citas.group(0), new_citas)

# 4. Fix "Beneficios Visibles" to look PREMIUM
target_beneficios = re.search(r'<!-- 4\. Beneficios Visibles -->.*?<div class="premium-divider"></div>', html, re.DOTALL)
if target_beneficios:
    new_beneficios = """<!-- 4. Beneficios Visibles -->
                        <div id="section-visible-benefits" class="builder-card" style="margin-bottom:24px;">
                            <div class="premium-section-title"><i class="fa-solid fa-eye" style="color:#3b82f6;"></i> 4. Beneficios Visibles</div>
                            <p style="font-size:13px; color:#6b7280; margin-bottom:20px;">Configura la mecánica frontal de tu tarjeta.</p>
                            
                            <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:20px; background:#f8fafc; padding:20px; border-radius:16px; border:1px solid #e2e8f0; margin-bottom:20px;">
                                <div>
                                    <label class="premium-label" style="font-weight:700;"><i class="fa-solid fa-bullseye text-muted"></i> Meta de Sellos</label>
                                    <input type="number" id="stamps-total" class="premium-input" style="background:white; font-size:16px; font-weight:bold; color:#8b5cf6;" value="10" min="1" max="20" onchange="if(window.updatePassRender) window.updatePassRender()">
                                </div>
                                <div>
                                    <label class="premium-label" style="font-weight:700;"><i class="fa-solid fa-unlock text-muted"></i> Siguiente Premio a Desbloquear</label>
                                    <input type="text" class="premium-input" style="background:#f1f5f9; color:#94a3b8; cursor:not-allowed;" value="Se autocompleta con el Premio." disabled>
                                </div>
                            </div>
                            
                            <div style="background:#f8fafc; padding:20px; border-radius:16px; border:1px solid #e2e8f0;">
                                <label class="premium-label" style="font-weight:700;"><i class="fa-solid fa-scale-balanced text-muted"></i> Términos Legales (Reverso de la tarjeta)</label>
                                <textarea id="rest-terms" class="premium-textarea" style="background:white; height:80px;">Las recompensas no son transferibles ni canjeables por efectivo.</textarea>
                            </div>
                        </div>
                        
                        <div class="premium-divider"></div>\n"""
    html = html.replace(target_beneficios.group(0), new_beneficios)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
