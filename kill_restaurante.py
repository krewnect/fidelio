import re

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('de tu restaurante para el radar', 'de tu negocio para el radar')
html = html.replace('saldo digital digital de tu restaurante', 'saldo digital de tu negocio')
html = html.replace('nuevos restaurantes.', 'nuevos negocios.')
html = html.replace('<th style="padding: 16px;">Restaurante</th>', '<th style="padding: 16px;">Negocio</th>')
html = html.replace('placeholder="Negocio/Restaurante..."', 'placeholder="Filtrar Negocio..."')
html = html.replace('Listado de restaurantes afiliados', 'Listado de negocios afiliados')
html = html.replace('Plan Business (Restaurantes)', 'Plan Business (Negocios Generales)')
html = html.replace('Restaurantes cuyos pagos han fallado', 'Negocios cuyos pagos han fallado')
html = html.replace('atención a restaurantes.', 'atención a negocios afiliados.')
html = html.replace('Restaurante XYZ', 'Negocio XYZ')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# Update dashboard_v2.js
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('datos geográficos de su restaurante', 'datos geográficos de su negocio')
js = js.replace('Cargando restaurantes...', 'Cargando negocios...')
js = js.replace('a este restaurante?', 'a este negocio?')

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Restaurante terminology completely purged and replaced with Negocio.")
