import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace("script.src = 'dashboard.js?v='", "script.src = 'dashboard_v2.js?v='")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
