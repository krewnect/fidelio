import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add the Program Type selector in the sidebar before 'Siguiente Premio a Desbloquear'
sidebar_addition = """
                                <div>
                                    <label class="premium-label">Tipo de Programa</label>
                                    <select id="program-type-select" class="premium-input" style="font-weight:600;">
                                        <option value="cashback" selected>Monedero Digital (Cashback & QR)</option>
                                        <option value="stamps">Tarjeta de Sellos (Visitas frecuentes)</option>
                                    </select>
                                </div>
                                <div id="stamps-config-group" style="display:none; flex-direction:column; gap:16px;">
                                    <div>
                                        <label class="premium-label">Total de Sellos (Meta)</label>
                                        <input type="number" id="stamps-total" class="premium-input" value="5" min="3" max="10">
                                    </div>
                                </div>
                                
                                <div>
                                    <label class="premium-label">Siguiente Premio a Desbloquear"""

html = html.replace('<div>\n                                    <label class="premium-label">Siguiente Premio a Desbloquear', sidebar_addition)

# 2. Add the stamps container inside the card layout in the preview area
# The easiest place is inside .pass-body-section right before or replacing .pass-qr-section
# Let's put it next to pass-qr-section but default hidden
stamps_container_html = """
                                                <div id="render-stamps-view" style="display:none; flex-direction:column; align-items:center; padding-top:20px; border-top: 1px dashed #e5e7eb;">
                                                    <div style="font-size:11px; font-weight:700; color:#6b7280; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">Tus Visitas</div>
                                                    <div id="render-stamps-grid" style="display:flex; gap:8px; justify-content:center; flex-wrap:wrap; max-width:280px;">
                                                        <!-- Stamps will be generated here -->
                                                    </div>
                                                </div>
                                                
                                                <div class="pass-qr-section" id="render-qr-view">"""

html = html.replace('<div class="pass-qr-section">', stamps_container_html)
html = html.replace('<div class="pass-qr-section">', '<div class="pass-qr-section" id="render-qr-view">') # In case it didn't match perfectly, but it should

with open('index.html', 'w') as f:
    f.write(html)
