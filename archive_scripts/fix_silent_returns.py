import re

with open('dashboard.js', 'r') as f:
    js = f.read()

old_checks = """    if (!window.supabaseClient) {
        console.error("No supabase client!");
        return;
    }
    if (!state.tenantId) {
        console.error("No tenantId in state!");
        return;
    }"""

new_checks = """    if (!window.supabaseClient) {
        alert("CRASH: window.supabaseClient es nulo!");
        console.error("No supabase client!");
        return;
    }
    if (!state.tenantId) {
        alert("CRASH: state.tenantId es nulo!");
        console.error("No tenantId in state!");
        return;
    }"""

js = js.replace(old_checks, new_checks)

# And let's add an explicit alert if it succeeds just to prove it!
js = js.replace(
    'console.log("Guardado automático exitoso");',
    'console.log("Guardado automático exitoso");\n            alert("¡ÉXITO! Supabase confirmó que la sucursal se guardó en la nube.");'
)

with open('dashboard.js', 'w') as f:
    f.write(js)
