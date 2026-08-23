import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the table strictly packed to the left by removing width 100% from Negocio and giving it to Acciones, or just fixed widths.
old_table = """                <div class="content-panel" style="background: #ffffff; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left; table-layout: auto; white-space: nowrap;">
                        <thead>
                            <tr style="border-bottom: 2px solid #E5E7EB; color: #6B7280; font-size:11px; text-transform:uppercase;">
                                <th style="padding: 12px 8px; width: 100%; white-space: normal;">Negocio</th>
                                <th style="padding: 12px 8px;">Plan Actual</th>
                                <th style="padding: 12px 8px;">Días Restantes</th>
                                <th style="padding: 12px 8px;">Estado Pago</th>
                                <th style="padding: 12px 8px; text-align: right;">Acciones</th>
                            </tr>
                        </thead>"""

new_table = """                <div class="content-panel" style="background: #ffffff; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
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

html = html.replace(old_table, new_table)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Table packed successfully using colgroup")
