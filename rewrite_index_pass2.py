import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_str = '<div class="card-3d-scene">'
end_str = '<div style="width:100%; display:flex; justify-content:center; padding-top:10px;">'

start_idx = html.find(start_str)
end_idx = html.find(end_str)

if start_idx == -1 or end_idx == -1:
    print(f"Could not find boundaries. start={start_idx}, end={end_idx}")
    exit(1)

new_pass_html = """<div class="card-3d-scene" style="perspective: 1000px; display: flex; justify-content: center; align-items: center; padding: 20px;">
                                    <div class="card-3d-object" id="pass-render" style="width: 100%; max-width: 360px; position: relative; transition: transform 0.6s; transform-style: preserve-3d;">
                                        
                                        <!-- FRONT OF CARD -->
                                        <div class="card-face card-front pass-preview-card premium-white-card" style="background: #ffffff; border-radius: 20px; padding: 24px; position: relative; overflow: hidden; box-shadow: 0 16px 40px rgba(0,0,0,0.12); display: flex; flex-direction: column; min-height: 250px; backface-visibility: hidden; border: 1px solid var(--pass-primary, #8b5cf6);">
                                            
                                            <!-- Top row: Logo and "10 SELLOS" -->
                                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                                                <div class="pass-logo-container" style="flex: 1; max-width: 160px; display: flex; align-items: center;">
                                                    <img id="render-custom-logo" src="" style="width: 100%; max-height: 45px; object-fit: contain; display: none; object-position: left center;" />
                                                    <div id="render-default-logo" style="display: flex; align-items: center; gap: 8px;">
                                                        <i class="fa-solid fa-crown" id="render-icon" style="color: var(--pass-primary, #8b5cf6); font-size: 24px;"></i>
                                                        <span id="render-name" style="font-weight: 800; font-size: 20px; color: #111827; letter-spacing: -0.5px;">Fidelio</span>
                                                    </div>
                                                </div>
                                                <div id="render-top-right" style="text-align: right; display: flex; align-items: center; gap: 8px;">
                                                    <span id="render-top-right-text" style="font-size: 11px; font-weight: 700; color: var(--pass-primary, #8b5cf6); text-transform: uppercase; letter-spacing: 0.5px;">10 SELLOS</span>
                                                    <i class="fa-solid fa-wifi" style="transform: rotate(90deg); color: var(--pass-primary, #8b5cf6); opacity: 0.8; font-size: 14px;"></i>
                                                </div>
                                            </div>

                                            <!-- Middle Body (Dynamic: Stamps vs Cashback) -->
                                            <div id="render-body-stamps" style="display: flex; flex-direction: column; flex-grow: 1;">
                                                <div style="font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.5px; line-height: 1.4;">ACUMULA <span id="render-stamps-total-text">10</span> SELLOS<br>Y OBTÉN TU RECOMPENSA</div>
                                                
                                                <!-- Stamps Grid -->
                                                <div id="render-stamps-grid" style="display: flex; flex-wrap: wrap; gap: 14px; position: relative; margin-bottom: 20px;">
                                                    <!-- Generated via JS -->
                                                </div>
                                            </div>

                                            <div id="render-body-cashback" style="display: none; flex-direction: column; flex-grow: 1;">
                                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
                                                    <div>
                                                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 1px;">NIVEL</div>
                                                        <div id="render-vip-caption" style="font-size: 28px; font-weight: 800; color: var(--pass-primary, #8b5cf6); letter-spacing: -1px; display: flex; align-items: center; gap: 8px;">ÉLITE <i class="fa-solid fa-crown" style="font-size: 18px; color: #eab308;"></i></div>
                                                        <div style="margin-top: 12px; background: rgba(139, 92, 246, 0.1); padding: 6px 10px; border-radius: 6px; font-size: 10px; font-weight: 700; color: var(--pass-primary, #8b5cf6); display: inline-block;">1,250 pts para NIVEL PRO</div>
                                                    </div>
                                                    <div style="text-align: right;">
                                                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 1px;">CASHBACK</div>
                                                        <div id="render-balance" style="font-size: 24px; font-weight: 800; color: #111827;">$325.00</div>
                                                        <div style="font-size: 10px; font-weight: 600; color: var(--pass-primary, #8b5cf6); text-transform: uppercase; margin-top: 2px;">Disponible</div>
                                                    </div>
                                                </div>
                                                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: auto;">
                                                    <div>
                                                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 1px;">MONEDERO</div>
                                                        <div id="render-wallet-balance" style="font-size: 20px; font-weight: 800; color: #111827;">$1,250.00</div>
                                                        <div style="font-size: 10px; font-weight: 600; color: var(--pass-primary, #8b5cf6); text-transform: uppercase; margin-top: 2px;">Disponible</div>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Bottom row: Instructions and QR -->
                                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: auto; padding-top: 16px;">
                                                <div style="display: flex; align-items: center; gap: 10px;">
                                                    <div style="color: var(--pass-primary, #8b5cf6); font-size: 24px;"><i class="fa-solid fa-expand"></i></div>
                                                    <div style="font-size: 10px; font-weight: 600; color: #4b5563; text-transform: uppercase; line-height: 1.4; letter-spacing: 0.5px;">ESCANEA TU TARJETA<br>EN CAJA</div>
                                                </div>
                                                <div style="width: 55px; height: 55px; background: white; padding: 4px; border-radius: 8px; border: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: center;">
                                                    <i class="fa-solid fa-qrcode" style="font-size: 42px; color: #111827;"></i>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- BACK OF CARD -->
                                        <div class="card-face card-back pass-preview-card premium-white-card" style="background: #ffffff; border-radius: 20px; padding: 24px; position: absolute; top: 0; left: 0; width: 100%; height: 100%; box-shadow: 0 16px 40px rgba(0,0,0,0.12); display: flex; flex-direction: column; transform: rotateY(180deg); backface-visibility: hidden; border: 1px solid var(--pass-primary, #8b5cf6);">
                                            <div style="font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 16px; border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">Términos y Políticas</div>
                                            <div id="render-policies-text" style="font-size: 11px; color: #4b5563; line-height: 1.6; overflow-y: auto; flex-grow: 1;">Las recompensas no son transferibles ni canjeables por efectivo.</div>
                                            
                                            <div id="render-wallet-links-back" style="display:none; margin-bottom: 16px;">
                                                <div style="font-size: 12px; font-weight: 700; color: #111827; margin-bottom: 8px;">Acciones Rápidas</div>
                                                <div id="render-wallet-link-appointment" style="background:#f9fafb; border: 1px solid #e5e7eb; padding:10px; border-radius:8px; margin-bottom:6px; display:none; align-items:center; gap:10px; color: #111827;">
                                                    <i class="fa-solid fa-calendar-check" style="color:var(--pass-primary, #8b5cf6);"></i> <span style="font-size:12px; font-weight: 600;">Agendar Cita</span>
                                                </div>
                                                <div id="render-wallet-link-payment" style="background:#f9fafb; border: 1px solid #e5e7eb; padding:10px; border-radius:8px; display:none; align-items:center; gap:10px; color: #111827;">
                                                    <i class="fa-solid fa-credit-card" style="color:#10b981;"></i> <span style="font-size:12px; font-weight: 600;">Pagar Cita</span>
                                                </div>
                                            </div>

                                            <div style="text-align: center; margin-top: 16px; font-size: 10px; color: #9ca3af; display: flex; align-items: center; justify-content: center; gap: 8px;">
                                                <img src="./fidelio_logo_purple.png" style="height: 14px; filter: grayscale(1) opacity(0.5);">
                                            </div>
                                        </div>

                                    </div>
                                </div>
                                """

new_html = html[:start_idx] + new_pass_html + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
