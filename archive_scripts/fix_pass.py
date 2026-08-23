import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_pass = """function updatePassRender() {
        window._updatePassRenderGlobal = true; // Debug flag
        const passRender = document.getElementById('pass-render');
        if (!passRender) return;"""

new_pass = """function updatePassRender() {
        window._updatePassRenderGlobal = true; // Debug flag
        const passRender = document.getElementById('pass-render');
        if (!passRender || typeof state === 'undefined' || !state.customers || !state.vipTiers) return;"""

if old_pass in js:
    js = js.replace(old_pass, new_pass)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v2.js updatePassRender patched.")
else:
    print("WARNING: Could not find old_pass in dashboard_v2.js")

