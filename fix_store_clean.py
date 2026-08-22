import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- TIENDA FIDELIO TAB -->'
end_marker = '<!-- EQUIPO FIDELIO (SUPER ADMIN ONLY) -->'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

new_store = """<!-- TIENDA FIDELIO TAB -->
            <section id="tab-store" class="tab-content">
                <div class="workspace-header" style="margin-bottom: 40px; border-bottom: 1px solid #E5E7EB; padding-bottom: 24px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-end; width:100%; flex-wrap: wrap; gap: 16px;">
                        <div>
                            <div class="workspace-eyebrow">HARDWARE & MATERIALES</div>
                            <h1 style="font-size: 32px; font-weight: 800; letter-spacing: -1px; color: #111827; margin: 8px 0;">Tienda Fidelio</h1>
                            <p style="color: #6B7280; font-size: 16px; margin: 0; max-width: 600px;">Adquiere equipo optimizado para escaneo ultra rápido y material promocional oficial para tu negocio.</p>
                        </div>
                        <div style="background: rgba(139, 92, 246, 0.1); color: #7C3AED; padding: 8px 16px; border-radius: 20px; font-weight: 700; font-size: 13px; display:flex; align-items:center; gap:8px;">
                            <i class="fa-solid fa-clock"></i> Lanzamiento: Q4 2026
                        </div>
                    </div>
                </div>

                <h2 style="font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 20px; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-microchip" style="color:#8B5CF6;"></i> Terminales y Lectores NFC</h2>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 24px; margin-bottom: 48px;">
                    
                    <!-- Product 1 -->
                    <div class="content-panel" style="padding: 24px !important; display: flex; flex-direction: column; opacity: 0.8; transition: transform 0.2s; cursor: pointer;">
                        <div style="background: #F3F4F6; border-radius: 16px; height: 180px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; position: relative;">
                            <i class="fa-solid fa-mobile-screen" style="font-size: 64px; color: #D1D5DB;"></i>
                            <div style="position: absolute; top: 12px; right: 12px; background: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 800; color: #9CA3AF; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">PRÓXIMAMENTE</div>
                        </div>
                        <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Lector NFC Fidelio Pro</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Lectura de pases en milisegundos. Conexión WiFi y batería de 24 horas.</p>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 18px; font-weight: 800; color: #111827;">$2,499<span style="font-size: 12px; color: #6B7280; font-weight: 500;"> MXN</span></span>
                            <button class="fidelio-btn-secondary" disabled style="padding: 6px 16px !important; font-size: 12px !important; opacity: 0.5; cursor: not-allowed; min-width: 80px; text-align: center;">Agotado</button>
                        </div>
                    </div>

                    <!-- Product 2 -->
                    <div class="content-panel" style="padding: 24px !important; display: flex; flex-direction: column; opacity: 0.8; transition: transform 0.2s; cursor: pointer;">
                        <div style="background: #F3F4F6; border-radius: 16px; height: 180px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; position: relative;">
                            <i class="fa-solid fa-tablet-screen-button" style="font-size: 64px; color: #D1D5DB;"></i>
                            <div style="position: absolute; top: 12px; right: 12px; background: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 800; color: #9CA3AF; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">PRÓXIMAMENTE</div>
                        </div>
                        <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Base de Mostrador iPad</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Acrílico sólido con cargador magnético integrado para tu punto de venta.</p>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 18px; font-weight: 800; color: #111827;">$1,299<span style="font-size: 12px; color: #6B7280; font-weight: 500;"> MXN</span></span>
                            <button class="fidelio-btn-secondary" disabled style="padding: 6px 16px !important; font-size: 12px !important; opacity: 0.5; cursor: not-allowed; min-width: 80px; text-align: center;">Agotado</button>
                        </div>
                    </div>

                    <!-- Product 3 -->
                    <div class="content-panel" style="padding: 24px !important; display: flex; flex-direction: column; opacity: 0.8; transition: transform 0.2s; cursor: pointer;">
                        <div style="background: #F3F4F6; border-radius: 16px; height: 180px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; position: relative;">
                            <i class="fa-solid fa-credit-card" style="font-size: 64px; color: #D1D5DB;"></i>
                            <div style="position: absolute; top: 12px; right: 12px; background: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 800; color: #9CA3AF; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">PRÓXIMAMENTE</div>
                        </div>
                        <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Tarjetas Físicas NFC (x100)</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Para clientes que prefieren el plástico. Personalizadas con tu logo.</p>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 18px; font-weight: 800; color: #111827;">$899<span style="font-size: 12px; color: #6B7280; font-weight: 500;"> MXN</span></span>
                            <button class="fidelio-btn-secondary" disabled style="padding: 6px 16px !important; font-size: 12px !important; opacity: 0.5; cursor: not-allowed; min-width: 80px; text-align: center;">Agotado</button>
                        </div>
                    </div>
                </div>

                <h2 style="font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 20px; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-swatchbook" style="color:#8B5CF6;"></i> Material Gráfico Gratuito</h2>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 24px; margin-bottom: 48px;">
                    
                    <div class="content-panel" style="padding: 24px !important; display: flex; flex-direction: column; transition: transform 0.2s; cursor: pointer;">
                        <div style="background: #F5F3FF; border-radius: 16px; height: 140px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; position: relative;">
                            <i class="fa-solid fa-qrcode" style="font-size: 48px; color: #8B5CF6;"></i>
                            <div style="position: absolute; top: 12px; right: 12px; background: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 800; color: #10B981; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">GRATIS</div>
                        </div>
                        <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Table Tent (QR Escaneable)</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">PDF listo para imprimir en tamaño carta. Dóblalo y colócalo en tus mesas.</p>
                        <button class="fidelio-btn-primary" style="width: 100%; justify-content: center; padding: 10px !important;"><i class="fa-solid fa-cloud-arrow-down"></i> Descargar PDF</button>
                    </div>

                    <div class="content-panel" style="padding: 24px !important; display: flex; flex-direction: column; transition: transform 0.2s; cursor: pointer;">
                        <div style="background: #F5F3FF; border-radius: 16px; height: 140px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; position: relative;">
                            <i class="fa-solid fa-note-sticky" style="font-size: 48px; color: #8B5CF6;"></i>
                            <div style="position: absolute; top: 12px; right: 12px; background: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 800; color: #10B981; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">GRATIS</div>
                        </div>
                        <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 8px 0;">Stickers para Vitrina</h3>
                        <p style="font-size: 13px; color: #6B7280; margin: 0 0 16px 0; line-height: 1.5; flex: 1;">Formatos circulares de 10cm y 15cm listos para enviar a imprenta y pegar en la entrada.</p>
                        <button class="fidelio-btn-primary" style="width: 100%; justify-content: center; padding: 10px !important;"><i class="fa-solid fa-cloud-arrow-down"></i> Descargar PDF</button>
                    </div>

                </div>
            </section>
            
            """

html = html[:start_idx] + new_store + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
