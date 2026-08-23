import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_logic = "el.style.display = el.tagName === 'BUTTON' ? 'flex' : 'block';"
new_logic = "el.style.display = 'flex';"

if old_logic in js:
    js = js.replace(old_logic, new_logic)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("JS logic updated.")
else:
    print("WARNING: Logic not found.")
