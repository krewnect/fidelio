import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_stripe = """<section id="tab-stripe" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">MONETIZACIÓN</span>
                        <h1>Vende por Apple Wallet</h1>
                        <p>Convierte tu tarjeta de lealtad en un punto de venta. Configura cobros por suscripciones, recargas o membresías VIP.</p>
                    </div>
                </div>

                <!-- PROFESSIONAL TIER LOCK -->
                <div id="stripe-pro-lock" style="display:none; background: linear-gradient(135deg, rgba(139,92,246,0.05) 0%, rgba(0,0,0,0) 100%); border: 1px solid rgba(139,92,246,0.2); border-radius: 24px; padding: 50px; text-align: center; margin-bottom: 24px; position:relative; overflow:hidden;">
                    <div style="font-size: 60px; color: var(--accent-amber); margin-bottom: 20px;"><i class="fa-solid fa-crown" style="filter: drop-shadow(0 10px 10px rgba(245,158,11,0.4));"></i></div>
                    <h3 style="margin-bottom: 12px; color: var(--text-main); font-size: 28px; font-weight:800; letter-spacing:-0.5px;">Desbloquea Pagos en Wallet</h3>
                    <p style="color: var(--text-muted); font-size: 16px; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto; line-height:1.6;">
                        La conexión oficial con <b>Stripe</b> para vender saldo o membresías directamente en el reverso de la tarjeta requiere una licencia de nivel Business. Sube de nivel para revolucionar tus ventas.
                    </p>
                    <button class="btn btn-primary hover-glow" onclick="window.location.href='professionals.html'" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important; color: white !important; font-weight: 800; border: none; padding:16px 32px; border-radius:12px; font-size:16px; box-shadow: 0 10px 25px rgba(245,158,11,0.4);"><i class="fa-solid fa-arrow-up-right-dots"></i> Subir Nivel a Business</button>
                </div>

                <div id="stripe-active-ui" style="display:flex; flex-direction:column; gap:24px;">
                    <!-- HEADER METRICS / STEPS -->
                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:24px;">
                        
                        <div style="background:var(--surface); border:1px solid var(--border-soft); border-radius:24px; padding:32px; position:relative; overflow:hidden;">
                            <div style="position:absolute; top:-20px; right:-20px; font-size:100px; opacity:0.03;"><i class="fa-brands fa-stripe"></i></div>
                            <div style="width:50px; height:50px; border-radius:12px; background:rgba(99,102,241,0.1); color:#6366f1; display:flex; align-items:center; justify-content:center; font-size:24px; margin-bottom:20px;">
                                <i class="fa-solid fa-link"></i>
                            </div>
                            <h4 style="font-size:18px; font-weight:700; margin-bottom:8px; color:var(--text-main);">1. Crea tu Payment Link</h4>
                            <p style="font-size:14px; color:var(--text-muted); margin:0; line-height:1.5;">Entra a tu cuenta de Stripe, crea un producto (ej. Membresía VIP Mensual) y genera un link de pago.</p>
                        </div>

                        <div style="background:var(--surface); border:1px solid var(--border-soft); border-radius:24px; padding:32px; position:relative; overflow:hidden;">
                            <div style="position:absolute; top:-20px; right:-20px; font-size:100px; opacity:0.03;"><i class="fa-brands fa-apple"></i></div>
                            <div style="width:50px; height:50px; border-radius:12px; background:rgba(16,185,129,0.1); color:#10b981; display:flex; align-items:center; justify-content:center; font-size:24px; margin-bottom:20px;">
                                <i class="fa-solid fa-wallet"></i>
                            </div>
                            <h4 style="font-size:18px; font-weight:700; margin-bottom:8px; color:var(--text-main);">2. Vincula a la Tarjeta</h4>
                            <p style="font-size:14px; color:var(--text-muted); margin:0; line-height:1.5;">Pega el enlace abajo. Automáticamente se creará un botón de "Comprar / Renovar" en el reverso de la Wallet.</p>
                        </div>

                    </div>

                    <!-- CONFIGURATION PANEL -->
                    <div style="background:var(--surface); border:1px solid var(--border-soft); border-radius:24px; padding:40px; display:flex; flex-wrap:wrap; gap:40px;">
                        <div style="flex:1; min-width:300px;">
                            <h3 style="font-size:22px; font-weight:800; margin-bottom:12px; display:flex; align-items:center; gap:10px;"><i class="fa-brands fa-stripe" style="color:#6366f1;"></i> Conectar Checkout</h3>
                            <p style="font-size:15px; color:var(--text-muted); margin-bottom:32px; line-height:1.6;">Convierte a tus clientes en suscriptores. Al pagar, el saldo o nivel VIP se actualizará automáticamente en su teléfono mediante webhooks (próximamente).</p>
                            
                            <div class="form-group" style="margin-bottom: 24px;">
                                <label style="display: block; margin-bottom: 10px; font-weight: 700; font-size: 14px; color:var(--text-main);">¿A qué campaña quieres añadir el botón de cobro?</label>
                                <select id="stripe-campaign-select" class="apple-input" style="width: 100%;">
                                    <option value="">-- Selecciona una campaña --</option>
                                </select>
                            </div>

                            <div class="form-group" style="margin-bottom: 32px;">
                                <label style="display: block; margin-bottom: 10px; font-weight: 700; font-size: 14px; color:var(--text-main);">Enlace de Pago de Stripe (Payment Link)</label>
                                <div style="position:relative;">
                                    <i class="fa-solid fa-link" style="position:absolute; left:16px; top:18px; color:#94a3b8;"></i>
                                    <input type="url" id="stripe-payment-link" class="apple-input" placeholder="https://buy.stripe.com/..." style="width: 100%; padding-left:45px; font-family:monospace;">
                                </div>
                                <div style="font-size:12px; color:var(--text-muted); margin-top:8px;"><i class="fa-solid fa-circle-info"></i> El cliente será redirigido a este enlace de forma segura.</div>
                            </div>
                            
                            <button class="btn btn-primary hover-glow" onclick="saveStripeKeys()" style="background: linear-gradient(135deg, #6366f1, #4f46e5) !important; color: #fff !important; padding: 16px 32px; font-size: 16px; font-weight: 800; border: none; border-radius: 12px; cursor: pointer; box-shadow: 0 10px 25px rgba(99,102,241,0.4); width:100%;"><i class="fa-solid fa-cloud-arrow-up" style="margin-right: 8px;"></i> Guardar e Inyectar en Wallet</button>
                        </div>
                        
                        <!-- PREVIEW MOCKUP -->
                        <div style="width:300px; display:flex; justify-content:center; align-items:center; background:var(--bg-card); border-radius:24px; padding:20px; border:1px dashed var(--border-soft);">
                            <div style="width:100%; background:black; border-radius:24px; padding:20px; color:white; font-family:-apple-system, sans-serif; box-shadow:0 20px 40px rgba(0,0,0,0.3); position:relative;">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                                    <div style="width:40px; height:40px; border-radius:50%; background:#222; display:flex; justify-content:center; align-items:center;"><i class="fa-solid fa-xmark"></i></div>
                                    <div style="font-weight:600;">Reverso del Pass</div>
                                </div>
                                <div style="background:#222; border-radius:12px; padding:16px; margin-bottom:16px;">
                                    <div style="font-size:12px; color:#aaa; margin-bottom:4px;">NIVEL ACTUAL</div>
                                    <div style="font-size:18px; font-weight:700;">Membresía Gratuita</div>
                                </div>
                                <div style="background:#222; border-radius:12px; padding:16px; margin-bottom:20px;">
                                    <div style="font-size:12px; color:#aaa; margin-bottom:8px;">SUSCRIPCIÓN VIP</div>
                                    <p style="font-size:13px; color:#ddd; margin:0 0 12px 0; line-height:1.4;">Desbloquea 2x Puntos y envíos gratis.</p>
                                    <div style="background:#4f46e5; color:white; text-align:center; padding:10px; border-radius:8px; font-weight:600; font-size:14px; display:flex; justify-content:center; align-items:center; gap:8px;"><i class="fa-solid fa-lock-open"></i> Activar por $9.99/mes</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>"""

old_block_pattern = r'<section id="tab-stripe" class="tab-content">[\s\S]*?</section>'
html = re.sub(old_block_pattern, new_stripe, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
