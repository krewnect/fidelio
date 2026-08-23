import re

filepath = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/app.js'

with open(filepath, 'r') as f:
    content = f.read()

# Select custom_price too
content = content.replace("select('stripe_customer_id, business_name')", "select('stripe_customer_id, business_name, custom_price')")

replacement = """
        let sessionParams = {
            mode: 'subscription',
            payment_method_types: ['card'],
            customer: merchant.stripe_customer_id || undefined,
            success_url: `${req.headers.origin}/panel?payment=success`,
            cancel_url: `${req.headers.origin}/panel?payment=cancelled`,
            metadata: { merchant_id: req.merchantId }
        };

        if (merchant.custom_price) {
            // Dynamic custom pricing
            sessionParams.line_items = [{
                price_data: {
                    currency: 'mxn',
                    product_data: { name: 'Licencia Especial Fidelio' },
                    unit_amount: merchant.custom_price * 100,
                    recurring: { interval: 'month' }
                },
                quantity: 1
            }];
        } else {
            // Standard static pricing
            if (!priceId) {
                return res.status(500).json({ success: false, error: 'Falta configurar los STRIPE_PRICE_ en el archivo .env' });
            }
            sessionParams.line_items = [{ price: priceId, quantity: 1 }];
        }

        const session = await stripe.checkout.sessions.create(sessionParams);
"""

pattern = re.compile(r'        if \(\!priceId\) \{\n            return res.status\(500\).*?        \}\n\n        const session = await stripe.checkout.sessions.create\(\{.*?        \}\);', re.DOTALL)
new_content = pattern.sub(replacement.strip('\n'), content)

with open(filepath, 'w') as f:
    f.write(new_content)
