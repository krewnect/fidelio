import re

with open('index.html', 'r') as f:
    html = f.read()

stamps_css = """
                    /* Stamp Styles */
                    .stamp-coin { width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 700; transition: all 0.3s; }
                    .stamp-coin.filled { background: #8b5cf6; color: white; box-shadow: 0 4px 10px rgba(139, 92, 246, 0.4); }
                    .stamp-coin.empty { background: #f3f4f6; color: #9ca3af; border: 2px dashed #d1d5db; }
                    
                    /* Back of Wallet Pass */"""

html = html.replace('/* Back of Wallet Pass */', stamps_css)

with open('index.html', 'w') as f:
    f.write(html)
