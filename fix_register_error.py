import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_error = """        if (dbError) console.error("Error al crear merchant:", dbError);

        res.json({ success: true, user: authData.user, skipStripe });"""

new_error = """        if (dbError) {
            console.error("Error al crear merchant:", dbError);
            throw new Error("No se pudo crear el perfil del negocio. Por favor intenta de nuevo.");
        }

        res.json({ success: true, user: authData.user, skipStripe });"""

if old_error in js:
    js = js.replace(old_error, new_error)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("app.js error handling patched.")
else:
    print("WARNING: Could not find old_error in app.js")

