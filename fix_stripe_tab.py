import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the entire settings-card inside tab-stripe
old_stripe = """                <div class="settings-card" style="background: var(--surface); padding: 24px; border-radius: 16px; border: 1px solid var(--surface-light);">
                    <div class="form-group" style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 8px;">Public Key (Stripe)</label>
                        <input type="text" id="stripe-pub-key" class="form-control" placeholder="pk_test_..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--bg-color); color: var(--text-color);">
                    </div>
                    <div class="form-group" style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 8px;">Secret Key (Stripe)</label>
                        <input type="password" id="stripe-secret-key" class="form-control" placeholder="sk_test_..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--bg-color); color: var(--text-color);">
                    </div>
                    <button class="btn btn-primary" onclick="saveStripeKeys()" style="background: #8b5cf6 !important; color: #fff; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer;"><i class="fa-solid fa-save"></i> Guardar Llaves</button>
                </div>"""

new_stripe = """                <div class="settings-card" style="background: var(--surface); padding: 32px; border-radius: 20px; border: 1px solid var(--surface-light); text-align: center;">
                    <div style="font-size: 48px; color: #6366f1; margin-bottom: 16px;">
                        <i class="fa-brands fa-stripe"></i>
                    </div>
                    <h3 style="margin-bottom: 12px; color: var(--text-main); font-size: 20px;">Vende tus beneficios directo desde Wallet</h3>
                    <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 32px; max-width: 500px; margin-left: auto; margin-right: auto;">
                        Crea un producto en tu cuenta de Stripe (ej. "Membresía Anual" o "Saldo Prepagado") y pega aquí el enlace de pago. Nosotros nos encargamos de integrarlo en tu tarjeta de Apple Wallet.
                    </p>
                    
                    <div class="form-group" style="margin-bottom: 24px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; font-size: 13px;">Payment Link de Stripe</label>
                        <input type="url" id="stripe-payment-link" class="form-control" placeholder="https://buy.stripe.com/test_..." style="width: 100%; padding: 16px; border-radius: 12px; border: 2px solid var(--surface-light); background: var(--bg-color); color: var(--text-color); font-size: 15px; transition: all 0.3s ease;">
                    </div>
                    
                    <button class="btn btn-primary" onclick="saveStripeKeys()" style="background: #8b5cf6 !important; color: #fff !important; padding: 16px 32px; font-size: 16px; font-weight: 700; border: none; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 14px rgba(139,92,246,0.3); transition: all 0.3s ease;"><i class="fa-solid fa-link" style="margin-right: 8px;"></i> Vincular Payment Link</button>
                </div>"""

if old_stripe in html:
    html = html.replace(old_stripe, new_stripe)
    print("Stripe successfully replaced in index.html")
else:
    print("Could not find the exact old stripe HTML. Looking dynamically...")
    # Dynamic replace
    html = re.sub(
        r'<div class="settings-card" style="background: var\(--surface\).*?Guardar Llaves</button>\s*</div>',
        new_stripe,
        html,
        flags=re.DOTALL
    )
    print("Stripe replaced via regex")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
