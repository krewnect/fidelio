import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the flash drop button with a configurable block
old_flashdrop_html = """<button type="button" onclick="testFlashDrop()" class="fidelio-btn-primary" style="background: #ef4444 !important; width: 100%;">
                                    <i class="fa-solid fa-bolt"></i> Disparar Flash Drop Masivo
                                </button>"""

new_flashdrop_html = """<div style="background: #fef2f2; padding: 16px; border-radius: 8px; border: 1px solid #fca5a5; margin-top: 16px;">
                                    <h4 style="font-size: 14px; font-weight: 700; color: #991b1b; margin-bottom: 8px;"><i class="fa-solid fa-bolt"></i> Disparar Flash Drop Masivo</h4>
                                    <p style="font-size: 12px; color: #b91c1c; margin-bottom: 12px;">Envía una oferta relámpago con tiempo límite a todos tus clientes activos.</p>
                                    
                                    <div style="margin-bottom: 12px;">
                                        <label class="apple-label" style="font-size: 11px; color: #991b1b;">Título de la Oferta</label>
                                        <input type="text" id="magic-flash-title" class="apple-input fidelio-input" placeholder="Ej. ¡Happy Hour de Locura!" value="¡Venta Relámpago!">
                                    </div>
                                    <div style="margin-bottom: 16px;">
                                        <label class="apple-label" style="font-size: 11px; color: #991b1b;">Mensaje Push / Condiciones</label>
                                        <input type="text" id="magic-flash-message" class="apple-input fidelio-input" placeholder="Ej. 50% de descuento en la próxima hora." value="Obtén 30% OFF si nos visitas en los próximos 60 minutos.">
                                    </div>
                                    
                                    <button type="button" onclick="testFlashDrop()" class="fidelio-btn-primary" style="background: #ef4444 !important; width: 100%; border-color: #ef4444 !important;">
                                        <i class="fa-solid fa-bolt"></i> Lanzar Flash Drop Ahora
                                    </button>
                                </div>"""

if "magic-flash-title" not in html:
    if old_flashdrop_html in html:
        html = html.replace(old_flashdrop_html, new_flashdrop_html)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Updated flash drop UI successfully.")
    else:
        print("Could not find the old flashdrop block to replace.")
else:
    print("Already updated.")
