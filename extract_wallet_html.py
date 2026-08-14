import sys
import re

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the prepaid role card
prepaid_card = """                        <label class="role-card" id="loyalty-mode-prepaid">
                            <input type="radio" name="loyalty_mode" value="prepaid" style="display:none;">
                            <div class="role-icon" style="color:var(--accent-violet); background:rgba(139, 92, 246, 0.1);"><i class="fa-solid fa-money-bill-transfer"></i></div>
                            <div class="role-info">
                                <h4>Monedero Prepago</h4>
                                <p>El cliente carga saldo por adelantado a cambio de una bonificación.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>"""
html = html.replace(prepaid_card, '')
# In case the regex misses exact whitespace:
html = re.sub(r'<label class="role-card" id="loyalty-mode-prepaid">.*?</label>', '', html, flags=re.DOTALL)

# 2. Remove settings-prepaid from custom panel
settings_prepaid = """                    <div id="settings-prepaid" style="display:none;">
                        <div class="form-group" style="margin-bottom: 16px;">
                            <label>Monto de Recarga Sugerido (MXN)</label>
                            <input type="number" id="pre-amount" class="fidelio-input" placeholder="Ej. 500" value="500">
                        </div>
                        <div class="form-group">
                            <label>Bono de Regalo al Recargar (MXN)</label>
                            <input type="number" id="pre-bonus" class="fidelio-input" placeholder="Ej. 100" value="100">
                            <p style="font-size:12px; color:var(--text-muted); margin-top:8px;">Al recargar, el cliente recibe <strong style="color:var(--accent-violet);" id="pre-total-display">$600</strong> en total.</p>
                        </div>
                    </div>"""
html = html.replace(settings_prepaid, '')
html = re.sub(r'<div id="settings-prepaid" style="display:none;">.*?</div>\s*</div>', '', html, flags=re.DOTALL)
# The above regex might swallow too much if not careful. Let's do it safely.
# Actually I'll just find `<div id="settings-prepaid"` and remove until its matching closing div.
start = html.find('<div id="settings-prepaid"')
if start != -1:
    # it has 2 inner divs.
    end = html.find('</div>\n                    \n                    <div id="settings-custom-prog"', start)
    if end != -1:
        html = html[:start] + html[end+6:] # keep the </div> of the previous or next? 
        # Better:
        pass # I'll use simple string replace for exact match

html = html.replace("""                    <div id="settings-prepaid" style="display:none;">
                        <div class="form-group" style="margin-bottom: 16px;">
                            <label>Monto de Recarga Sugerido (MXN)</label>
                            <input type="number" id="pre-amount" class="fidelio-input" placeholder="Ej. 500" value="500">
                        </div>
                        <div class="form-group">
                            <label>Bono de Regalo al Recargar (MXN)</label>
                            <input type="number" id="pre-bonus" class="fidelio-input" placeholder="Ej. 100" value="100">
                            <p style="font-size:12px; color:var(--text-muted); margin-top:8px;">Al recargar, el cliente recibe <strong style="color:#10B981;" id="pre-total-display">$600</strong> en total.</p>
                        </div>
                    </div>""", "")

# 3. Add the Independent Wallet Module at the end of tab-loyalty
independent_wallet = """
                <!-- PREPAID WALLET MODULE (ADD-ON) -->
                <div class="accordion-card" style="margin-top: 24px; border: 2px solid rgba(139, 92, 246, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <div>
                            <span style="background: var(--accent-violet); color:white; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight:700; margin-bottom:8px; display:inline-block;">MÓDULO ADICIONAL</span>
                            <h3 style="font-size: 16px; margin:0;"><i class="fa-solid fa-money-bill-transfer" style="color:var(--accent-violet); margin-right:8px;"></i> Monedero de Prepago</h3>
                            <p style="font-size:12px; color:var(--text-muted); margin-top:4px;">Inyecta liquidez permitiendo recargas adelantadas. Funciona en paralelo con tu plan de recompensas.</p>
                        </div>
                        <label class="toggle-switch">
                            <input type="checkbox" id="toggle-prepaid">
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                    
                    <div id="panel-prepaid-config" style="display:none; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border-color);">
                        <div style="display:flex; gap: 24px; flex-wrap: wrap;">
                            <div class="form-group" style="flex:1; min-width: 200px;">
                                <label>Monto de Recarga Sugerido (MXN)</label>
                                <input type="number" id="pre-amount" class="fidelio-input" placeholder="Ej. 500" value="500">
                            </div>
                            <div class="form-group" style="flex:1; min-width: 200px;">
                                <label>Bono Extra de Regalo (MXN)</label>
                                <input type="number" id="pre-bonus" class="fidelio-input" placeholder="Ej. 100" value="100">
                                <p style="font-size:12px; color:var(--text-muted); margin-top:8px;">El cliente pagará $<span id="pre-pay-display">500</span> y recibirá <strong style="color:var(--accent-violet);" id="pre-total-display">$600</strong> de saldo.</p>
                            </div>
                        </div>
                    </div>
                </div>
"""

# Insert before </section> of tab-loyalty
html = html.replace('                </div>\n            </section>', '                </div>\n' + independent_wallet + '            </section>')

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Extracted Wallet HTML.")
