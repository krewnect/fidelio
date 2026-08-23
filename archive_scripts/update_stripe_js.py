import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_save_stripe = """window.saveStripeKeys = async function() {
    const pub = document.getElementById('stripe-pub-key').value;
    const sec = document.getElementById('stripe-secret-key').value;
    try {
        const res = await fetch('/api/stripe/keys', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ stripe_pub_key: pub, stripe_secret_key: sec })
        });
        if(res.ok) {
            if (typeof showToast === 'function') showToast("Llaves de Stripe guardadas", "success");
        } else {
            if (typeof showToast === 'function') showToast("Error al guardar Stripe", "error");
        }
    } catch(e) {
        console.error(e);
        alert("Error saving stripe: " + e.message);
    }
};"""

new_save_stripe = """window.saveStripeKeys = async function() {
    const linkInput = document.getElementById('stripe-payment-link');
    const paymentLink = linkInput ? linkInput.value : '';
    
    if (!paymentLink || !paymentLink.includes('stripe.com')) {
        if (typeof showToast === 'function') showToast("Ingresa un Payment Link válido de Stripe", "warning");
        return;
    }
    
    // We save this into the current active campaign (if there is one) or locally
    state.customBannerUrl = paymentLink;
    
    if (typeof showToast === 'function') showToast("Payment Link de Stripe vinculado con éxito", "success");
};"""

if old_save_stripe in js:
    js = js.replace(old_save_stripe, new_save_stripe)
    print("Replaced saveStripeKeys correctly.")
else:
    # Use regex
    js = re.sub(
        r'window\.saveStripeKeys = async function\(\) \{.*?\};',
        new_save_stripe,
        js,
        flags=re.DOTALL
    )
    print("Replaced saveStripeKeys via regex.")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
