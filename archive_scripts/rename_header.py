import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<h3 style="font-size:18px; font-weight:700; color:#111827; margin-bottom:16px;">Solicitudes Recientes</h3>', '<h3 style="font-size:18px; font-weight:800; color:#e11d48; margin-bottom:16px;"><i class="fa-solid fa-bell"></i> Solicitudes y Alertas Pendientes</h3>')

# Also bump cache
html = re.sub(r'src="dashboard\.js\?v=\d+"', 'src="dashboard.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
