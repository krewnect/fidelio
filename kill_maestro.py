import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern = r"document\.getElementById\('header-business-category'\)\.innerHTML = `<span style='display:flex; align-items:center; gap:6px;'><span>\$\{bCatDisp\}</span> <span style='background: linear-gradient.*?Lv\. 1 Maestro</span></span>`;"
replacement = "document.getElementById('header-business-category').innerHTML = `<span>${bCatDisp}</span>`;"

js = re.sub(pattern, replacement, js)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
