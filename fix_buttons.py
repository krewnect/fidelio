import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix btn-primary CSS
old_css = ".btn-primary { background: var(--text-main); color: white; box-shadow: 0 4px 14px rgba(0,0,0,0.1); }"
new_css = ".btn-primary { background: var(--primary); color: white; box-shadow: 0 4px 14px rgba(139,92,246,0.3); border:none; }"
html = html.replace(old_css, new_css)

old_css_hover = ".btn-primary:hover { background: #000000; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }"
new_css_hover = ".btn-primary:hover { background: #7c3aed; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(139,92,246,0.4); border:none; }"
html = html.replace(old_css_hover, new_css_hover)

# Restore Sucursales buttons
html = html.replace('class="btn btn-primary" onclick="alert(\'Cargar Layout CSV...\')"', 'class="btn btn-outline" style="background:transparent; color:var(--text-main); border:1px solid var(--border-color);" onclick="alert(\'Cargar Layout CSV...\')"')
html = html.replace('class="btn btn-primary" onclick="alert(\'Subir Base de Datos...\')"', 'class="btn btn-primary" style="background:var(--text-main); color:white; border:none;" onclick="alert(\'Subir Base de Datos...\')"')

# Make Actualizar button use var(--primary) explicitly just in case
html = html.replace('class="btn btn-primary" onclick="window.location.reload()"><i class="fa-solid fa-rotate-right"></i> Actualizar</button>', 'class="btn btn-primary" style="background: var(--primary); border: none;" onclick="window.location.reload()"><i class="fa-solid fa-rotate-right"></i> Actualizar</button>')

# Nueva Campana button in Mis Campanas
html = html.replace('class="btn btn-primary" onclick="openCampaignModal()"', 'class="btn btn-primary" style="background: var(--primary); border: none;" onclick="openCampaignModal()"')

# Fix CRM Buttons
# The script previously changed them to btn-primary. The CSS fix above should make btn-primary purple. Let's make sure inline styles don't force black.
html = html.replace('class="btn btn-primary" style="font-size: 13px;" onclick="exportCRM()"><i class="fa-solid fa-download"></i> Exportar CSV', 'class="btn btn-primary" style="background: var(--primary); border: none; font-size: 13px;" onclick="exportCRM()"><i class="fa-solid fa-download"></i> Exportar CSV')
html = html.replace('class="btn btn-primary" style="font-size: 13px;" onclick="alert(\'Abrir campañas\')"><i class="fa-solid fa-bullhorn"></i> Enviar Campaña', 'class="btn btn-primary" style="background: var(--primary); border: none; font-size: 13px;" onclick="alert(\'Abrir campañas\')"><i class="fa-solid fa-bullhorn"></i> Enviar Campaña')


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Button colors and Sucursales buttons reverted/fixed.")
