import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = "if (promo.target_plan) {\n                        businessType = promo.target_plan;\n                    }"
replacement = """if (promo.target_plan) {
                        businessType = promo.target_plan;
                        // Map internal 'business' to 'restaurant' to satisfy Postgres constraints
                        if (businessType === 'business') businessType = 'restaurant';
                    }"""

if target in js:
    js = js.replace(target, replacement)
    
target2 = "business_type: businessType || 'restaurant'"
replacement2 = "business_type: (businessType === 'business' ? 'restaurant' : businessType) || 'restaurant'"

if target2 in js:
    js = js.replace(target2, replacement2)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Backend register mapping fixed")
