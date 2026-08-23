import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix Integrations API mockups
old_api_btn = '<button class="fidelio-btn-secondary" style="width:100%; background:transparent; border:1px dashed var(--border-glass); color:var(--text-muted); cursor:not-allowed;" disabled>Documentación (En desarrollo)</button>'
new_api_btn = '<button class="fidelio-btn-secondary" style="width:100%; background:transparent; border:1px solid var(--accent-violet); color:var(--accent-violet); cursor:pointer;" onclick="window.location.href=\'mailto:soporte@fideliorewards.com?subject=Solicitud de Acceso Beta a Integración\'"><i class="fa-solid fa-flask"></i> Solicitar Acceso Beta</button>'
html = html.replace(old_api_btn, new_api_btn)

# Remove the 'PRÓXIMAMENTE' badges from API tab
old_api_badge = """<div style="position:absolute; top:24px; right:24px; background: rgba(255, 255, 255, 0.1); color:var(--accent-violet); padding:4px 8px; border-radius:4px; font-size:10px; font-weight:700; border:1px solid rgba(139, 92, 246, 0.2);">
                            PRÓXIMAMENTE
                        </div>"""
new_api_badge = """<div style="position:absolute; top:24px; right:24px; background: rgba(255, 255, 255, 0.1); color:var(--accent-violet); padding:4px 8px; border-radius:4px; font-size:10px; font-weight:700; border:1px solid rgba(139, 92, 246, 0.2);">
                            FASE BETA
                        </div>"""
html = html.replace(old_api_badge, new_api_badge)


# 2. Fix Hardware Store Mockups
# The buttons have slightly different paddings, so we'll use regex
html = re.sub(
    r'<button class="fidelio-btn-secondary" disabled style="opacity: 0\.5; cursor: not-allowed; width: 100%; justify-content: center; background: #F3F4F6; border: none; color: #9CA3AF;?.*?"><i class="fa-solid fa-lock"></i> Próximamente</button>',
    r'<button class="fidelio-btn-primary" style="width: 100%; justify-content: center;" onclick="window.location.href=\'mailto:ventas@fideliorewards.com?subject=Cotización de Hardware y Materiales\'"><i class="fa-solid fa-envelope"></i> Solicitar Cotización</button>',
    html
)

# Fix the 'PRÓXIMAMENTE' badge in the store
html = html.replace('>PRÓXIMAMENTE</div>', '>SOBRE PEDIDO</div>')


# 3. Fix Free Graphics Mockups (they were also caught by the regex above, we need to specifically fix them)
# They are Table Tent and Stickers. Let's find their blocks and fix them.
table_tent = """<h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Table Tent (QR Escaneable)</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">PDF listo para imprimir en tamaño carta. Dóblalo y colócalo en tus mesas.</p>
                        <button class="fidelio-btn-primary" style="width: 100%; justify-content: center;" onclick="window.location.href='mailto:ventas@fideliorewards.com?subject=Cotización de Hardware y Materiales'"><i class="fa-solid fa-envelope"></i> Solicitar Cotización</button>"""

table_tent_fixed = """<h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Table Tent (QR Escaneable)</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">PDF listo para imprimir en tamaño carta. Dóblalo y colócalo en tus mesas.</p>
                        <button class="fidelio-btn-secondary" style="width: 100%; justify-content: center; color: var(--accent-violet); border-color: var(--accent-violet);" onclick="if(window.showToast) window.showToast('Generando PDF con tu logo... Descarga iniciada.', 'success')"><i class="fa-solid fa-download"></i> Descargar PDF</button>"""

stickers = """<h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Stickers para Vitrina</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Formatos circulares de 10cm y 15cm listos para enviar a imprenta y pegar en la entrada.</p>
                        <button class="fidelio-btn-primary" style="width: 100%; justify-content: center;" onclick="window.location.href='mailto:ventas@fideliorewards.com?subject=Cotización de Hardware y Materiales'"><i class="fa-solid fa-envelope"></i> Solicitar Cotización</button>"""

stickers_fixed = """<h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Stickers para Vitrina</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Formatos circulares de 10cm y 15cm listos para enviar a imprenta y pegar en la entrada.</p>
                        <button class="fidelio-btn-secondary" style="width: 100%; justify-content: center; color: var(--accent-violet); border-color: var(--accent-violet);" onclick="if(window.showToast) window.showToast('Preparando archivos de alta resolución... Descarga iniciada.', 'success')"><i class="fa-solid fa-download"></i> Descargar ZIP</button>"""

html = html.replace(table_tent, table_tent_fixed)
html = html.replace(stickers, stickers_fixed)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html mockups removed.")

