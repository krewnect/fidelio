import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_loading = "if (tbody) tbody.innerHTML = '<tr><td colspan=\"4\" style=\"text-align:center;\">Calculando saldos...</td></tr>';"
new_loading = "if (tbody) tbody.innerHTML = '<div style=\"padding: 20px; text-align: center; color: var(--text-muted);\">Calculando saldos...</div>';"
js = js.replace(old_loading, new_loading)

old_error1 = "if (tbody) tbody.innerHTML = '<tr><td colspan=\"4\" style=\"text-align:center;color:#ef4444;\">Faltan las columnas del Monedero. Corre el script SQL primero.</td></tr>';"
new_error1 = "if (tbody) tbody.innerHTML = '<div style=\"padding: 20px; text-align: center; color: #ef4444;\">Faltan las columnas del Monedero. Corre el script SQL primero.</div>';"
js = js.replace(old_error1, new_error1)

old_error2 = "if (tbody) tbody.innerHTML = `<tr><td colspan=\"4\" style=\"text-align:center;color:#ef4444;\">Error: ${error.message}</td></tr>`;"
new_error2 = "if (tbody) tbody.innerHTML = `<div style=\"padding: 20px; text-align: center; color: #ef4444;\">Error: ${error.message}</div>`;"
js = js.replace(old_error2, new_error2)

old_empty = "if (tbody) tbody.innerHTML = '<tr><td colspan=\"4\" style=\"text-align:center; color:var(--text-muted);\">No hay saldos registrados aún.</td></tr>';"
new_empty = "if (tbody) tbody.innerHTML = '<div style=\"padding: 20px; text-align: center; color: var(--text-muted);\">No hay saldos registrados aún.</div>';"
js = js.replace(old_empty, new_empty)

old_row = """                    tbody.innerHTML += `
                        <tr style="border-bottom: 1px solid var(--border-soft);">
                            <td style="padding: 16px;">
                                <strong>${c.full_name || 'Sin Nombre'}</strong>
                                <div style="font-size:12px; color:var(--text-muted);">${c.email}</div>
                            </td>
                            <td style="padding: 16px; color: #10b981; font-weight: 600;">$${deposited.toFixed(2)}</td>
                            <td style="padding: 16px; color: #ef4444;">$${spent.toFixed(2)}</td>
                            <td style="padding: 16px; font-weight: 700; color: var(--accent-violet);">$${balance.toFixed(2)}</td>
                        </tr>
                    `;"""

new_row = """                    tbody.innerHTML += `
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 16px; padding: 16px; border-bottom: 1px solid var(--border-soft); align-items: center; transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                            <div style="min-width: 150px;">
                                <strong style="color: #111827;">${c.full_name || 'Sin Nombre'}</strong>
                                <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">${c.email}</div>
                            </div>
                            <div style="color: #10b981; font-weight: 600; font-size: 15px;">$${deposited.toFixed(2)}</div>
                            <div style="color: #ef4444; font-size: 15px;">$${spent.toFixed(2)}</div>
                            <div style="font-weight: 700; color: var(--accent-violet); font-size: 16px;">$${balance.toFixed(2)}</div>
                        </div>
                    `;"""

js = js.replace(old_row, new_row)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS updated.")
