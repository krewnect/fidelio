import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_loading_js = """tbody.innerHTML = '<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--text-muted);">Cargando...</td></tr>';"""
new_loading_js = """tbody.innerHTML = '<tr><td colspan="3" style="padding:24px;text-align:center;color:var(--text-muted);">Cargando...</td></tr>';"""
js = js.replace(old_loading_js, new_loading_js)

old_error_js = """tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;"""
new_error_js = """tbody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;"""
js = js.replace(old_error_js, new_error_js)

old_empty_js = """tbody.innerHTML = '<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--text-muted);">No hay negocios registrados.</td></tr>';"""
new_empty_js = """tbody.innerHTML = '<tr><td colspan="3" style="padding:24px;text-align:center;color:var(--text-muted);">No hay negocios registrados.</td></tr>';"""
js = js.replace(old_empty_js, new_empty_js)

old_row_js = """            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft); transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 12px 24px 12px 8px; white-space: nowrap;"><strong style="font-size: 14px;">${m.business_name}</strong></td>
                    <td style="padding: 12px 24px; white-space: nowrap; color: var(--text-muted);">${createdDate.toLocaleDateString()}</td>
                    <td style="padding: 12px 24px; white-space: nowrap;"><span class="menu-badge" style="background:var(--accent-violet);color:#fff;font-size:10px;">${planText}</span></td>
                    <td style="padding: 12px 24px; white-space: nowrap; font-variant-numeric: tabular-nums;">${tarifa}</td>
                    <td style="padding: 12px 24px; white-space: nowrap; font-weight:700; font-variant-numeric: tabular-nums;">${ltv}</td>
                    <td style="padding: 12px 8px; white-space: nowrap;">${estado}</td>
                </tr>
            `;"""

new_row_js = """            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft); transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 12px 24px 12px 8px; white-space: nowrap;"><strong style="font-size: 14px;">${m.business_name}</strong></td>
                    <td style="padding: 12px 24px; white-space: nowrap; font-weight:700; font-variant-numeric: tabular-nums; color: #10b981;">${ltv}</td>
                    <td style="padding: 12px 8px; white-space: nowrap; color: var(--text-muted);">${createdDate.toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' })}</td>
                </tr>
            `;"""
if old_row_js in js:
    js = js.replace(old_row_js, new_row_js)
else:
    print("WARNING: Could not find old row JS")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS logic patched.")
