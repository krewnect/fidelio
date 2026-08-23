import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_refresh = """            // Refrescar lista de negocios
            if(typeof window.loadFidelioTeam === 'function') {
                window.loadFidelioTeam();
            }"""

new_refresh = """            // Refrescar lista de negocios
            if(typeof window.loadMerchantsControl === 'function') {
                window.loadMerchantsControl();
            }"""

if old_refresh in js:
    js = js.replace(old_refresh, new_refresh)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v2.js UI refresh patched.")
else:
    print("WARNING: Could not find refresh code in dashboard_v2.js")

