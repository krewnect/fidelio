import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_citas = r'<div class="builder-card plan-professional-only" style="margin-bottom:24px;">.*?<div class="premium-divider plan-professional-only"></div>'
replacement_citas = """<div class="builder-card plan-professional-only" style="margin-bottom:24px;">
                            <div class="premium-section-title"><i class="fa-solid fa-calendar-check" style="color:#8b5cf6;"></i> Integración de Citas y Pagos <span style="background:#8b5cf6; color:white; font-size:10px; padding:3px 8px; border-radius:6px; margin-left:8px; font-weight:bold; letter-spacing:1px;">PRO</span></div>
                            <p style="font-size:13px; color:#6b7280; margin-bottom:20px;">Añade botones interactivos directamente en la tarjeta Wallet para que tus clientes agenden o paguen con un solo toque.</p>
                            
                            <div style="display:flex; flex-direction:column; gap:16px;">
                                <div style="background:#f8fafc; padding:20px; border-radius:16px; border:1px solid #e2e8f0; display:flex; flex-direction:column; gap:12px;">
                                    <div>
                                        <label class="premium-label" style="font-weight:700; font-size:15px; margin-bottom:4px; display:block;"><i class="fa-regular fa-calendar-plus" style="color:#8b5cf6; margin-right:8px;"></i>Botón 'Agendar Cita'</label>
                                        <span style="font-size:12px; color:#94a3b8;">Habilita un link directo a tu sistema de reservas.</span>
                                    </div>
                                    <select id="builder-btn-appointment" class="premium-input" style="width:100%; background:white; font-weight:bold; color:#475569; border-color:#cbd5e1; font-size:14px; padding:12px;">
                                        <option value="no">No, ocultar botón</option>
                                        <option value="yes">Sí, habilitar botón de Agendar</option>
                                    </select>
                                </div>
                                <div style="background:#f8fafc; padding:20px; border-radius:16px; border:1px solid #e2e8f0; display:flex; flex-direction:column; gap:12px;">
                                    <div>
                                        <label class="premium-label" style="font-weight:700; font-size:15px; margin-bottom:4px; display:block;"><i class="fa-solid fa-credit-card" style="color:#10b981; margin-right:8px;"></i>Botón 'Pagar Cita'</label>
                                        <span style="font-size:12px; color:#94a3b8;">Permite cobrar adelantos o liquidar el servicio.</span>
                                    </div>
                                    <select id="builder-btn-payment" class="premium-input" style="width:100%; background:white; font-weight:bold; color:#475569; border-color:#cbd5e1; font-size:14px; padding:12px;">
                                        <option value="no">No, ocultar botón</option>
                                        <option value="yes">Sí, habilitar botón de Pago</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <div class="premium-divider plan-professional-only"></div>"""

html = re.sub(target_citas, replacement_citas, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
