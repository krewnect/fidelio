import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will inject min-height and line-height into the overriding .nav-tab rule to ensure they never clip.
old_rule = """.nav-tab {
    border-radius: 10px !important;
    margin: 4px 16px !important;
    padding: 12px 16px !important;
    color: #4B5563 !important;
    font-weight: 500 !important;
}"""

new_rule = """.nav-tab {
    border-radius: 10px !important;
    margin: 4px 16px !important;
    padding: 12px 16px !important;
    color: #4B5563 !important;
    font-weight: 500 !important;
    min-height: 44px !important;
    line-height: 1.2 !important;
    display: flex !important;
    align-items: center !important;
    box-sizing: border-box !important;
}"""

if old_rule in html:
    html = html.replace(old_rule, new_rule)
else:
    print("WARNING: Exact match failed")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Sidebar CSS updated.")
