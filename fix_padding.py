import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_rule = """.nav-tab {
    -webkit-appearance: none;
    appearance: none;
    border-radius: 10px;
    margin: 4px 16px;
    padding: 12px 16px;
    color: #4B5563;
    font-weight: 500;
    line-height: 1.5;
    display: flex;
    align-items: center;
    box-sizing: border-box;
    overflow: visible !important;
    min-height: 44px;
    height: auto;
    flex-shrink: 0;
}
.nav-tab.admin-only-item {
    padding-bottom: 14px !important; /* Extra padding just in case */
    min-height: 48px !important;
}"""

new_rule = """.nav-tab {
    -webkit-appearance: none;
    appearance: none;
    border-radius: 10px;
    margin: 4px 16px;
    padding: 8px 16px;
    color: #4B5563;
    font-weight: 500;
    line-height: 1.2;
    display: flex;
    align-items: center;
    box-sizing: border-box;
    overflow: visible !important;
    min-height: 44px;
    height: auto;
    flex-shrink: 0;
}
.nav-tab.admin-only-item {
    padding: 8px 16px !important; 
    min-height: 44px !important;
}"""

if old_rule in html:
    html = html.replace(old_rule, new_rule)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Padding fixed.")
else:
    print("WARNING: Exact match failed")

