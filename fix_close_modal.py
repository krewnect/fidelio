import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace closeModal hallucination with native DOM style trick
html = html.replace("closeModal('modal-admin-merchant')", "document.getElementById('modal-admin-merchant').style.display='none'")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("closeModal ReferenceError fixed.")
