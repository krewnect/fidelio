import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = r'<!-- 4\. CITAS Y PAGOS \(PRO\) -->.*?<div class="apple-section plan-professional-only" style="background: linear-gradient\(135deg, #f8fafc, #f3e8ff\); padding: 24px; border-radius: 20px; border: 1px solid #e9d5ff;">.*?</div>\s*</div>'

replacement = """<!-- 4. CITAS Y PAGOS -->
                        <div class="apple-section plan-professional-only" style="background: #ffffff; padding: 0;">
                            <div class="apple-section-header"><i class="fa-solid fa-calendar-check"></i> Integración Wallet</div>
                            <p style="font-size:13px; color:#64748b; margin-bottom:20px; line-height:1.5;">Agrega botones interactivos al reverso de tu tarjeta para que tus clientes agenden o paguen con un toque.</p>
                            
                            <div style="display:flex; flex-direction:column; gap:12px;">
                                <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:16px 20px; border-radius:12px; border:1px solid #e2e8f0;">
                                    <label class="apple-label" style="margin-bottom:0; font-size:13px;"><i class="fa-regular fa-calendar-plus" style="margin-right:8px; color:#8b5cf6;"></i> Botón 'Agendar Cita'</label>
                                    <select id="builder-btn-appointment" class="apple-input" style="width:180px; padding:10px 14px; margin:0; background:white;">
                                        <option value="no">OFF (Oculto)</option>
                                        <option value="yes">ON (Visible)</option>
                                    </select>
                                </div>
                                
                                <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:16px 20px; border-radius:12px; border:1px solid #e2e8f0;">
                                    <label class="apple-label" style="margin-bottom:0; font-size:13px;"><i class="fa-solid fa-credit-card" style="margin-right:8px; color:#10b981;"></i> Botón 'Pagar Cita'</label>
                                    <select id="builder-btn-payment" class="apple-input" style="width:180px; padding:10px 14px; margin:0; background:white;">
                                        <option value="no">OFF (Oculto)</option>
                                        <option value="yes">ON (Visible)</option>
                                    </select>
                                </div>
                            </div>
                        </div>"""

html = re.sub(target, replacement, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
