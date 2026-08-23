with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("app-shell opens:", len(re.findall(r'<div class="app-shell"', text)))
print("app-main opens:", len(re.findall(r'<main class="app-main"', text)))
print("app-main closes:", len(re.findall(r'</main>', text)))
