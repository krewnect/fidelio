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


# 3. Add the Independent Wallet Module at the exact end of tab-loyalty
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

old_end_of_loyalty = """                    </div>
                </div>
                </div>
            </section>
            <!-- ACCOUNT SETTINGS TAB -->"""

new_end_of_loyalty = "                    </div>\n                </div>\n                </div>\n" + independent_wallet + "            </section>\n            <!-- ACCOUNT SETTINGS TAB -->"

html = html.replace(old_end_of_loyalty, new_end_of_loyalty)

# 4. Inject Wallet Render Block into the Card
old_header_stats = """                                                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                                                    <div>
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Nivel Actual</div>
                                                        <div id="render-vip-caption" style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;">ORO VIP</div>
                                                    </div>
                                                    <div style="text-align:right;">
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Cashback</div>
                                                        <div style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;" id="render-balance">$145.00</div>
                                                    </div>
                                                </div>"""

new_header_stats = """                                                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                                                    <div>
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Nivel Actual</div>
                                                        <div id="render-vip-caption" style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;">ORO VIP</div>
                                                    </div>
                                                    <div id="render-wallet-block" style="display:none; text-align:center;">
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Monedero</div>
                                                        <div style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;" id="render-wallet-balance">$600.00</div>
                                                    </div>
                                                    <div id="render-cashback-block" style="text-align:right;">
                                                        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Cashback</div>
                                                        <div style="font-size:20px; font-weight:800; letter-spacing:-0.5px; font-family:-apple-system, sans-serif;" id="render-balance">$145.00</div>
                                                    </div>
                                                </div>"""
html = html.replace(old_header_stats, new_header_stats)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Fixed HTML.")
