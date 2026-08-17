import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Stripe keys section
old_stripe = """                        <div style="margin-top: 15px;">
                            <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">Stripe Secret Key</label>
                            <input type="text" id="stripe-secret-key" class="form-control" placeholder="sk_test_..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--bg-color); color: var(--text-color);">
                        </div>"""

new_stripe = """                        <div style="margin-top: 15px;">
                            <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">Stripe Secret Key</label>
                            <input type="text" id="stripe-secret-key" class="form-control" placeholder="sk_test_..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--bg-color); color: var(--text-color);">
                        </div>
                        
                        <div style="margin-top: 15px; padding:15px; background: rgba(139, 92, 246, 0.1); border-radius: 8px; border: 1px solid var(--primary);">
                            <label style="color: var(--primary); font-size: 14px; margin-bottom: 8px; display: block; font-weight:bold;">Enlace de Pago de Stripe (Profesionales)</label>
                            <p style="font-size:12px; color:var(--text-muted); margin-bottom:10px;">Pega tu "Payment Link" generado en Stripe. Si eres un profesional, el botón de tu tarjeta digital redirigirá a los clientes aquí para cobrar tus servicios.</p>
                            <input type="text" id="stripe-payment-link" class="form-control" placeholder="https://buy.stripe.com/..." onchange="updateStripeLink(this.value)" style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--primary); background: var(--bg-color); color: var(--text-color);">
                        </div>"""

content = content.replace(old_stripe, new_stripe)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Add the function to handle the link update
js_append = """
window.updateStripeLink = function(val) {
    if (val && val.includes('stripe')) {
        state.customBannerUrl = val;
        showToast("Enlace de Stripe configurado como acción principal de la tarjeta.", "success");
    }
};

// Auto-fill the input if it has a stripe link
const oldSelectCamp = "        state.customBannerUrl = camp.banner_url || null;";
const newSelectCamp = "        state.customBannerUrl = camp.banner_url || null;\\n        if(state.customBannerUrl && state.customBannerUrl.includes('stripe.com')) {\\n            const linkInput = document.getElementById('stripe-payment-link');\\n            if(linkInput) linkInput.value = state.customBannerUrl;\\n        }";
"""
js_content = js_content.replace("        state.customBannerUrl = camp.banner_url || null;", "        state.customBannerUrl = camp.banner_url || null;\n        if(state.customBannerUrl && state.customBannerUrl.includes('stripe.com')) {\n            const linkInput = document.getElementById('stripe-payment-link');\n            if(linkInput) linkInput.value = state.customBannerUrl;\n        }")

if "window.updateStripeLink =" not in js_content:
    js_content += js_append

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
