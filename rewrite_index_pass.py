import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will find the block <div class="card-3d-scene"> and replace everything inside it up to its closing tag.
# Let's just find the whole pass-render div.

start_str = '<!-- THE PASS -->'
end_str = '<!-- END THE PASS -->' # Assuming I can find the end of the scene. Wait, I didn't add an END comment.

# Find start
start_idx = html.find(start_str)
# Find the next section '<!-- BUILDER CONTROLS -->'
end_idx = html.find('<!-- SECTIONS FOR BUILDER -->')

if start_idx == -1 or end_idx == -1:
    print(f"Could not find boundaries. start={start_idx}, end={end_idx}")
    exit(1)

new_pass_html = """<!-- THE PASS -->
                                <div class="card-3d-scene" style="perspective: 1000px; display: flex; justify-content: center; align-items: center; padding: 20px;">
                                    <div class="card-3d-object" id="pass-render" style="width: 100%; max-width: 360px; position: relative; transition: transform 0.6s; transform-style: preserve-3d;">
                                        
                                        <!-- FRONT OF CARD -->
                                        <div class="card-face card-front pass-preview-card premium-white-card" style="background: #ffffff; border-radius: 16px; padding: 24px; position: relative; overflow: hidden; box-shadow: 0 12px 30px rgba(0,0,0,0.08); display: flex; flex-direction: column; min-height: 240px; backface-visibility: hidden; border: 2px solid var(--pass-primary, #8b5cf6);">
                                            
                                            <!-- Top row: Logo and "10 SELLOS" -->
                                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                                                <div class="pass-logo-container" style="flex: 1; max-width: 140px; display: flex; align-items: center;">
                                                    <img id="render-custom-logo" src="" style="width: 100%; max-height: 45px; object-fit: contain; display: none; object-position: left center;" />
                                                    <div id="render-default-logo" style="display: flex; align-items: center; gap: 8px;">
                                                        <i class="fa-solid fa-crown" id="render-icon" style="color: var(--pass-primary, #8b5cf6); font-size: 24px;"></i>
                                                        <span id="render-name" style="font-weight: 800; font-size: 18px; color: #111827; letter-spacing: -0.5px;">Fidelio</span>
                                                    </div>
                                                </div>
                                                <div id="render-top-right" style="text-align: right; display: flex; align-items: center; gap: 6px;">
                                                    <span id="render-top-right-text" style="font-size: 11px; font-weight: 700; color: var(--pass-primary, #8b5cf6); text-transform: uppercase;">10 SELLOS</span>
                                                    <i class="fa-solid fa-wifi" style="transform: rotate(90deg); color: var(--pass-primary, #8b5cf6); opacity: 0.8;"></i>
                                                </div>
                                            </div>

                                            <!-- Middle Body (Dynamic: Stamps vs Cashback) -->
                                            <div id="render-body-stamps" style="display: flex; flex-direction: column; flex-grow: 1;">
                                                <div style="font-size: 10px; font-weight: 600; color: #6b7280; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.5px;">ACUMULA <span id="render-stamps-total-text">10</span> SELLOS<br>Y OBTÉN TU RECOMPENSA</div>
                                                
                                                <!-- Stamps Grid -->
                                                <div id="render-stamps-grid" style="display: flex; flex-wrap: wrap; gap: 12px 10px; position: relative;">
                                                    <!-- Generated via JS -->
                                                </div>
                                            </div>

                                            <div id="render-body-cashback" style="display: none; flex-direction: column; flex-grow: 1;">
                                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                                                    <div>
                                                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 2px;">NIVEL</div>
                                                        <div id="render-vip-caption" style="font-size: 24px; font-weight: 800; color: var(--pass-primary, #8b5cf6); letter-spacing: -0.5px; display: flex; align-items: center; gap: 6px;">ÉLITE <i class="fa-solid fa-crown" style="font-size: 16px; color: #eab308;"></i></div>
                                                        <div style="margin-top: 8px; background: rgba(139, 92, 246, 0.1); padding: 4px 8px; border-radius: 4px; font-size: 9px; font-weight: 700; color: var(--pass-primary, #8b5cf6); display: inline-block;">1,250 pts para NIVEL PRO</div>
                                                    </div>
                                                    <div style="text-align: right;">
                                                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 2px;">CASHBACK</div>
                                                        <div id="render-balance" style="font-size: 22px; font-weight: 800; color: #111827;">$325.00</div>
                                                        <div style="font-size: 9px; font-weight: 600; color: var(--pass-primary, #8b5cf6); text-transform: uppercase;">Disponible</div>
                                                    </div>
                                                </div>
                                                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: auto;">
                                                    <div>
                                                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 2px;">MONEDERO</div>
                                                        <div id="render-wallet-balance" style="font-size: 20px; font-weight: 800; color: #111827;">$1,250.00</div>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Bottom row: Instructions and QR -->
                                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: auto; padding-top: 20px;">
                                                <div style="display: flex; align-items: center; gap: 8px;">
                                                    <div style="color: var(--pass-primary, #8b5cf6); font-size: 20px;"><i class="fa-solid fa-expand"></i></div>
                                                    <div style="font-size: 9px; font-weight: 600; color: #4b5563; text-transform: uppercase; line-height: 1.3;">ESCANEA TU TARJETA<br>EN CAJA</div>
                                                </div>
                                                <div style="width: 50px; height: 50px; background: white; padding: 4px; border-radius: 8px; border: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: center;">
                                                    <i class="fa-solid fa-qrcode" style="font-size: 38px; color: #111827;"></i>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- BACK OF CARD (Hidden for now, logic inside dashboard.js handles flip) -->
                                        <div class="card-face card-back pass-preview-card" style="background: #ffffff; border-radius: 16px; padding: 24px; position: absolute; top: 0; left: 0; width: 100%; height: 100%; box-shadow: 0 12px 30px rgba(0,0,0,0.08); display: flex; flex-direction: column; transform: rotateY(180deg); backface-visibility: hidden; border: 2px solid var(--pass-primary, #8b5cf6);">
                                            <div style="font-size: 12px; font-weight: 700; color: #111827; margin-bottom: 12px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">Términos y Condiciones</div>
                                            <div id="render-policies-text" style="font-size: 10px; color: #6b7280; line-height: 1.5; overflow-y: auto; flex-grow: 1;">Válido en todas las sucursales participantes. No es transferible.</div>
                                            <div style="text-align: center; margin-top: 16px; font-size: 10px; color: #9ca3af;">fidelio.com</div>
                                        </div>
                                    </div>
                                </div>
                                """

new_html = html[:start_idx] + new_pass_html + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
