import re

def patch_schema():
    with open('schema.sql', 'r') as f:
        content = f.read()
    if 'target_plan TEXT DEFAULT \'business\'' not in content:
        content = content.replace("reward_type TEXT NOT NULL,", "reward_type TEXT NOT NULL,\n    target_plan TEXT DEFAULT 'business',")
        with open('schema.sql', 'w') as f:
            f.write(content)

def patch_index():
    with open('index.html', 'r') as f:
        content = f.read()
    if 'promo-target-plan' not in content:
        target_plan_html = """
                        <div class="input-group" style="margin-bottom: 16px;">
                            <label style="display:block; margin-bottom:8px; font-weight:600; font-size:14px;">Plan Destino</label>
                            <select id="promo-target-plan" class="fidelio-input">
                                <option value="business">Plan Business (Restaurantes)</option>
                                <option value="professional">Plan Professional (Belleza/Salud)</option>
                            </select>
                        </div>"""
        content = content.replace('</select>\n                        </div>\n                        \n                        <div id="promo-discount-group"', '</select>\n                        </div>\n' + target_plan_html + '\n                        \n                        <div id="promo-discount-group"')
        with open('index.html', 'w') as f:
            f.write(content)

def patch_dashboard():
    with open('dashboard.js', 'r') as f:
        content = f.read()
    if 'promo-target-plan' not in content:
        content = content.replace("const typeSelect = document.getElementById('promo-type-select');", "const typeSelect = document.getElementById('promo-type-select');\n        const targetPlanSelect = document.getElementById('promo-target-plan');")
        content = content.replace("reward_type: type,", "reward_type: type,\n            target_plan: targetPlanSelect ? targetPlanSelect.value : 'business',")
        with open('dashboard.js', 'w') as f:
            f.write(content)

def patch_app():
    with open('app.js', 'r') as f:
        content = f.read()
    
    if 'businessType = promo.target_plan;' not in content:
        # Currently: let skipStripe = false;
        # Wait, the body extracts businessType as const: const { businessType, businessName, email, password, phone, promoCode } = req.body;
        # We need to change businessType to let, or use a new variable.
        content = content.replace("const { businessType, businessName", "let { businessType, businessName")
        
        target_logic = """
                    if (promo.target_plan) {
                        businessType = promo.target_plan;
                    }
                    if (promo.reward_type === 'lifetime_free' || (promo.reward_type === 'discount' && promo.discount_pct >= 100)) {"""
        
        content = content.replace("if (promo.reward_type === 'lifetime_free' || (promo.reward_type === 'discount' && promo.discount_pct >= 100)) {", target_logic)
        
        with open('app.js', 'w') as f:
            f.write(content)

if __name__ == '__main__':
    patch_schema()
    patch_index()
    patch_dashboard()
    patch_app()
