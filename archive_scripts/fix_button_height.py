import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will enforce a strict height of 42px for all three buttons so they are perfectly identical.
old_button1 = '<button class="fidelio-btn-primary" style="flex: 1; white-space: nowrap; padding: 12px 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important;">'
new_button1 = '<button class="fidelio-btn-primary" style="flex: 1; height: 42px !important; box-sizing: border-box !important; white-space: nowrap; padding: 0 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important;">'

old_label = '<label class="fidelio-btn-primary" style="flex: 1; white-space: nowrap; padding: 12px 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important; margin: 0; cursor: pointer;">'
new_label = '<label class="fidelio-btn-primary" style="flex: 1; height: 42px !important; box-sizing: border-box !important; white-space: nowrap; padding: 0 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important; margin: 0; cursor: pointer;">'

old_button2 = '<button class="fidelio-btn-primary" style="flex: 1; white-space: nowrap; padding: 12px 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important;"><i class="fa-solid fa-plus"></i> Añadir Sucursal</button>'
new_button2 = '<button class="fidelio-btn-primary" style="flex: 1; height: 42px !important; box-sizing: border-box !important; white-space: nowrap; padding: 0 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important;"><i class="fa-solid fa-plus"></i> Añadir Sucursal</button>'


html = html.replace(old_button1, new_button1)
html = html.replace(old_label, new_label)
html = html.replace(old_button2, new_button2)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Button heights strictly enforced.")
