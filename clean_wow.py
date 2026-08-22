import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'/\* PROJECT WOW: ULTRA PREMIUM STYLING \*/.*?rgba\(0,0,0,0\.02\)\s*!\s*important;\s*\}'
html = re.sub(pattern, '', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
