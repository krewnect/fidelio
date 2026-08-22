import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Restore Mis Campañas
html = html.replace('<!-- Oculto para unificar UX -->\n                <button class="nav-tab" data-tab="tab-builder"', '<button class="nav-tab" data-tab="tab-campaigns" id="nav-campaigns"><i class="fa-solid fa-list"></i> Mis Campañas</button>\n                <button class="nav-tab" data-tab="tab-builder"')

# Hide Fidelización
html = re.sub(
    r'<button class="nav-tab" data-tab="tab-loyalty" id="nav-loyalty"><i class="fa-solid fa-gift"></i> Fidelización</button>',
    r'<!-- Oculto para unificar UX: Fidelizacion movida al Creador -->',
    html
)

# Hide Tarjetas Especiales
html = re.sub(
    r'<button class="nav-tab plan-pro-only" data-tab="tab-special-cards" id="nav-special-cards"><i class="fa-solid fa-address-card"></i> Tarjetas & Reglas</button>',
    r'<!-- Oculto para unificar UX: Reglas movidas al Creador -->',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
