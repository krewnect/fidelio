import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                        <!-- 4. CITAS Y PAGOS -->
                        <div class="apple-section plan-professional-only" style="background: #ffffff; padding: 0;">
                            <div class="apple-section-header"><i class="fa-solid fa-calendar-check"></i> Integración Wallet</div>"""

replacement = """                        <!-- 4. VIGENCIA Y CADUCIDAD -->
                        <div class="apple-section">
                            <div class="apple-section-header"><i class="fa-solid fa-hourglass-half"></i> Vigencia del Programa</div>
                            <p style="font-size:13px; color:#64748b; margin-bottom:20px; line-height:1.5;">Configura si este programa tiene una fecha de cierre o si el premio caduca después de un tiempo.</p>
                            
                            <div style="display:flex; gap:16px;">
                                <div class="apple-input-group" style="flex:1;">
                                    <label class="apple-label">Vigencia de la Campaña (Opcional)</label>
                                    <input type="date" id="camp-valid-until" class="apple-input">
                                    <div style="font-size:11px; color:#94a3b8; margin-top:4px;">Dejar vacío para que no caduque nunca.</div>
                                </div>
                                <div class="apple-input-group" style="flex:1;">
                                    <label class="apple-label">Tiempo para redimir premio (Días)</label>
                                    <input type="number" id="camp-grace-period" class="apple-input" value="" min="1" placeholder="Ej. 15">
                                    <div style="font-size:11px; color:#94a3b8; margin-top:4px;">Días de tolerancia si termina la campaña.</div>
                                </div>
                            </div>
                        </div>

                        <!-- 5. CITAS Y PAGOS -->
                        <div class="apple-section plan-professional-only" style="background: #ffffff; padding: 0;">
                            <div class="apple-section-header"><i class="fa-solid fa-calendar-check"></i> Integración Wallet</div>"""

if target in html:
    html = html.replace(target, replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added Section 4")
else:
    print("Target not found")
