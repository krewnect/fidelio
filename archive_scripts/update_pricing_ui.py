import re

filepath = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html'

with open(filepath, 'r') as f:
    content = f.read()

replacement = """
                <!-- PRICING & SUBSCRIPTION CENTER -->
                <div style="background:var(--bg-card); border-radius:16px; border:1px solid var(--border-glass); padding:24px; margin-bottom: 24px;">
                    <!-- Top Stats & Founder Meter -->
                    <div style="display:flex; flex-wrap:wrap; gap:24px; justify-content:space-between; align-items:flex-start; margin-bottom:24px; border-bottom:1px solid var(--border-glass); padding-bottom:24px;">
                        <div style="display:flex; flex-wrap:wrap; gap:32px;">
                            <div>
                                <span style="font-size:12px; color:var(--text-muted);">Suscripción Actual</span>
                                <div id="sub-status-text" style="font-size:18px; font-weight:800; color:#10B981;"><i class="fa-solid fa-clock"></i> Calculando...</div>
                            </div>
                            <div>
                                <span style="font-size:12px; color:var(--text-muted);">Lugares Founder Restantes</span>
                                <div id="founder-meter-text" style="font-size:18px; font-weight:800; color:var(--accent-violet);"><i class="fa-solid fa-fire"></i> -- / 50 Disponibles</div>
                            </div>
                            <div>
                                <span style="font-size:12px; color:var(--text-muted);">Tarjetas Emitidas</span>
                                <div style="font-size:18px; font-weight:800; color:white;"><i class="fa-solid fa-wallet" style="color:var(--accent-violet);"></i> <span id="metrics-cards-issued">0</span></div>
                            </div>
                        </div>
                        <div style="display:flex; gap:12px; align-items: center; flex-wrap: wrap;">
                            <button id="btn-request-invoice" class="btn" style="background:rgba(139,92,246,0.1); border:1px solid var(--accent-violet); color:var(--accent-violet);"><i class="fa-solid fa-file-invoice"></i> Factura</button>
                            <button id="btn-bank-transfer" class="btn" style="background:rgba(139,92,246,0.1); border:1px solid var(--accent-violet); color:var(--accent-violet);"><i class="fa-solid fa-building-columns"></i> Transferencia</button>
                        </div>
                    </div>

                    <!-- Pricing Selector -->
                    <div style="display:flex; flex-direction:column; align-items:center;">
                        <!-- Toggle Monthly / Annual -->
                        <div style="display:flex; align-items:center; gap:16px; margin-bottom:24px; background:rgba(0,0,0,0.3); padding:8px 16px; border-radius:999px; border:1px solid var(--border-glass);">
                            <span id="label-monthly" style="color:white; font-weight:bold; font-size:14px; cursor:pointer;">Mensual</span>
                            
                            <label style="position:relative; display:inline-block; width:50px; height:24px;">
                                <input type="checkbox" id="billing-cycle-toggle" checked style="opacity:0; width:0; height:0;">
                                <span style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background-color:var(--accent-violet); border-radius:24px; transition:.4s;">
                                    <span style="position:absolute; content:''; height:18px; width:18px; left:3px; bottom:3px; background-color:white; border-radius:50%; transition:.4s; transform:translateX(26px);"></span>
                                </span>
                            </label>

                            <span id="label-annual" style="color:var(--text-muted); font-size:14px; cursor:pointer;">Anual <span style="background:rgba(16,185,129,0.2); color:#10b981; padding:2px 8px; border-radius:12px; font-size:10px; margin-left:4px; font-weight:800;">2 MESES GRATIS</span></span>
                        </div>

                        <!-- Price Display -->
                        <div style="text-align:center; margin-bottom:24px;">
                            <div id="pricing-tier-badge" style="display:inline-block; background:linear-gradient(135deg, #FFD700 0%, #FDB931 100%); color:black; font-weight:800; padding:4px 12px; border-radius:12px; font-size:12px; margin-bottom:8px; text-transform:uppercase; letter-spacing:1px;">
                                LICENCIA FOUNDER (DE POR VIDA)
                            </div>
                            <div style="font-size:48px; font-weight:800; line-height:1;">
                                $<span id="pricing-amount">9,999</span> <span style="font-size:16px; color:var(--text-muted); font-weight:normal;">MXN / <span id="pricing-period">año</span></span>
                            </div>
                            <p id="pricing-description" style="color:var(--text-muted); margin-top:8px; font-size:14px;">Sucursales ilimitadas. Soporte VIP.</p>
                        </div>

                        <!-- Checkout Action -->
                        <div style="display:flex; gap:12px; width:100%; max-width:400px;">
                            <input type="text" id="merchant-promo-code" class="fidelio-input" placeholder="Código Promo" style="flex:1;">
                            <button id="btn-pay-stripe" class="btn btn-primary" style="flex:2; background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); border:none; justify-content:center;">
                                <i class="fa-brands fa-stripe"></i> Procesar Pago
                            </button>
                        </div>
                    </div>
                </div>
"""

pattern = re.compile(r'<!-- TOP BAR \(Billing & Sub\) -->.*?</div>\s*</div>', re.DOTALL)
new_content = pattern.sub(replacement.strip(), content)

with open(filepath, 'w') as f:
    f.write(new_content)
