import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'<!-- RADAR DE FUGA -->[\s\S]*?Lanzar Salvavidas\n                        </button>\n                    </div>\n                </div>'
html = re.sub(pattern, '', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
