import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add white-space: nowrap to the global button classes
html = html.replace('gap: 8px !important;', 'gap: 8px !important;\n    white-space: nowrap !important;')

# Remove max-width: 800px from tab-branches so it breathes properly
html = html.replace('<div class="content-panel" style="max-width: 800px;">', '<div class="content-panel">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Global fixes applied.")
