import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_render = """        if (!crmTableBody || !state || !state.customers) return;"""

new_render = """        if (!crmTableBody || typeof state === 'undefined' || !state.customers || !Array.isArray(state.customers)) return;"""

if old_render in js:
    js = js.replace(old_render, new_render)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v2.js renderCRMTable patched again.")
else:
    print("WARNING: Could not find old_render in dashboard_v2.js")

