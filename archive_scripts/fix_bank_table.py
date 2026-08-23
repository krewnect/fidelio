import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_table = """                <!-- Desglose por Usuario -->
                <div class="content-panel" style="padding: 24px;  overflow-x: auto;">
                    <h3 style="font-size: 1.2rem; margin-bottom: 16px; font-weight: 700;">Desglose por Cliente</h3>
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 2px solid var(--border-soft); color: var(--text-muted);">
                                <th style="padding: 16px;">Cliente</th>
                                <th style="padding: 16px;">Total Ingresado</th>
                                <th style="padding: 16px;">Total Gastado</th>
                                <th style="padding: 16px;">Saldo Restante</th>
                            </tr>
                        </thead>
                        <tbody id="bank-table-body">
                            <tr><td colspan="4" style="text-align:center;">Cargando registros...</td></tr>
                        </tbody>
                    </table>
                </div>"""

new_table = """                <!-- Desglose por Usuario -->
                <div class="content-panel" style="padding: 24px;">
                    <h3 style="font-size: 1.2rem; margin-bottom: 16px; font-weight: 700;">Desglose por Cliente</h3>
                    <div style="width: 100%;">
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 16px; padding: 12px 16px; border-bottom: 2px solid var(--border-soft); color: var(--text-muted); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                            <div style="min-width: 150px;">Cliente</div>
                            <div>Total Ingresado</div>
                            <div>Total Gastado</div>
                            <div>Saldo Restante</div>
                        </div>
                        <div id="bank-table-body" style="display: flex; flex-direction: column;">
                            <div style="padding: 20px; text-align: center; color: var(--text-muted);">Cargando registros...</div>
                        </div>
                    </div>
                </div>"""

html = html.replace(old_table, new_table)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML updated.")
