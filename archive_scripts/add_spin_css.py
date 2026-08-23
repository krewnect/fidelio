import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

spin_css = """
                    @keyframes spinY {
                        0% { transform: scale(0.65) rotateY(0deg); }
                        50% { transform: scale(0.7) rotateY(180deg); }
                        100% { transform: scale(0.65) rotateY(360deg); }
                    }
                    @media (min-width: 1400px) {
                        @keyframes spinY {
                            0% { transform: scale(0.75) rotateY(0deg); }
                            50% { transform: scale(0.8) rotateY(180deg); }
                            100% { transform: scale(0.75) rotateY(360deg); }
                        }
                    }
"""

html = html.replace('/* Dynamic Island */', spin_css + '\n                    /* Dynamic Island */')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
