import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add cache buster to all custom js and css files
html = re.sub(r'src="live_dashboard\.js.*?"', 'src="live_dashboard.js?v=' + str(__import__('time').time()) + '"', html)
html = re.sub(r'src="fidelito\.js.*?"', 'src="fidelito.js?v=' + str(__import__('time').time()) + '"', html)
html = re.sub(r'href="styles\.css.*?"', 'href="styles.css?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
