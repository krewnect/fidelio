import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_badge = r'<span style="background: linear-gradient[^>]*>Lv\. 1 Maestro</span>'
html = re.sub(bad_badge, '', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
