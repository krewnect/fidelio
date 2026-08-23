import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

modal_pattern = r'<!-- QUICK CAMPAIGN WIZARD MODAL -->[\s\S]*?<!-- SETTINGS OFF-CANVAS -->'
html = re.sub(modal_pattern, '<!-- SETTINGS OFF-CANVAS -->', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
