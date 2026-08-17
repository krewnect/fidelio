import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I want to insert the tutorials right after the main banner and before the grid
tutorials_html = """
                <!-- TUTORIALES NUEVOS -->
                <div style="margin-bottom: 32px; max-width: 1000px;">
                    <h3 style="font-size: 1.1rem; margin-bottom: 15px; font-weight: 700;">Tutoriales de Nuevas Funciones</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px;">
                        
                        <div class="content-panel" style="background: var(--surface); border-radius: 16px; padding: 15px; cursor: pointer; transition: all 0.2s; border: 1px solid var(--border-soft);" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-soft)'" onclick="alert('Abriendo tutorial de Campañas IA...')">
                            <div style="background: linear-gradient(135deg, rgba(139,92,246,0.2) 0%, rgba(0,0,0,0) 100%); height: 120px; border-radius: 10px; margin-bottom: 12px; display: flex; align-items: center; justify-content: center;">
                                <i class="fa-solid fa-robot" style="font-size: 30px; color: var(--primary);"></i>
                            </div>
                            <h4 style="font-size: 14px; margin: 0 0 5px 0;">Cómo usar Campañas IA</h4>
                            <p style="font-size: 12px; color: var(--text-muted); margin: 0;">Aprende a usar el copiloto para crear promociones automáticas.</p>
                        </div>
                        
                        <div class="content-panel" style="background: var(--surface); border-radius: 16px; padding: 15px; cursor: pointer; transition: all 0.2s; border: 1px solid var(--border-soft);" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-soft)'" onclick="alert('Abriendo tutorial de 8 Programas...')">
                            <div style="background: linear-gradient(135deg, rgba(16,185,129,0.2) 0%, rgba(0,0,0,0) 100%); height: 120px; border-radius: 10px; margin-bottom: 12px; display: flex; align-items: center; justify-content: center;">
                                <i class="fa-solid fa-tags" style="font-size: 30px; color: #10b981;"></i>
                            </div>
                            <h4 style="font-size: 14px; margin: 0 0 5px 0;">Los 8 Programas (Cupones)</h4>
                            <p style="font-size: 12px; color: var(--text-muted); margin: 0;">Configura tarjetas de descuento, sellos, o membresías.</p>
                        </div>
                        
                        <div class="content-panel" style="background: var(--surface); border-radius: 16px; padding: 15px; cursor: pointer; transition: all 0.2s; border: 1px solid var(--border-soft);" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-soft)'" onclick="alert('Abriendo tutorial de Citas y Stripe...')">
                            <div style="background: linear-gradient(135deg, rgba(245,158,11,0.2) 0%, rgba(0,0,0,0) 100%); height: 120px; border-radius: 10px; margin-bottom: 12px; display: flex; align-items: center; justify-content: center;">
                                <i class="fa-solid fa-calendar-check" style="font-size: 30px; color: #f59e0b;"></i>
                            </div>
                            <h4 style="font-size: 14px; margin: 0 0 5px 0;">Citas Médicas y Stripe</h4>
                            <p style="font-size: 12px; color: var(--text-muted); margin: 0;">Gestiona tu agenda y cobra anticipos con Payment Links.</p>
                        </div>
                        
                        <div class="content-panel" style="background: var(--surface); border-radius: 16px; padding: 15px; cursor: pointer; transition: all 0.2s; border: 1px solid var(--border-soft);" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border-soft)'" onclick="alert('Abriendo tutorial de Súper Admin...')">
                            <div style="background: linear-gradient(135deg, rgba(59,130,246,0.2) 0%, rgba(0,0,0,0) 100%); height: 120px; border-radius: 10px; margin-bottom: 12px; display: flex; align-items: center; justify-content: center;">
                                <i class="fa-solid fa-headset" style="font-size: 30px; color: #3b82f6;"></i>
                            </div>
                            <h4 style="font-size: 14px; margin: 0 0 5px 0;">Uso del Inbox de Soporte</h4>
                            <p style="font-size: 12px; color: var(--text-muted); margin: 0;">Atiende a tus clientes estilo Zendesk en la zona Admin.</p>
                        </div>
                        
                    </div>
                </div>
"""

# Insert after the banner styling
target = "</style>\n                </div>"
if target in html and "TUTORIALES NUEVOS" not in html:
    html = html.replace(target, target + "\n\n" + tutorials_html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Tutorials added to Soporte tab")
else:
    print("Tutorials already exist or target not found")
