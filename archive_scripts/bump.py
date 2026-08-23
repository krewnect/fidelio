import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'src="dashboard\.js\?v=\d+"', 'src="dashboard.js?v=' + str(__import__('time').time()) + '"', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
