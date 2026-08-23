import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace massive paddings in the table headers of the Control de Negocios tab
old_table = """                <div class="content-panel" style="background: #ffffff;  padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 2px solid #E5E7EB; color: #6B7280; font-size:12px; text-transform:uppercase;">
                                <th style="padding: 16px;">Negocio</th>
                                <th style="padding: 16px;">Plan Actual</th>
                                <th style="padding: 16px;">Días Restantes</th>
                                <th style="padding: 16px;">Estado Pago</th>
                                <th style="padding: 16px; text-align: right;">Acciones</th>
                            </tr>
                        </thead>
                        <tbody id="merchants-control-body">"""

new_table = """                <div class="content-panel" style="background: #ffffff; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left; table-layout: auto;">
                        <thead>
                            <tr style="border-bottom: 2px solid #E5E7EB; color: #6B7280; font-size:11px; text-transform:uppercase;">
                                <th style="padding: 12px 8px;">Negocio</th>
                                <th style="padding: 12px 8px; width: 120px;">Plan Actual</th>
                                <th style="padding: 12px 8px; width: 110px;">Días Restantes</th>
                                <th style="padding: 12px 8px; width: 130px;">Estado Pago</th>
                                <th style="padding: 12px 8px; text-align: right; width: 140px;">Acciones</th>
                            </tr>
                        </thead>
                        <tbody id="merchants-control-body">"""

html = html.replace(old_table, new_table)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace massive paddings in the table body of the Control de Negocios tab
old_js_row = """            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft);">
                    <td style="padding: 16px;"><strong>${m.business_name}</strong></td>
                    <td style="padding: 16px;">${planBadge}</td>
                    <td style="padding: 16px;">${daysLeft}</td>
                    <td style="padding: 16px;">${paymentStatus}</td>
                    <td style="padding: 16px; text-align: right;">
                        <button class="fidelio-btn-secondary-preset" onclick="openAdminMerchant('${m.id}')" style="background:var(--bg-main); color:var(--text-main); padding:6px 12px; font-size:12px; border:1px solid var(--border-soft);">
                            <i class="fa-solid fa-sliders"></i> Administrar
                        </button>
                    </td>
                </tr>
            `;"""

new_js_row = """            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft); transition: background 0.2s;" onmouseover="this.style.background='#f9fafb'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 12px 8px; max-width: 200px; white-space: normal; word-break: break-word;"><strong style="font-size: 14px;">${m.business_name}</strong></td>
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

js = js.replace(old_js_row, new_js_row)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Table padding fixed.")
