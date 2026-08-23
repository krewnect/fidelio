import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'href="styles\.css\?v=\d+"', 'href="styles.css?v=' + str(__import__('time').time()) + '"', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
