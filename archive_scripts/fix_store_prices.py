import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Card 1
html = html.replace(
    '<h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Lector NFC Fidelio Pro</h3>',
    '<h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Lectores NFC Inteligentes</h3>'
)
html = html.replace(
    '<p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Lectura de pases en milisegundos. Conexión WiFi y batería de 24 horas.</p>',
    '<p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Terminales dedicadas para lectura de pases en milisegundos sin necesidad de usar celulares.</p>'
)
html = html.replace(
    '<div style="display: flex; justify-content: space-between; align-items: center;">\n                            <span style="font-size: 18px; font-weight: 800; color: #111827;">$2,499<span style="font-size: 12px; color: #6B7280; font-weight: 500;"> MXN</span></span>\n                            <button class="fidelio-btn-secondary" disabled style="padding: 6px 16px !important; font-size: 12px !important; opacity: 0.5; cursor: not-allowed; min-width: 80px; text-align: center;">Agotado</button>\n                        </div>',
    '<button class="fidelio-btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed; width: 100%; justify-content: center; background: #F3F4F6; border: none; color: #9CA3AF;"><i class="fa-solid fa-lock"></i> Próximamente</button>'
)

# Card 2
html = html.replace(
    '<h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Base de Mostrador iPad</h3>',
    '<h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Bases de Mostrador</h3>'
)
html = html.replace(
    '<p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Acrílico sólido con cargador magnético integrado para tu punto de venta.</p>',
    '<p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Bases de acrílico y metal para colocar instrucciones o Códigos QR de registro en tu caja.</p>'
)
html = html.replace(
    '<div style="display: flex; justify-content: space-between; align-items: center;">\n                            <span style="font-size: 18px; font-weight: 800; color: #111827;">$1,299<span style="font-size: 12px; color: #6B7280; font-weight: 500;"> MXN</span></span>\n                            <button class="fidelio-btn-secondary" disabled style="padding: 6px 16px !important; font-size: 12px !important; opacity: 0.5; cursor: not-allowed; min-width: 80px; text-align: center;">Agotado</button>\n                        </div>',
    '<button class="fidelio-btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed; width: 100%; justify-content: center; background: #F3F4F6; border: none; color: #9CA3AF;"><i class="fa-solid fa-lock"></i> Próximamente</button>'
)

# Card 3
html = html.replace(
    '<div style="display: flex; justify-content: space-between; align-items: center;">\n                            <span style="font-size: 18px; font-weight: 800; color: #111827;">$899<span style="font-size: 12px; color: #6B7280; font-weight: 500;"> MXN</span></span>\n                            <button class="fidelio-btn-secondary" disabled style="padding: 6px 16px !important; font-size: 12px !important; opacity: 0.5; cursor: not-allowed; min-width: 80px; text-align: center;">Agotado</button>\n                        </div>',
    '<button class="fidelio-btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed; width: 100%; justify-content: center; background: #F3F4F6; border: none; color: #9CA3AF;"><i class="fa-solid fa-lock"></i> Próximamente</button>'
)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
