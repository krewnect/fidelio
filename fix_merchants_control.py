import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract from <section id="tab-merchants-control" class="tab-content"> to </section>
pattern = r'(<section id="tab-merchants-control" class="tab-content">.*?)</section>'

replacement = """<section id="tab-merchants-control" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <div class="workspace-eyebrow">ADMINISTRACIÓN CENTRAL</div>
                        <h1>Control de Negocios</h1>
                        <p>Listado de restaurantes afiliados y estatus de sus suscripciones.</p>
                    </div>
                    <button class="fidelio-btn-primary" onclick="loadMerchantsControl()"><i class="fa-solid fa-rotate-right"></i> Actualizar Estatus</button>
                </div>
                
                <div class="content-panel" style="background: #ffffff; border-radius: 20px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
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
                        <tbody id="merchants-control-body">
                            <!-- Dynamic Content -->
                        </tbody>
                    </table>
                </div>
            """

# Do substitution
new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Restored tab-merchants-control")
