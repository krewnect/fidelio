import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = "<!-- PRICING & SUBSCRIPTION CENTER -->"
end_marker = "<!-- MAIN GRID -->"

pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)

new_layout = """<!-- PRICING & SUBSCRIPTION CENTER -->
                <div class="content-panel" style="margin-bottom: 32px; padding: 32px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid var(--border-soft); padding-bottom: 24px;">
                        <div>
                            <h2 style="font-size: 20px; font-weight: 800; color: var(--text-main); margin: 0;">Suscripción y Pagos</h2>
                            <p style="margin: 4px 0 0 0; font-size: 13px; color: var(--text-muted);">Administra tu plan de facturación de Fidelio.</p>
                        </div>
                        <div style="display: flex; gap: 12px;">
                            <button id="btn-request-invoice" class="fidelio-btn-secondary"><i class="fa-solid fa-file-invoice"></i> Solicitar Factura</button>
                            <button id="btn-bank-transfer" class="fidelio-btn-secondary"><i class="fa-solid fa-building-columns"></i> Datos Bancarios</button>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 32px;">
                        
                        <!-- Left Side: Subscription Details -->
                        <div style="display: flex; flex-direction: column; gap: 24px;">
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                                <div>
                                    <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 700; margin-bottom: 8px; letter-spacing: 0.5px;">Plan Actual</div>
                                    <div id="pricing-tier-badge" style="font-weight: 800; color: #F59E0B; display: inline-flex; align-items: center; gap: 6px; background: rgba(245, 158, 11, 0.1); padding: 6px 12px; border-radius: 8px; font-size: 13px;"><i class="fa-solid fa-crown"></i> Founder (De por vida)</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 700; margin-bottom: 8px; letter-spacing: 0.5px;">Precio</div>
                                    <div style="font-size: 20px; font-weight: 800; color: var(--text-main);">$<span id="pricing-amount">9,999</span> <span style="font-size: 13px; color: var(--text-muted); font-weight: 600;">MXN / <span id="pricing-period">año</span></span></div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 700; margin-bottom: 8px; letter-spacing: 0.5px;">Estado</div>
                                    <div id="sub-status-text" style="font-size: 15px; font-weight: 700; color: #10B981; display: flex; align-items: center; gap: 6px;"><i class="fa-solid fa-check-circle"></i> Calculando...</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-weight: 700; margin-bottom: 8px; letter-spacing: 0.5px;">Tarjetas Emitidas</div>
                                    <div style="font-size: 15px; font-weight: 700; color: var(--text-main); display: flex; align-items: center; gap: 6px;"><i class="fa-solid fa-wallet" style="color:var(--accent-violet);"></i> <span id="metrics-cards-issued">0</span></div>
                                </div>
                            </div>
                            
                            <p id="pricing-description" style="color:var(--text-muted); font-size:14px; margin: 0; padding-top: 16px; border-top: 1px solid var(--border-soft);">Sucursales ilimitadas. Soporte VIP incluido.</p>
                        </div>

                        <!-- Right Side: Payment -->
                        <div style="background: var(--bg-input); padding: 24px; border-radius: 16px; border: 1px solid var(--border-soft); display: flex; flex-direction: column;">
                            <div style="font-size: 14px; font-weight: 700; color: var(--text-main); margin-bottom: 16px;">Renovar o Mejorar Plan</div>
                            
                            <!-- Toggle Monthly / Annual -->
                            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px; background: rgba(139,92,246,0.05); padding: 8px 16px; border-radius: 100px; width: fit-content; border: 1px solid rgba(139,92,246,0.1);">
                                <span id="label-monthly" style="font-size: 13px; font-weight: 600; color: var(--text-muted); cursor:pointer;">Mensual</span>
                                <label style="position:relative; display:inline-block; width:44px; height:24px;">
                                    <input type="checkbox" id="billing-cycle-toggle" checked style="opacity:0; width:0; height:0;">
                                    <span style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:var(--accent-violet); border-radius:24px; transition:.3s; box-shadow: 0 2px 4px rgba(139,92,246,0.2);">
                                        <span class="slider-circle" style="position:absolute; content:''; height:18px; width:18px; left:3px; bottom:3px; background-color:white; border-radius:50%; transition:.3s; transform:translateX(20px);"></span>
                                    </span>
                                </label>
                                <span id="label-annual" style="font-size: 13px; font-weight: 700; color: var(--text-main); cursor:pointer; display: flex; align-items: center; gap: 6px;">Anual <span style="background:rgba(16,185,129,0.1); color:#059669; padding:3px 8px; border-radius:100px; font-size:10px; font-weight:800; text-transform:uppercase;">2 Meses Gratis</span></span>
                            </div>

                            <div style="display: flex; flex-direction: column; gap: 12px;">
                                <input type="text" id="merchant-promo-code" class="fidelio-input" placeholder="Código promocional" style="width: 100%; background: #ffffff;">
                                <button id="btn-pay-stripe" class="fidelio-btn-primary" style="width: 100%; justify-content: center; font-size: 15px;"><i class="fa-brands fa-stripe" style="font-size: 18px;"></i> Procesar Pago</button>
                            </div>
                            
                            <div style="text-align: center; font-size: 11px; color: var(--text-muted); margin-top: auto; padding-top: 16px;">
                                Pagos encriptados con seguridad bancaria de Stripe.<br>
                                Al procesar el pago, aceptas nuestro <a href="/privacy.html" target="_blank" style="color:var(--accent-violet); text-decoration:none; font-weight: 600;">Aviso</a> y <a href="/terms.html" target="_blank" style="color:var(--accent-violet); text-decoration:none; font-weight: 600;">Términos</a>.
                            </div>
                        </div>
                        
                    </div>
                </div>

                <!-- MAIN GRID -->"""

if re.search(pattern, html):
    html = re.sub(pattern, new_layout, html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Billing section refactored successfully.")
else:
    print("Could not find the block to replace.")
