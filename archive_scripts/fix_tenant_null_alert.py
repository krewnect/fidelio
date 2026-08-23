import re

with open('dashboard.js', 'r') as f:
    js = f.read()

js = js.replace(
    "if (window.supabaseClient && state.tenantId) {",
    "if (!state.tenantId) { alert('¡LA VARIABLE TENANT ID ESTÁ NULA AL HACER CLIC!'); } else if (window.supabaseClient && state.tenantId) {"
)

with open('dashboard.js', 'w') as f:
    f.write(js)
