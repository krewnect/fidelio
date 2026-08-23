import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_store = """            <!-- TIENDA FIDELIO TAB -->
            <section id="tab-store" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <div class="workspace-eyebrow">TIENDA</div>
                        <h1>Tienda Fidelio</h1>
                        <p>Adquiere equipos profesionales y descarga materiales gratuitos para tu negocio.</p>
                    </div>
                </div>

                <div class="content-panel" style="text-align: center; margin-bottom: 40px;">
                    <i class="fa-solid fa-boxes-packing" style="font-size: 3.5rem; color: var(--accent-violet); margin-bottom: 20px;"></i>
                    <h2 style="font-size: 1.8rem; margin-bottom: 12px; font-weight: 800;">Próximamente Disponible</h2>
                    <p style="color: var(--text-muted); max-width: 550px; margin: 0 auto; font-size: 1.1rem; line-height: 1.6;">Estamos preparando nuestro catálogo para que puedas equipar tu sucursal con la mejor tecnología de escaneo e impresión de materiales.</p>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 24px;">
                    <!-- Equipos y Accesorios -->
                    <div class="content-panel" style="position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 20px; right: 20px; background: rgba(139,92,246,0.1); color: var(--accent-violet); padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">PRÓXIMAMENTE</div>
                        <i class="fa-solid fa-mobile-screen-button" style="font-size: 2.5rem; color: var(--accent-violet); margin-bottom: 24px;"></i>
                        <h3 style="font-size: 1.4rem; margin-bottom: 16px; font-weight: 800;">Equipos y Accesorios</h3>
                        <p style="color: var(--text-muted); margin-bottom: 24px; font-size: 0.95rem; line-height: 1.5;">Adquiere hardware optimizado para leer los pases de Fidelio con la mayor velocidad.</p>
                        <ul style="color: var(--text-main); list-style: none; padding: 0; line-height: 2; margin-bottom: 30px; font-size: 0.95rem; font-weight: 600;">
                            <li><i class="fa-solid fa-check" style="color: var(--success); margin-right: 12px;"></i> Lectores NFC Profesionales</li>
                            <li><i class="fa-solid fa-check" style="color: var(--success); margin-right: 12px;"></i> Bases de metal y acrílico (QR)</li>
                            <li><i class="fa-solid fa-check" style="color: var(--success); margin-right: 12px;"></i> Tarjetas físicas NFC en PVC</li>
                        </ul>
                        <button class="btn btn-secondary btn-block" disabled style="opacity: 0.6; cursor: not-allowed; justify-content: center;"><i class="fa-solid fa-lock"></i> Ver Catálogo</button>
                    </div>

                    <!-- Materiales de Apoyo -->
                    <div class="content-panel" style="position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 20px; right: 20px; background: rgba(16, 185, 129, 0.1); color: var(--success); padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">GRATIS</div>
                        <i class="fa-solid fa-print" style="font-size: 2.5rem; color: var(--accent-violet); margin-bottom: 24px;"></i>
                        <h3 style="font-size: 1.4rem; margin-bottom: 16px; font-weight: 800;">Materiales de Apoyo</h3>
                        <p style="color: var(--text-muted); margin-bottom: 24px; font-size: 0.95rem; line-height: 1.5;">Explora y descarga distintos materiales personalizados listos para impresión, totalmente gratis para impulsar tu programa.</p>
                        <ul style="color: var(--text-main); list-style: none; padding: 0; line-height: 2; margin-bottom: 30px; font-size: 0.95rem; font-weight: 600;">
                            <li><i class="fa-solid fa-check" style="color: var(--success); margin-right: 12px;"></i> Diseños para Table Tents (Display)</li>
                            <li><i class="fa-solid fa-check" style="color: var(--success); margin-right: 12px;"></i> Formatos para Stickers y Calcomanías</li>
                            <li><i class="fa-solid fa-check" style="color: var(--success); margin-right: 12px;"></i> Flyers y Posters de Promoción</li>
                        </ul>
                        <button class="btn btn-primary btn-block" disabled style="opacity: 0.6; cursor: not-allowed; justify-content: center;"><i class="fa-solid fa-lock"></i> Ver Materiales</button>
                    </div>
                </div>"""

new_store = """            <!-- TIENDA FIDELIO TAB -->
            <section id="tab-store" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <div class="workspace-eyebrow">TIENDA & HARDWARE</div>
                        <h1>Tienda Fidelio</h1>
                        <p>Adquiere equipos profesionales y descarga materiales gratuitos para tu negocio.</p>
                    </div>
                </div>

                <!-- Premium Purple Banner -->
                <div class="metric-card-hover" style="background: linear-gradient(135deg, #7C3AED 0%, #4C1D95 100%); border-radius: 24px; padding: 56px 32px; color: white; display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 32px; box-shadow: 0 10px 30px rgba(124, 58, 237, 0.2); position: relative; overflow: hidden;">
                    <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255, 255, 255, 0.1); border-radius: 50%; filter: blur(50px);"></div>
                    <div style="width: 80px; height: 80px; background: rgba(255,255,255,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(10px); margin-bottom: 24px; box-shadow: inset 0 0 0 1px rgba(255,255,255,0.2);">
                        <i class="fa-solid fa-boxes-packing" style="font-size: 32px; color: white;"></i>
                    </div>
                    <h2 style="font-size: 28px; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.5px; color: white;">Próximamente Disponible</h2>
                    <p style="color: rgba(255,255,255,0.8); max-width: 600px; font-size: 16px; line-height: 1.6; margin: 0;">Estamos preparando un catálogo curado de hardware profesional de alto rendimiento y materiales de marketing para complementar tu programa de lealtad.</p>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 24px;">
                    <!-- Equipos y Accesorios -->
                    <div class="content-panel" style="position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="position: absolute; top: 32px; right: 32px; background: rgba(139,92,246,0.1); color: #7C3AED; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">PRÓXIMAMENTE</div>
                            <div style="width: 56px; height: 56px; background: #F3F4F6; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin-bottom: 24px;">
                                <i class="fa-solid fa-mobile-screen-button" style="font-size: 24px; color: #7C3AED;"></i>
                            </div>
                            <h3 style="font-size: 20px; margin-bottom: 12px; font-weight: 800; color: #111827;">Equipos y Accesorios</h3>
                            <p style="color: #6B7280; margin-bottom: 24px; font-size: 15px; line-height: 1.6;">Adquiere hardware optimizado para leer los pases de Fidelio con la mayor velocidad.</p>
                            <ul style="color: #4B5563; list-style: none; padding: 0; line-height: 2; margin-bottom: 32px; font-size: 14px; font-weight: 600;">
                                <li><i class="fa-solid fa-check" style="color: #10B981; margin-right: 12px;"></i> Lectores NFC Profesionales</li>
                                <li><i class="fa-solid fa-check" style="color: #10B981; margin-right: 12px;"></i> Bases de metal y acrílico (QR)</li>
                                <li><i class="fa-solid fa-check" style="color: #10B981; margin-right: 12px;"></i> Tarjetas físicas NFC en PVC</li>
                            </ul>
                        </div>
                        <button class="fidelio-btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed; width: 100%; justify-content: center; background: #F3F4F6; border: none; color: #9CA3AF;"><i class="fa-solid fa-lock"></i> Ver Catálogo</button>
                    </div>

                    <!-- Materiales de Apoyo -->
                    <div class="content-panel" style="position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="position: absolute; top: 32px; right: 32px; background: rgba(16, 185, 129, 0.1); color: #10B981; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">GRATIS</div>
                            <div style="width: 56px; height: 56px; background: #F3F4F6; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin-bottom: 24px;">
                                <i class="fa-solid fa-print" style="font-size: 24px; color: #7C3AED;"></i>
                            </div>
                            <h3 style="font-size: 20px; margin-bottom: 12px; font-weight: 800; color: #111827;">Materiales de Apoyo</h3>
                            <p style="color: #6B7280; margin-bottom: 24px; font-size: 15px; line-height: 1.6;">Explora y descarga distintos materiales personalizados listos para impresión, totalmente gratis para impulsar tu programa.</p>
                            <ul style="color: #4B5563; list-style: none; padding: 0; line-height: 2; margin-bottom: 32px; font-size: 14px; font-weight: 600;">
                                <li><i class="fa-solid fa-check" style="color: #10B981; margin-right: 12px;"></i> Diseños para Table Tents (Display)</li>
                                <li><i class="fa-solid fa-check" style="color: #10B981; margin-right: 12px;"></i> Formatos para Stickers y Calcomanías</li>
                                <li><i class="fa-solid fa-check" style="color: #10B981; margin-right: 12px;"></i> Flyers y Posters de Promoción</li>
                            </ul>
                        </div>
                        <button class="fidelio-btn-primary" disabled style="opacity: 0.5; cursor: not-allowed; width: 100%; justify-content: center;"><i class="fa-solid fa-lock"></i> Ver Materiales</button>
                    </div>
                </div>"""

html = html.replace(old_store, new_store)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
