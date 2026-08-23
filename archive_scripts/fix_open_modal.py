import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace openModal with the native DOM style display trick used across the codebase
js = js.replace("openModal('modal-admin-merchant');", "document.getElementById('modal-admin-merchant').style.display = 'flex';")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("openModal ReferenceError fixed.")
