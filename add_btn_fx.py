import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add hover states to sidebar buttons
css_fx = """
        /* BUTTON HOVER FX */
        .nav-tab { position: relative; overflow: hidden; }
        .nav-tab::after {
            content: ''; position: absolute; top: 50%; left: 50%; width: 0; height: 0;
            background: rgba(139, 92, 246, 0.1); border-radius: 50%; transform: translate(-50%, -50%); transition: width 0.4s, height 0.4s;
        }
        .nav-tab:active::after { width: 300px; height: 300px; opacity: 0; transition: 0s; }
"""

if "BUTTON HOVER FX" not in html:
    html = html.replace('/* SIDEBAR */', css_fx + '\n        /* SIDEBAR */')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
