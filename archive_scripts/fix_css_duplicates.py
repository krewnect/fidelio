import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I am going to delete the second injection of apple-section and stagger animations entirely, 
# and just make sure the FIRST one is correct.

# Actually, let's just make ALL apple-sections have opacity: 1 !important just in case.
html = html.replace('.apple-section {', '.apple-section {\n                        opacity: 1 !important;\n                        visibility: visible !important;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
