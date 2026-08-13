import re

with open('dashboard.js', 'r') as f:
    js = f.read()

old_save = """        if (!error) {
            showToast("Guardado automático en la nube ☁️", "success");
        }"""

new_save = """        if (!error) {
            showToast("Guardado automático en la nube ☁️", "success");
        } else {
            console.error("Supabase Save Error:", error);
            showToast("Error de conexión BD: " + (error.message || "Fallo desconocido"), "error");
        }"""

js = js.replace(old_save, new_save)

with open('dashboard.js', 'w') as f:
    f.write(js)
