import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace any instance of accordion-card inside class attributes
html = html.replace('accordion-card ', 'content-panel ')
html = html.replace(' accordion-card', ' content-panel')
html = html.replace('"accordion-card"', '"content-panel"')

# Make sure we don't have double content-panel
html = html.replace('content-panel content-panel', 'content-panel')
html = html.replace('content-panel  content-panel', 'content-panel')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Accordion cards completely eliminated.")
