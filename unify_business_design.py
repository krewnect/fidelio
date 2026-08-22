import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace accordion-card with content-panel in the main layout (we leave specific ones like AI campaign modules alone if needed, but for layout panels content-panel is better)
# Wait, let's just do a targeted replacement for the layout containers.
html = re.sub(r'<div class="accordion-card"(.*?)>', r'<div class="content-panel"\1>', html)

# Let's ensure workspace-header buttons have fidelio-btn-primary
# Actually, the user specifically mentioned Business modules:
# Cajeros y Equipo (tab-staff)
# The Bank (tab-bank)
# Caja y Registro de Pagos (tab-caja)
# Campañas Push (tab-marketing)
# My Business (tab-mybusiness)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Replaced accordion-card with content-panel globally.")
