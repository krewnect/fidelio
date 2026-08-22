import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix h4 colors
html = html.replace('margin:0 0 8px; font-size:18px;"', 'margin:0 0 8px; font-size:18px; color: var(--text-main);"')

# Just in case var(--text-main) is failing or not set properly on the h4, let's also force it:
# Actually var(--text-main) should work if the CSS variables are correct.

# Make sure the modal background itself is solid
html = html.replace('background:var(--bg-body); width:90%; max-width:700px;', 'background:var(--bg-body); width:90%; max-width:700px; color: var(--text-main);')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
