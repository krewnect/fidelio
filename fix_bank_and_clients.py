import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX THE BANK (Replace the metrics-grid with the beautiful design)
old_bank_grid = """                <div class="metrics-grid" style="margin-bottom: 24px; grid-template-columns: 1fr 1fr;">
                    <div class="metric-card" style="border-left: 4px solid var(--accent-violet);">
                        <div class="metric-title"><i class="fa-solid fa-wallet" style="color:var(--accent-violet); margin-right:8px;"></i> Total Prepagado (Histórico)</div>
                        <div class="metric-value" id="bank-total-deposited">$0.00</div>
                        <div class="metric-trend" style="color: var(--text-muted);">Dinero total que han metido tus clientes al monedero.</div>
                    </div>
                    <div class="metric-card" style="border-left: 4px solid #10b981;">
                        <div class="metric-title"><i class="fa-solid fa-vault" style="color:#10b981; margin-right:8px;"></i> Bolsa de Dinero No Gastado</div>
                        <div class="metric-value" id="bank-total-unspent" style="color: #10b981;">$0.00</div>
                        <div class="metric-trend" style="color: var(--text-muted);">Pasivo actual: Dinero que tienen a favor para gastar.</div>
                    </div>
                </div>"""

new_bank_grid = """                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 32px;">
                    <!-- Metric Card 1: Total Prepagado -->
                    <div style="background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(0,0,0,0) 100%); border: 1px solid rgba(16,185,129,0.2); border-radius: 20px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); position: relative; overflow: hidden;">
                        <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; color: rgba(16,185,129,0.05);"><i class="fa-solid fa-vault"></i></div>
                        <div style="font-size: 13px; font-weight: bold; color: #10b981; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">Total Prepagado (Histórico)</div>
                        <div id="bank-total-deposited" style="font-size: 3rem; font-weight: 800; color: var(--text-main); margin-bottom: 5px;">$0.00</div>
                        <div style="font-size: 13px; color: var(--text-muted);">Dinero ingresado por tarjetas de regalo y monederos.</div>
                    </div>

                    <!-- Metric Card 2: Pasivo Circulante -->
                    <div style="background: linear-gradient(135deg, rgba(244,63,94,0.1) 0%, rgba(0,0,0,0) 100%); border: 1px solid rgba(244,63,94,0.2); border-radius: 20px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); position: relative; overflow: hidden;">
                        <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; color: rgba(244,63,94,0.05);"><i class="fa-solid fa-hand-holding-dollar"></i></div>
                        <div style="font-size: 13px; font-weight: bold; color: #f43f5e; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">Pasivo Circulante Vivo</div>
                        <div id="bank-total-unspent" style="font-size: 3rem; font-weight: 800; color: var(--text-main); margin-bottom: 5px;">$0.00</div>
                        <div style="font-size: 13px; color: var(--text-muted);">Bolsa de dinero no gastado a favor del cliente.</div>
                    </div>
                </div>"""

if old_bank_grid in html:
    html = html.replace(old_bank_grid, new_bank_grid)
    print("The Bank redesigned.")
else:
    print("Could not find The Bank HTML to replace.")


# 2. FIX TOP CLIENTS METRICS (Empty the fake data)
# "Top Clientes (Mes)" table
top_clientes_old = """                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="display:flex; align-items:center; gap:12px;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:var(--accent-orange); color:white; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700;">1</div>
                                    <div>
                                        <div style="font-weight:700; font-size:14px; color:var(--text-main);">Mariana Vega</div>
                                        <div style="font-size:11px; color:var(--text-muted);">VIP Oro</div>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-weight:800; font-size:14px; color:var(--text-main);">$4,250</div>
                                    <div style="font-size:11px; color:var(--text-muted);">6 visitas</div>
                                </div>
                            </div>
                            
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="display:flex; align-items:center; gap:12px;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:#9ca3af; color:white; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700;">2</div>
                                    <div>
                                        <div style="font-weight:700; font-size:14px; color:var(--text-main);">David Silva</div>
                                        <div style="font-size:11px; color:var(--text-muted);">VIP Plata</div>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-weight:800; font-size:14px; color:var(--text-main);">$3,800</div>
                                    <div style="font-size:11px; color:var(--text-muted);">4 visitas</div>
                                </div>
                            </div>
                            
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="display:flex; align-items:center; gap:12px;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:#b45309; color:white; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700;">3</div>
                                    <div>
                                        <div style="font-weight:700; font-size:14px; color:var(--text-main);">Elena Rios</div>
                                        <div style="font-size:11px; color:var(--text-muted);">VIP Bronce</div>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-weight:800; font-size:14px; color:var(--text-main);">$2,950</div>
                                    <div style="font-size:11px; color:var(--text-muted);">5 visitas</div>
                                </div>
                            </div>"""

top_clientes_new = """                            <div style="display:flex; justify-content:center; align-items:center; height: 100%; color: var(--text-muted); font-size: 14px; text-align:center;">
                                <p>Aún no hay clientes top este mes.</p>
                            </div>"""

if top_clientes_old in html:
    html = html.replace(top_clientes_old, top_clientes_new)
    print("Top Clientes zeroed.")

# 3. FIX HEATMAP (Remove background colors of the grid)
# Just regex replace all occurrences of `background:var(--accent-violet)` or `#8b5cf6` or `#c4b5fd` inside the heatmap grid
html = re.sub(r'background:\s*var\(--accent-violet\);', 'background: var(--bg-input);', html)
html = re.sub(r'background:\s*rgba\(139, 92, 246, [0-9.]+\);', 'background: var(--bg-input);', html)
# specifically the heatmap blocks like `background:#4c1d95;`, `background:#6d28d9;`, `background:#8b5cf6;`, `background:#a78bfa;`, `background:#c4b5fd;`
heatmap_colors = ['#4c1d95', '#6d28d9', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ede9fe']
for color in heatmap_colors:
    html = html.replace(f'background:{color};', 'background: var(--bg-input);')

print("Heatmap zeroed.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
