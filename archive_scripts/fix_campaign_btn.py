import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_btn = '<button class="fidelio-btn-primary"><i class="fa-solid fa-wand-magic-sparkles"></i> Diseñar Nueva Campaña Mágica</button>'
new_btn = '<button class="fidelio-btn-primary" onclick="window.openCampaignModal()"><i class="fa-solid fa-wand-magic-sparkles"></i> Diseñar Nueva Campaña Mágica</button>'

if old_btn in html:
    html = html.replace(old_btn, new_btn)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Campaign button fixed.")
else:
    print("Could not find the exact campaign button string.")

