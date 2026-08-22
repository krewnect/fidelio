import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_rule = """.nav-tab.admin-only-item {
    padding: 8px 16px !important; 
    min-height: 44px !important;
}"""

new_rule = """.nav-tab.admin-only-item {
    -webkit-appearance: none !important;
    appearance: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    padding: 0 16px !important;
    height: 42px !important;
    min-height: 42px !important;
    max-height: 42px !important;
    line-height: 42px !important;
    flex-shrink: 0 !important;
    box-sizing: border-box !important;
    border: none !important;
    background: transparent;
    overflow: visible !important;
}
.nav-tab.admin-only-item i {
    line-height: 42px !important;
    height: 42px !important;
    display: flex !important;
    align-items: center !important;
}"""

if old_rule in html:
    html = html.replace(old_rule, new_rule)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Nuclear fix applied.")
else:
    print("WARNING: Exact match failed")

