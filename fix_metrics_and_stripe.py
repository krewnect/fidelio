import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix Metrics Tab Data (Zeroing out)
html = html.replace('<div style="font-size: 3rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 12px; text-shadow: 0 4px 10px rgba(0,0,0,0.1);">+0%</div>', '<div style="font-size: 3rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 12px; text-shadow: 0 4px 10px rgba(0,0,0,0.1);">0%</div>')
html = html.replace('<div style="font-size: 2.5rem; font-weight: 800; color: #10b981; margin-bottom: 8px;">+$0.00 <span style="font-size: 1rem; color: var(--text-muted); font-weight: 500;">MXN</span></div>', '<div style="font-size: 2.5rem; font-weight: 800; color: #10b981; margin-bottom: 8px;">$0.00 <span style="font-size: 1rem; color: var(--text-muted); font-weight: 500;">MXN</span></div>')

# Clear out the mock text "+18% vs mes pasado" and generic texts if they exist
html = html.replace('<div style="background: rgba(16, 185, 129, 0.1); color: #10b981; display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;"><i class="fa-solid fa-arrow-trend-up"></i> +18% vs mes pasado</div>', '<div style="background: rgba(16, 185, 129, 0.1); color: #10b981; display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;"><i class="fa-solid fa-arrow-trend-up"></i> 0% vs mes pasado</div>')

# Clear out "Actividad en Vivo" mock items
mock_activity_1 = """                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid var(--border-soft);">
                                        <div style="display: flex; gap: 12px;">
                                            <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--surface-light); display: flex; align-items: center; justify-content: center; font-size: 12px;"><i class="fa-solid fa-wallet"></i></div>
                                            <div>
                                                <div style="font-size: 14px; font-weight: 600;">Roberto O. <span style="font-weight: normal; color: var(--text-muted);">usó $45 cashback</span></div>
                                            </div>
                                        </div>
                                        <div style="font-size: 12px; color: var(--text-muted);">Hace 2m</div>
                                    </div>"""

mock_activity_2 = """                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid var(--border-soft);">
                                        <div style="display: flex; gap: 12px;">
                                            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(139, 92, 246, 0.1); color: var(--accent-violet); display: flex; align-items: center; justify-content: center; font-size: 12px;"><i class="fa-solid fa-qrcode"></i></div>
                                            <div>
                                                <div style="font-size: 14px; font-weight: 600;">Ana G. <span style="font-weight: normal; color: var(--text-muted);">escaneó mesa #4 (+120 pts)</span></div>
                                            </div>
                                        </div>
                                        <div style="font-size: 12px; color: var(--text-muted);">Hace 5m</div>
                                    </div>"""

mock_activity_3 = """                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid var(--border-soft);">
                                        <div style="display: flex; gap: 12px;">
                                            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(245, 158, 11, 0.1); color: #f59e0b; display: flex; align-items: center; justify-content: center; font-size: 12px;"><i class="fa-solid fa-crown"></i></div>
                                            <div>
                                                <div style="font-size: 14px; font-weight: 600;">Carlos R. <span style="font-weight: normal; color: var(--text-muted);">subió a VIP Oro 🏆</span></div>
                                            </div>
                                        </div>
                                        <div style="font-size: 12px; color: var(--text-muted);">Hace 14m</div>
                                    </div>"""

mock_activity_4 = """                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; padding: 12px 0;">
                                        <div style="display: flex; gap: 12px;">
                                            <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--surface-light); display: flex; align-items: center; justify-content: center; font-size: 12px;"><i class="fa-solid fa-envelope-open-text"></i></div>
                                            <div>
                                                <div style="font-size: 14px; color: var(--text-muted);">24 clientes abrieron promo Cumpleaños</div>
                                            </div>
                                        </div>
                                        <div style="font-size: 12px; color: var(--text-muted);">Hace 30m</div>
                                    </div>"""

empty_activity = """                                    <div style="display: flex; justify-content: center; align-items: center; height: 100%; padding: 40px 0; flex-direction: column; color: var(--text-muted);">
                                        <i class="fa-solid fa-chart-line" style="font-size: 32px; margin-bottom: 10px; opacity: 0.5;"></i>
                                        <p style="margin: 0; font-size: 14px;">Aún no hay actividad de clientes.</p>
                                    </div>"""

html = html.replace(mock_activity_1, empty_activity)
html = html.replace(mock_activity_2, "")
html = html.replace(mock_activity_3, "")
html = html.replace(mock_activity_4, "")

# Ensure the 4 small metric cards are zeroed (if they haven't been already, but my previous batch script did it globally on '1,248' etc)
html = html.replace('1,248', '0')
html = html.replace('$485', '$0.00')
html = html.replace('43.5%', '0%')
html = html.replace('2.8x', '0x')

# 2. Fix Monetization (Stripe) Tab
# Instead of string matching exactly, let's use regex to find and replace the content of tab-stripe.
stripe_start = '<section id="tab-stripe" class="tab-content" style="display:none;">'
stripe_end = '<!-- BRANCHES TAB -->'
if stripe_start in html and stripe_end in html:
    pre_stripe = html.split(stripe_start)[0]
    post_stripe = html.split(stripe_end)[1]
    
    new_stripe_html = """
            <section id="tab-stripe" class="tab-content" style="display:none;">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">MONETIZACIÓN</span>
                        <h1>Pagos y Suscripciones</h1>
                        <p>Vincula tu cuenta de Stripe para cobrar anticipos de citas y suscripciones VIP.</p>
                    </div>
                </div>

                <div class="content-panel" style="background: linear-gradient(135deg, rgba(99,91,255,0.05) 0%, rgba(0,0,0,0) 100%); border-radius: 20px; padding: 40px; text-align: center; border: 1px solid rgba(99,91,255,0.3); max-width: 700px; margin: 0 auto;">
                    <i class="fa-brands fa-stripe" style="font-size: 64px; color: #635bff; margin-bottom: 20px;"></i>
                    <h2 style="margin-bottom: 15px;">Integra tus Payment Links</h2>
                    <p style="color: var(--text-muted); margin-bottom: 30px;">Simplificamos la conexión. No necesitas llaves técnicas (API Keys). Solo genera un enlace de pago (Payment Link) en tu panel de Stripe y pégalo aquí.</p>
                    
                    <div style="text-align: left; background: var(--surface); padding: 25px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid var(--border-color);">
                        <label style="display: block; font-weight: bold; margin-bottom: 10px; color: var(--text-main);">Tu Enlace de Pago de Stripe (Payment Link)</label>
                        <input type="text" id="stripe-payment-link" class="fidelio-input" placeholder="https://buy.stripe.com/..." style="width: 100%; padding: 16px; font-size: 16px; margin-bottom: 20px;">
                        
                        <div style="display: flex; justify-content: flex-end;">
                            <button class="btn btn-primary" style="background: #635bff; border: none; padding: 12px 30px; font-size: 16px; font-weight: bold;" onclick="saveStripeSettings()">
                                <i class="fa-solid fa-link"></i> Vincular Cuenta
                            </button>
                        </div>
                    </div>
                    
                    <div style="margin-top: 30px; font-size: 13px; color: var(--text-muted); display: flex; align-items: center; justify-content: center; gap: 10px;">
                        <i class="fa-solid fa-shield-halved"></i> <span>Tus pagos están protegidos por Stripe. Fidelio no cobra comisiones por transacción.</span>
                    </div>
                </div>
            </section>
"""
    html = pre_stripe + new_stripe_html + "            <!-- BRANCHES TAB -->\n" + post_stripe


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Metrics zeroed out and Stripe tab redesigned.")
