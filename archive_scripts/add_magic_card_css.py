import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

magic_card_css = """
        /* CAMPAIGN MAGIC CARDS */
        .campaign-magic-card:hover { transform: translateY(-5px) scale(1.02); }
        .campaign-magic-card:hover .campaign-magic-inner { box-shadow: 0 20px 40px -10px rgba(0,0,0,0.3); }
        .campaign-magic-card:hover .campaign-magic-actions { transform: translateY(0); }
        .campaign-magic-card:active { transform: scale(0.98); }
        
        #campaigns-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 24px;
            margin-top: 24px;
        }
"""

if "CAMPAIGN MAGIC CARDS" not in html:
    html = html.replace('/* BUTTON HOVER FX */', magic_card_css + '\n        /* BUTTON HOVER FX */')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
