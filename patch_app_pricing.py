import re

filepath = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/app.js'

with open(filepath, 'r') as f:
    content = f.read()

replacement = """
        const { billing_cycle, tier } = req.body;
        
        let priceId = null;
        if (tier === 'founder') {
            priceId = billing_cycle === 'annual' ? process.env.STRIPE_PRICE_FOUNDER_YR : process.env.STRIPE_PRICE_FOUNDER_MO;
        } else {
            priceId = billing_cycle === 'annual' ? process.env.STRIPE_PRICE_STANDARD_YR : process.env.STRIPE_PRICE_STANDARD_MO;
        }

        if (!priceId) {
            return res.status(500).json({ success: false, error: 'Falta configurar los STRIPE_PRICE_ en el archivo .env' });
        }
"""

pattern = re.compile(r'        // El Price ID debe venir del \.env.*?        \}', re.DOTALL)
new_content = pattern.sub(replacement.strip(), content)

with open(filepath, 'w') as f:
    f.write(new_content)
