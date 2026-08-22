import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                        <!-- 1. Identidad -->"""

rules_html = """                        <!-- 0. Reglas de Fidelización (UNIFICADO) -->
                        <div style="background: rgba(139, 92, 246, 0.05); padding: 24px; border-radius: 16px; border: 1px dashed rgba(139, 92, 246, 0.3);">
                            <div class="premium-section-title" style="color: var(--accent-violet);">1. Reglas de Recompensa</div>
                            <p class="premium-section-desc">Define qué ganan tus clientes al guardar esta tarjeta.</p>
                            
                            <div style="display:flex; flex-direction:column; gap:16px;">
                                <div>
                                    <label class="premium-label">¿Qué premio van a ganar?</label>
                                    <input type="text" id="unified-reward" class="premium-input" placeholder="Ej: ¡Felicidades! Ganaste un Frappé Gratis." value="Felicidades, ganaste un premio" oninput="if(window.updateUnifiedReward) window.updateUnifiedReward(this.value)">
                                </div>
                                <div>
                                    <label class="premium-label">Instrucciones Breves</label>
                                    <input type="text" id="unified-desc" class="premium-input" placeholder="Ej: Acumula 10 sellos para ganar." value="Acumula visitas para ganar." oninput="if(window.updateUnifiedDesc) window.updateUnifiedDesc(this.value)">
                                </div>
                            </div>
                        </div>
                        
                        <div class="premium-divider"></div>
                        
                        <!-- 1. Identidad -->"""

html = html.replace(target, rules_html)

# Let's also change the H1 from "Diseñador Wallet" to "Creador Mágico"
html = html.replace('<h1 style="font-size: 24px; font-weight: 800; letter-spacing: -1px; color: #111827;">Diseñador Wallet</h1>', '<h1 style="font-size: 24px; font-weight: 800; letter-spacing: -1px; color: #111827;">✨ Creador de Tarjetas Mágico</h1>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
