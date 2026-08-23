import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove save campaign success toast
js = js.replace('if (typeof window.showToast === \'function\') window.showToast("Campaña guardada ☁️", "success");', '')

# Remove update form success toast
js = js.replace('if (typeof window.showToast === \'function\') window.showToast(\'Formulario actualizado correctamente\', \'success\');', '')

# Remove Gemini analyzing toast (it's obvious from the button spinner)
js = js.replace('if (typeof window.showToast === \'function\') window.showToast("Gemini AI está analizando tu negocio...", "info");', '')

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
