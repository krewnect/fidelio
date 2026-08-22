import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Inject the Historial de Pagos table after the Cuentas Vencidas grid
old_html = """                        <div id="morosos-list" style="max-height: 250px; overflow-y: auto; padding-right: 10px;">
                            <!-- Dynamic Content -->
                            <div style="text-align: center; color: var(--text-muted); padding: 20px;">Cargando estado financiero...</div>
                        </div>
                    </div>
                </div>
            </section>"""

new_html = """                        <div id="morosos-list" style="max-height: 250px; overflow-y: auto; padding-right: 10px;">
                            <!-- Dynamic Content -->
                            <div style="text-align: center; color: var(--text-muted); padding: 20px;">Cargando estado financiero...</div>
                        </div>
                    </div>
                </div>

                <!-- Historial de Pagos -->
                <div class="content-panel" style="margin-top: 24px; background: #ffffff; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
                        <h3 style="font-size: 1.4rem; font-weight: 800;"><i class="fa-solid fa-file-invoice-dollar" style="color:#10b981;"></i> Historial de Pagos (Suscripciones)</h3>
                        <button class="fidelio-btn-secondary" onclick="loadBillingHistory()"><i class="fa-solid fa-rotate-right"></i> Actualizar</button>
                    </div>
                    <table class="crm-table" style="width: max-content; border-collapse: collapse; text-align: left; table-layout: auto; white-space: nowrap;">
                        <thead>
                            <tr style="border-bottom: 2px solid #E5E7EB; color: #6B7280; font-size:11px; text-transform:uppercase;">
                                <th style="padding: 12px 24px 12px 8px;">Negocio</th>
                                <th style="padding: 12px 24px;">Fecha Registro</th>
                                <th style="padding: 12px 24px;">Plan Actual</th>
                                <th style="padding: 12px 24px;">Tarifa Vigente</th>
                                <th style="padding: 12px 24px;">Estimado Pagado (LTV)</th>
                                <th style="padding: 12px 8px;">Estado Pago</th>
                            </tr>
                        </thead>
                        <tbody id="billing-history-body">
                            <!-- Dynamic Content -->
                            <tr><td colspan="6" style="padding: 24px; text-align: center; color: var(--text-muted);">Cargando historial de pagos...</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>"""

if old_html in html:
    html = html.replace(old_html, new_html)
else:
    print("WARNING: Could not find HTML injection point")

# Inject call to loadBillingHistory in the sidebar click
old_menu = """onclick="showTab('tab-master-admin'); document.querySelectorAll('.fidelio-sidebar li').forEach(el=>el.classList.remove('active')); this.parentElement.classList.add('active');" """
new_menu = """onclick="showTab('tab-master-admin'); document.querySelectorAll('.fidelio-sidebar li').forEach(el=>el.classList.remove('active')); this.parentElement.classList.add('active'); if(typeof loadBillingHistory === 'function') loadBillingHistory();" """
html = html.replace(old_menu, new_menu)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML patched.")
