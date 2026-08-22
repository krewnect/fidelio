import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_fetch = "const res = await fetch('https://fidelio-41j9.onrender.com/api/admin/merchant/' + id, {"
new_fetch = "const res = await fetch('/api/admin/merchant/' + id, {"

if old_fetch in js:
    js = js.replace(old_fetch, new_fetch)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v2.js fetch patched.")
else:
    print("WARNING: Could not find old_fetch in dashboard_v2.js")

