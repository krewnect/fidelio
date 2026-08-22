import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

deep_tech_html = """
                        <!-- MAGIC ENGINE: DEEP TECH -->
                        <div class="apple-section plan-business-only">
                            <div class="apple-section-header" style="display:flex; justify-content:space-between; align-items:center;">
                                <span><i class="fa-solid fa-microchip"></i> Fidelio Deep Tech</span>
                                <span class="menu-badge" style="font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #0f172a, #1e293b); color: #fff; border-radius: 4px; border: 1px solid #334155;">ENTERPRISE</span>
                            </div>
                            <p style="font-size: 13px; color: #64748b; margin-bottom: 16px;">
                                Tecnologías de frontera exclusivas de Fidelio para operaciones de misión crítica y experiencias zero-friction.
                            </p>
                            <div style="display: flex; flex-direction: column; gap: 12px;">
                                <label style="display: flex; align-items: flex-start; gap: 12px; cursor: pointer; padding: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;">
                                    <input type="checkbox" id="deep-tech-immortal" style="width: 18px; height: 18px; accent-color: #0f172a; margin-top: 2px;">
                                    <div>
                                        <span style="font-size: 14px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 2px;"><i class="fa-solid fa-barcode"></i> Pase Inmortal (Offline Survival)</span>
                                        <span style="font-size: 12px; color: #475569; display: block; line-height: 1.4;">Inyecta la base de datos (puntos, nivel, ID) dentro de los píxeles de la tarjeta usando esteganografía. Permite escanear a clientes sin necesidad de conexión a internet.</span>
                                    </div>
                                </label>
                                
                                <label style="display: flex; align-items: flex-start; gap: 12px; cursor: pointer; padding: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;">
                                    <input type="checkbox" id="deep-tech-sonic" style="width: 18px; height: 18px; accent-color: #0f172a; margin-top: 2px;">
                                    <div>
                                        <span style="font-size: 14px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 2px;"><i class="fa-solid fa-wave-square"></i> Check-In Supersónico (Zero-Scan)</span>
                                        <span style="font-size: 12px; color: #475569; display: block; line-height: 1.4;">Activa el handshake inaudible. Las bocinas del local y el micrófono del celular del cliente se comunican por ultrasonido para registrar la visita sin sacar el celular del bolsillo.</span>
                                    </div>
                                </label>
                                
                                <label style="display: flex; align-items: flex-start; gap: 12px; cursor: pointer; padding: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;">
                                    <input type="checkbox" id="deep-tech-geo" style="width: 18px; height: 18px; accent-color: #0f172a; margin-top: 2px;">
                                    <div>
                                        <span style="font-size: 14px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 2px;"><i class="fa-solid fa-earth-americas"></i> Infinite-Geo (Geocercas Rotativas)</span>
                                        <span style="font-size: 12px; color: #475569; display: block; line-height: 1.4;">El Magic Engine rotará dinámicamente las 10 ubicaciones permitidas por Apple Wallet basándose en el GPS en vivo, otorgando geocercas infinitas a nivel nacional.</span>
                                    </div>
                                </label>
                            </div>
                        </div>
"""

# Insert right after the Autopilot section
# Wait, the autopilot section ends with the flash drop button
search_str = """                                    <button type="button" onclick="testFlashDrop()" class="fidelio-btn-primary" style="background: #ef4444 !important; width: 100%; border-color: #ef4444 !important;">
                                        <i class="fa-solid fa-bolt"></i> Lanzar Flash Drop Ahora
                                    </button>
                                </div>"""

if "Fidelio Deep Tech" not in html:
    html = html.replace(search_str, search_str + "\n" + deep_tech_html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected Deep Tech Section.")
else:
    print("Already injected.")
