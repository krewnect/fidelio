import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the "Configurar" buttons in tab-loyalty to trigger startDesignerFlow
# The buttons look like: <button class="btn btn-outline" style="width: 100%; justify-content: center;" onclick="alert('Configurar Tarjeta Monedero')">Configurar</button>
# We will use regex to catch all of them in tab-loyalty.

html = re.sub(r'onclick="alert\(\'Configurar (.*?)\'\)"', r'onclick="startDesignerFlow(\'\1\')"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Loyalty Configure buttons hooked to startDesignerFlow")
