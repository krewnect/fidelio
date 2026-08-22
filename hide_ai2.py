import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_style = "<style>"
new_style = "<style>\n        .gemini-insight-panel { display: none !important; } /* Desactivación temporal de IA */"

if old_style in html:
    html = html.replace(old_style, new_style, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("AI panels hidden.")
else:
    print("WARNING: Could not find anchor.")

