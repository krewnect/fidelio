import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove save campaign success toast
js = js.replace('if (typeof window.showToast === \'function\') window.showToast("Campaña cargada en el editor", "success");', '')

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
