import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_insert = """        // 2. Insertar perfil en merchants
        const { error: dbError } = await supabase
            .from('merchants')
            .insert([
                { id: authData.user.id, business_name: businessName, plan_status: planStatus, business_type: businessType || 'business' }
            ]);"""

new_insert = """        // 2. Insertar perfil en merchants
        const { error: dbError } = await supabase
            .from('merchants')
            .insert([
                { 
                    id: authData.user.id, 
                    business_name: businessName, 
                    plan_status: planStatus, 
                    business_type: businessType || 'business',
                    owner_email: email,
                    owner_name: req.body.owner_name || '',
                    owner_phone: req.body.phone || ''
                }
            ]);"""

if old_insert in js:
    js = js.replace(old_insert, new_insert)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Sign up patched.")
else:
    print("WARNING: Could not find sign up insert in app.js")
