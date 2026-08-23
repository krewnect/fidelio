with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_logic = """        const plan = merchant.business_type || 'starter';
        if (plan === 'business' || plan === 'enterprise') {"""

new_logic = """        const plan = (merchant.business_type || 'basic').toLowerCase();
        if (['business', 'pro', 'enterprise'].includes(plan)) {"""

js = js.replace(old_logic, new_logic)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated backend logic.")
