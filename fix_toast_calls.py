import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make sure all typeof showToast checks use window.showToast
js = js.replace("typeof showToast === 'function'", "typeof window.showToast === 'function'")
js = js.replace("showToast(", "window.showToast(")
js = js.replace("window.window.showToast", "window.showToast")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

