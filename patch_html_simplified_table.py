import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_table_header = """                            <tr style="border-bottom: 2px solid #E5E7EB; color: #6B7280; font-size:11px; text-transform:uppercase;">
                                <th style="padding: 12px 24px 12px 8px;">Negocio</th>
                                <th style="padding: 12px 24px;">Fecha Registro</th>
                                <th style="padding: 12px 24px;">Plan Actual</th>
                                <th style="padding: 12px 24px;">Tarifa Vigente</th>
                                <th style="padding: 12px 24px;">Estimado Pagado (LTV)</th>
                                <th style="padding: 12px 8px;">Estado Pago</th>
                            </tr>"""

new_table_header = """                            <tr style="border-bottom: 2px solid #E5E7EB; color: #6B7280; font-size:11px; text-transform:uppercase;">
                                <th style="padding: 12px 24px 12px 8px;">Negocio</th>
                                <th style="padding: 12px 24px;">Total Histórico</th>
                                <th style="padding: 12px 8px;">Miembro Desde</th>
                            </tr>"""

if old_table_header in html:
    html = html.replace(old_table_header, new_table_header)
else:
    print("WARNING: Could not find old table header")

old_loading = """<td colspan="6" style="padding: 24px; text-align: center; color: var(--text-muted);">Cargando historial de pagos...</td>"""
new_loading = """<td colspan="3" style="padding: 24px; text-align: center; color: var(--text-muted);">Cargando historial de pagos...</td>"""
html = html.replace(old_loading, new_loading)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML header patched.")
