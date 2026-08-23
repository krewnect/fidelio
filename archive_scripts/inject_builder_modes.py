import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

anchor = '<div class="apple-section">\n                            <div class="apple-section-header"><i class="fa-solid fa-hourglass-half"></i> Vigencia del Programa</div>'

new_blocks = """
                        <!-- MAGIC ENGINE: DISEÑO AVANZADO -->
                        <div class="apple-section plan-business-only">
                            <div class="apple-section-header" style="display:flex; justify-content:space-between; align-items:center;">
                                <span><i class="fa-solid fa-layer-group"></i> Arquitectura Visual (Magic Engine)</span>
                                <span class="menu-badge" style="font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff; border-radius: 4px;">BUSINESS</span>
                            </div>
                            
                            <div style="display: flex; flex-direction: column; gap: 16px;">
                                <div style="display: flex; flex-direction: column; gap: 8px;">
                                    <label class="apple-label">Formato (Morphing)</label>
                                    <select id="magic-shape-select" class="apple-input">
                                        <option value="store_card">Store Card (Clásica)</option>
                                        <option value="event_ticket">Event Ticket (Muescas Laterales)</option>
                                        <option value="boarding_pass">Boarding Pass (Muesca Superior)</option>
                                    </select>
                                </div>
                                
                                <div style="display: flex; flex-direction: column; gap: 8px;">
                                    <label class="apple-label">Ubicación del Código QR</label>
                                    <div style="display: flex; gap: 12px;">
                                        <label class="fidelio-btn-primary" style="flex: 1; margin: 0; cursor: pointer; background: #f8fafc !important; color: #111827 !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 12px !important;">
                                            <input type="radio" name="magic_qr_location" value="traditional" checked style="margin-right: 8px;">
                                            Modo Tradicional (Frente)
                                        </label>
                                        <label class="fidelio-btn-primary" style="flex: 1; margin: 0; cursor: pointer; background: #f8fafc !important; color: #111827 !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 12px !important;">
                                            <input type="radio" name="magic_qr_location" value="clean_nfc" style="margin-right: 8px;">
                                            Modo Limpio (Reverso)
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- MAGIC ENGINE: REVERSO INTERACTIVO -->
                        <div class="apple-section plan-business-only">
                            <div class="apple-section-header" style="display:flex; justify-content:space-between; align-items:center;">
                                <span><i class="fa-solid fa-mobile-screen"></i> Reverso Inteligente (Cuponera)</span>
                                <span class="menu-badge" style="font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff; border-radius: 4px;">BUSINESS</span>
                            </div>
                            <p style="font-size: 13px; color: #64748b; margin-bottom: 16px;">
                                El Magic Engine inyectará enlaces dinámicos y cupones promocionales directamente en el reverso de la tarjeta mediante Push Notifications.
                            </p>
                            <div style="display: flex; flex-direction: column; gap: 12px;">
                                <label style="display: flex; align-items: center; gap: 12px; cursor: pointer;">
                                    <input type="checkbox" id="magic-coupon-birthday" checked style="width: 18px; height: 18px; accent-color: #8b5cf6;">
                                    <span style="font-size: 14px; font-weight: 500; color: #1e293b;">Cupón Automático de Cumpleaños</span>
                                </label>
                                <label style="display: flex; align-items: center; gap: 12px; cursor: pointer;">
                                    <input type="checkbox" id="magic-coupon-anniversary" checked style="width: 18px; height: 18px; accent-color: #8b5cf6;">
                                    <span style="font-size: 14px; font-weight: 500; color: #1e293b;">Recordatorio de Aniversario de Registro</span>
                                </label>
                            </div>
                        </div>

"""

if anchor in html:
    html = html.replace(anchor, new_blocks + anchor)
    print("Injected new builder modes")
else:
    print("WARNING: Could not find anchor")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
