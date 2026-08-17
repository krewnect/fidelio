import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Diseñador Card (nav-builder)
# Remove display:none from nav-builder so it's visible by default (or let JS handle it, but we make sure it's not hardcoded to display:none unconditionally if it was)
# But wait, in the sidebar:
html = html.replace('<button class="nav-tab" data-tab="tab-builder" id="nav-builder" style="display:none;"><i class="fa-solid fa-wand-magic-sparkles"></i> Diseñador Card</button>', '<button class="nav-tab" data-tab="tab-builder" id="nav-builder"><i class="fa-solid fa-wand-magic-sparkles"></i> Diseñador Card</button>')

# 2. Citas Name
html = html.replace('<button class="nav-tab" data-tab="tab-appointments" id="nav-appointments" style="display:none;"><i class="fa-solid fa-calendar-check"></i> Citas Médicas/Servicios</button>', '<button class="nav-tab" data-tab="tab-appointments" id="nav-appointments" style="display:none;"><i class="fa-solid fa-calendar-check"></i> Citas/Servicios</button>')
html = html.replace('<h1>Agenda de Citas</h1>', '<h1>Citas/Servicios</h1>')

# 3. The Bank - apply Metric Cards
bank_start = '<section id="tab-bank" class="tab-content" style="display:none;">'
bank_end = '<!-- STAFF TAB -->'
if bank_start in html and bank_end in html:
    pre_bank = html.split(bank_start)[0]
    post_bank = html.split(bank_end)[1]
    
    # We rebuild tab-bank completely to ensure metric cards are there
    new_bank = """
            <section id="tab-bank" class="tab-content" style="display:none;">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">EL BANCO (THE BANK)</span>
                        <h1>Control de Flujo de Efectivo</h1>
                        <p>Monitorea tu pasivo circulante y el impacto financiero de tus programas.</p>
                    </div>
                    <button class="btn btn-primary" style="background: var(--accent-violet); border: none;" onclick="loadBankStats()"><i class="fa-solid fa-rotate-right"></i> Actualizar Banco</button>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 32px;">
                    <!-- Metric Card 1: Total Prepagado -->
                    <div style="background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(0,0,0,0) 100%); border: 1px solid rgba(16,185,129,0.2); border-radius: 20px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); position: relative; overflow: hidden;">
                        <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; color: rgba(16,185,129,0.05);"><i class="fa-solid fa-vault"></i></div>
                        <div style="font-size: 13px; font-weight: bold; color: #10b981; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">Total Prepagado (Histórico)</div>
                        <div id="bank-total-prepaid" style="font-size: 3rem; font-weight: 800; color: var(--text-main); margin-bottom: 5px;">$0.00</div>
                        <div style="font-size: 13px; color: var(--text-muted);">Dinero ingresado por tarjetas de regalo y monederos.</div>
                    </div>

                    <!-- Metric Card 2: Pasivo Circulante -->
                    <div style="background: linear-gradient(135deg, rgba(244,63,94,0.1) 0%, rgba(0,0,0,0) 100%); border: 1px solid rgba(244,63,94,0.2); border-radius: 20px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); position: relative; overflow: hidden;">
                        <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; color: rgba(244,63,94,0.05);"><i class="fa-solid fa-hand-holding-dollar"></i></div>
                        <div style="font-size: 13px; font-weight: bold; color: #f43f5e; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">Pasivo Circulante Vivo</div>
                        <div id="bank-current-liability" style="font-size: 3rem; font-weight: 800; color: var(--text-main); margin-bottom: 5px;">$0.00</div>
                        <div style="font-size: 13px; color: var(--text-muted);">Saldo flotante en manos de clientes que pueden venir a canjear.</div>
                    </div>
                </div>

                <div class="content-panel" style="background: var(--surface); border-radius: 20px; padding: 24px; box-shadow: var(--shadow-sm); overflow-x: auto;">
                    <h3 style="margin-bottom: 20px; font-size: 16px;">Transacciones Financieras (Depósitos y Consumos)</h3>
                    <table class="crm-table">
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Cliente</th>
                                <th>Movimiento</th>
                                <th>Tipo</th>
                                <th>Cajero</th>
                            </tr>
                        </thead>
                        <tbody id="bank-table-body">
                            <!-- JS inyecta data -->
                        </tbody>
                    </table>
                </div>
            </section>
"""
    html = pre_bank + new_bank + "            <!-- STAFF TAB -->\n" + post_bank

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("The Bank redesigned, Designer unhidden, Appointments renamed.")
