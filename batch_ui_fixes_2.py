import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update program-type-select with 8 programs
old_select = """                                    <select id="program-type-select" class="premium-input" style="font-weight:600;" onchange="if(window.updatePassRender) window.updatePassRender();">
                                        <option value="stamps">Cuadrícula de Sellos (Visitas)</option>
                                        <option value="cashback">Monedero Electrónico (Cashback)</option>
                                        <option value="hybrid">Híbrido (VIP + Cashback)</option>
                                    </select>"""

new_select = """                                    <select id="program-type-select" class="premium-input" style="font-weight:600;" onchange="if(window.updatePassRender) window.updatePassRender();">
                                        <option value="stamps">Cuadrícula de Sellos (Visitas)</option>
                                        <option value="cashback">Monedero Electrónico (Cashback)</option>
                                        <option value="hybrid">Híbrido (VIP + Cashback)</option>
                                        <option value="subscription">Membresía Pagada (Suscripción)</option>
                                        <option value="discount">Descuento Fijo (VIP)</option>
                                        <option value="points">Sistema de Puntos Tradicional</option>
                                        <option value="punch">Tarjeta Perforada Clásica</option>
                                        <option value="coupons">Cupones de un solo uso</option>
                                    </select>"""

html = html.replace(old_select, new_select)

# 2. Update AI Campaigns UI
old_ai = """                        <div style="background: var(--surface-color); padding: 20px; border-radius: 12px; border: 1px solid var(--border-color);">
                            <h3 style="margin-bottom: 15px;">Crear Campaña con IA</h3>
                            <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 20px;">Describe qué quieres lograr y nuestra IA diseñará la campaña, la tarjeta y las reglas por ti.</p>
                            
                            <div style="margin-bottom: 15px;">
                                <label style="display: block; margin-bottom: 8px; color: var(--text-muted); font-size: 14px;">¿Cuál es tu objetivo?</label>
                                <textarea id="ai-prompt" class="fidelio-input" rows="4" placeholder="Ej. Quiero aumentar las ventas los martes por la tarde y recompensar a mis clientes que gastan más de $500..." style="resize: vertical;"></textarea>
                            </div>
                            
                            <button class="btn btn-primary" onclick="generateAICampaign()" id="btn-generate-ai" style="width: 100%;">
                                <i class="fa-solid fa-wand-magic-sparkles"></i> Generar Campaña Mágicamente
                            </button>
                        </div>"""

new_ai = """                        <div style="background: linear-gradient(180deg, var(--surface-color) 0%, rgba(15,23,42,1) 100%); padding: 30px; border-radius: 16px; border: 1px solid var(--primary); box-shadow: 0 10px 40px rgba(139,92,246,0.15); position:relative; overflow:hidden;">
                            <div style="position:absolute; top:-50px; right:-50px; width:150px; height:150px; background:var(--primary); filter:blur(80px); opacity:0.3; border-radius:50%;"></div>
                            
                            <div style="display:flex; align-items:center; gap:15px; margin-bottom: 25px;">
                                <div style="width:50px; height:50px; background:linear-gradient(135deg, var(--primary) 0%, #d8b4fe 100%); border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow: 0 0 20px rgba(139,92,246,0.5);">
                                    <i class="fa-solid fa-robot" style="color:white; font-size:24px;"></i>
                                </div>
                                <div>
                                    <h3 style="margin:0; font-size:22px; color:white;">Fidelio AI Brain</h3>
                                    <p style="margin:0; color:var(--text-muted); font-size:14px;">Tu Copiloto de Marketing 24/7</p>
                                </div>
                            </div>
                            
                            <div id="ai-chat-history" style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:20px; height:200px; overflow-y:auto; margin-bottom:20px; display:flex; flex-direction:column; gap:15px;">
                                <div style="display:flex; gap:10px;">
                                    <div style="width:30px; height:30px; border-radius:50%; background:var(--primary); display:flex; align-items:center; justify-content:center; flex-shrink:0;"><i class="fa-solid fa-robot" style="color:white; font-size:12px;"></i></div>
                                    <div style="background:rgba(139,92,246,0.1); padding:12px 15px; border-radius:0 12px 12px 12px; border:1px solid rgba(139,92,246,0.2); font-size:14px; color:white;">¡Hola! Soy tu asistente de IA. Dime qué quieres lograr (ej. "Atraer clientes los martes", "Lanzar un producto nuevo") y yo configuraré la campaña, el diseño de la tarjeta y las reglas matemáticas por ti.</div>
                                </div>
                            </div>
                            
                            <div style="position:relative;">
                                <textarea id="ai-prompt" class="fidelio-input" rows="2" placeholder="Ej. Quiero aumentar las ventas los martes..." style="width:100%; padding-right:50px; resize:none; border-radius:12px; background:rgba(255,255,255,0.05); color:white; border:1px solid rgba(255,255,255,0.2);"></textarea>
                                <button class="btn" onclick="generateAICampaign()" id="btn-generate-ai" style="position:absolute; right:10px; bottom:15px; background:var(--primary); color:white; border:none; width:35px; height:35px; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; transition:all 0.2s;">
                                    <i class="fa-solid fa-paper-plane"></i>
                                </button>
                            </div>
                            
                            <div style="display:flex; gap:10px; margin-top:15px; flex-wrap:wrap;">
                                <span style="font-size:12px; color:var(--text-muted);">Sugerencias:</span>
                                <span style="font-size:11px; background:rgba(255,255,255,0.1); padding:4px 10px; border-radius:10px; cursor:pointer;" onclick="document.getElementById('ai-prompt').value='Quiero recompensar a los clientes que gastan más de $1000 al mes'">Recompensar VIPs</span>
                                <span style="font-size:11px; background:rgba(255,255,255,0.1); padding:4px 10px; border-radius:10px; cursor:pointer;" onclick="document.getElementById('ai-prompt').value='Necesito mover inventario que está por caducar'">Mover Inventario</span>
                            </div>
                        </div>"""

if "Crear Campaña con IA" in html and "Fidelio AI Brain" not in html:
    html = html.replace(old_ai, new_ai)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Task 8 (AI and 8 Programs) completed.")
