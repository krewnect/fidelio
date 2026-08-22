import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_insert = """        // 2. Insertar perfil en merchants
        const { error: dbError } = await supabase
            .from('merchants')
            .insert(["""

new_insert = """        // 2. Insertar perfil en merchants
        const clientToUse = supabaseAdmin || supabase;
        const { error: dbError } = await clientToUse
            .from('merchants')
            .insert(["""

if old_insert in js:
    js = js.replace(old_insert, new_insert)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("app.js insert patched.")
else:
    print("WARNING: Could not find old_insert in app.js")

