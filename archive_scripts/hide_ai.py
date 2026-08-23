import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_style = "/* 1. Reset & Variables */"
new_style = "/* 1. Reset & Variables */\n.gemini-insight-panel { display: none !important; } /* Desactivación temporal de IA por inestabilidad de API gratuita */\n"

if old_style in html:
    html = html.replace(old_style, new_style, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("AI panels hidden via CSS.")
else:
    print("WARNING: Could not find anchor.")

