import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Completely strip all forced widths, colgroups, and 100% width. Let the table naturally wrap its content with a standard padding.
old_table = """                <div class="content-panel" style="background: #ffffff; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left; table-layout: fixed;">
                        <colgroup>
                            <col style="width: 250px;">
                            <col style="width: 140px;">
                            <col style="width: 140px;">
                            <col style="width: 140px;">
                            <col style="width: auto;">
                        </colgroup>
                        <thead>
                            <tr style="border-bottom: 2px solid #E5E7EB; color: #6B7280; font-size:11px; text-transform:uppercase;">
                                <th style="padding: 12px 8px;">Negocio</th>
                                <th style="padding: 12px 8px;">Plan Actual</th>
                                <th style="padding: 12px 8px;">Días Restantes</th>
                                <th style="padding: 12px 8px;">Estado Pago</th>
                                <th style="padding: 12px 8px; text-align: right;">Acciones</th>
                            </tr>
                        </thead>"""

new_table = """                <div class="content-panel" style="background: #ffffff; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
                    <table class="crm-table" style="width: max-content; border-collapse: collapse; text-align: left; table-layout: auto; white-space: nowrap;">
                        <thead>
                            <tr style="border-bottom: 2px solid #E5E7EB; color: #6B7280; font-size:11px; text-transform:uppercase;">
                                <th style="padding: 12px 24px 12px 8px;">Negocio</th>
                                <th style="padding: 12px 24px;">Plan Actual</th>
                                <th style="padding: 12px 24px;">Días Restantes</th>
                                <th style="padding: 12px 24px;">Estado Pago</th>
                                <th style="padding: 12px 8px;">Acciones</th>
                            </tr>
                        </thead>"""

if old_table in html:
    html = html.replace(old_table, new_table)
else:
    print("WARNING: Could not find old table HTML")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_js_row = """            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft); transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 12px 8px; white-space: normal; word-break: break-word;"><strong style="font-size: 14px;">${m.business_name}</strong></td>
                    <td style="padding: 12px 8px;">${planBadge}</td>
                    <td style="padding: 12px 8px; font-variant-numeric: tabular-nums;">${daysLeft}</td>
                    <td style="padding: 12px 8px;">${paymentStatus}</td>
                    <td style="padding: 12px 8px; text-align: right;">
                        <button class="fidelio-btn-secondary-preset" onclick="document.getElementById('modal-admin-merchant').style.display='flex'; openAdminMerchant('${m.id}')" style="background:var(--bg-main); color:var(--text-main); padding:6px 12px; font-size:12px; border:1px solid var(--border-soft);">
                            <i class="fa-solid fa-sliders"></i> Administrar
                        </button>
                    </td>
                </tr>
            `;"""

new_js_row = """            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft); transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 12px 24px 12px 8px; white-space: nowrap;"><strong style="font-size: 14px;">${m.business_name}</strong></td>
                    <td style="padding: 12px 24px; white-space: nowrap;">${planBadge}</td>
                    <td style="padding: 12px 24px; white-space: nowrap; font-variant-numeric: tabular-nums;">${daysLeft}</td>
                    <td style="padding: 12px 24px; white-space: nowrap;">${paymentStatus}</td>
                    <td style="padding: 12px 8px; white-space: nowrap;">
                        <button class="fidelio-btn-secondary-preset" onclick="document.getElementById('modal-admin-merchant').style.display='flex'; openAdminMerchant('${m.id}')" style="background:var(--bg-main); color:var(--text-main); padding:6px 12px; font-size:12px; border:1px solid var(--border-soft);">
                            <i class="fa-solid fa-sliders"></i> Administrar
                        </button>
                    </td>
                </tr>
            `;"""

if old_js_row in js:
    js = js.replace(old_js_row, new_js_row)
else:
    print("WARNING: Could not find old JS row")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Final fix deployed.")
