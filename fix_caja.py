import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix saveCajaTransaction button
html = html.replace('<button class="fidelio-btn-primary"><i class="fa-solid fa-check"></i> Guardar Pago</button>', '<button class="fidelio-btn-primary" onclick="saveCajaTransaction()"><i class="fa-solid fa-check"></i> Guardar Pago</button>')

# Fix Special Cards emission layout
old_special_buttons = """                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                        <button class="fidelio-btn-secondary" style="color:#25D366; border-color:#25D366;" onclick="window.emitirEspecial('whatsapp')">
                            <i class="fa-brands fa-whatsapp"></i> Enviar por WhatsApp
                        </button>
                        <button class="fidelio-btn-secondary" style="color:var(--accent-violet); border-color:var(--accent-violet);" onclick="window.emitirEspecial('email')">
                            <i class="fa-solid fa-envelope"></i> Enviar por Email
                        </button>
                        <button class="fidelio-btn-secondary" style="color:var(--text-main); border-color:var(--border-glass);" onclick="window.emitirEspecial('link')">
                            <i class="fa-solid fa-link"></i> Generar Enlace Único
                        </button>
                    </div>"""

new_special_buttons = """                    <div id="special-card-pre-payment">
                        <button class="fidelio-btn-primary" style="width:100%; margin-bottom: 24px; padding: 16px; font-size: 16px;" onclick="window.requireSpecialCardPayment()">
                            <i class="fa-solid fa-cash-register"></i> 1. Registrar Pago en Caja (Obligatorio)
                        </button>
                    </div>
                    
                    <div id="special-card-emission-buttons" style="display:none; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
                        <div style="grid-column: 1 / -1; font-size: 14px; color: #10b981; text-align: center; margin-bottom: 8px; font-weight: bold;">
                            <i class="fa-solid fa-check-circle"></i> ¡Pago registrado! Ahora puedes emitir la tarjeta.
                        </div>
                        <button class="fidelio-btn-secondary" style="color:#25D366; border-color:#25D366;" onclick="window.emitirEspecial('whatsapp')">
                            <i class="fa-brands fa-whatsapp"></i> Enviar por WhatsApp
                        </button>
                        <button class="fidelio-btn-secondary" style="color:var(--accent-violet); border-color:var(--accent-violet);" onclick="window.emitirEspecial('email')">
                            <i class="fa-solid fa-envelope"></i> Enviar por Email
                        </button>
                        <button class="fidelio-btn-secondary" style="color:var(--text-main); border-color:var(--border-glass);" onclick="window.emitirEspecial('link')">
                            <i class="fa-solid fa-link"></i> Generar Enlace Único
                        </button>
                    </div>"""

if old_special_buttons in html:
    html = html.replace(old_special_buttons, new_special_buttons)
else:
    print("WARNING: Exact match failed for special buttons")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML updated.")
