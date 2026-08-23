import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('onclick="location.reload()"', 'onclick="document.querySelector(\'.nav-tab[data-tab=\\\'tab-home\\\']\').click()"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
