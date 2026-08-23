import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_metrics = """                <!-- Resumen Financiero -->
                <div class="metrics-grid" style="margin-bottom: 24px; grid-template-columns: 1fr 1fr;">
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

new_metrics = """                <!-- Resumen Financiero -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-bottom: 24px;">
                    <div class="content-panel" style="padding: 24px; border-radius: 16px;">
                        <div style="font-size: 13px; color: var(--text-muted); font-weight: 600; text-transform: uppercase;">TOTAL PREPAGADO (HISTÓRICO) <i class="fa-solid fa-wallet" style="color:var(--accent-violet); margin-left:6px;"></i></div>
                        <div style="font-size: 36px; font-weight: 800; color: #111827; margin: 12px 0;" id="bank-total-deposited">$0.00</div>
                        <div style="font-size: 13px; color: var(--text-muted);">Dinero total que han metido tus clientes al monedero.</div>
                    </div>
                    <div class="content-panel" style="padding: 24px; border-radius: 16px;">
                        <div style="font-size: 13px; color: var(--text-muted); font-weight: 600; text-transform: uppercase;">BOLSA DE DINERO NO GASTADO <i class="fa-solid fa-vault" style="color:#10b981; margin-left:6px;"></i></div>
                        <div style="font-size: 36px; font-weight: 800; color: #10b981; margin: 12px 0;" id="bank-total-unspent">$0.00</div>
                        <div style="font-size: 13px; color: var(--text-muted);">Pasivo actual: Dinero que tienen a favor para gastar.</div>
                    </div>
                </div>"""

if old_metrics in html:
    html = html.replace(old_metrics, new_metrics)
else:
    print("WARNING: Exact match failed")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Bank metrics updated.")
