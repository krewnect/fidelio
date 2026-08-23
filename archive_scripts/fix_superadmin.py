import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('leads_orig.html', 'r', encoding='utf-8') as f:
    leads_orig = f.read()
    
with open('db_orig.html', 'r', encoding='utf-8') as f:
    db_orig = f.read()

with open('bank_orig.html', 'r', encoding='utf-8') as f:
    bank_orig = f.read()

# Replace sections
html = re.sub(r'<section id="tab-leads" class="tab-content">.*?</section>', leads_orig.strip(), html, flags=re.DOTALL)
html = re.sub(r'<section id="tab-global-db" class="tab-content">.*?</section>', db_orig.strip(), html, flags=re.DOTALL)
html = re.sub(r'<section id="tab-bank" class="tab-content">.*?</section>', bank_orig.strip(), html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Super admin tabs restored!")
