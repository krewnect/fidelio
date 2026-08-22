import re

with open('business.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = "alert('Error de conexión.');"
replacement = "alert('Error de conexión: ' + error.message);"

if target in html:
    html = html.replace(target, replacement)
    with open('business.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected detailed error alert")
else:
    print("Target not found")
