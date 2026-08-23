import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_html = r'<div style="margin-top:24px; background: linear-gradient\(135deg, rgba\(139,92,246,0\.1\) 0%, rgba\(59,130,246,0\.1\) 100%\); padding:20px 24px; border-radius:16px; display:flex; align-items:center; gap:20px; border:1px solid rgba\(139,92,246,0\.2\);">.*?Copiloto de Marketing IA.*?</div>\s*</div>\s*</div>'

html = re.sub(target_html, '</div>', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove the triggerAIMagicDesign function entirely to clean up the codebase
target_js = r'window\.triggerAIMagicDesign = function\(\) \{.*?(?: \}, 600\);\n\};)'
js = re.sub(target_js, '', js, flags=re.DOTALL)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
