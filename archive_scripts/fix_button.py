import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_rule = """.nav-tab {
    border-radius: 10px !important;
    margin: 4px 16px !important;
    padding: 12px 16px !important;
    color: #4B5563 !important;
    font-weight: 500 !important;
    line-height: normal !important;
    display: flex !important;
    align-items: center !important;
    box-sizing: border-box !important;
    overflow: visible !important;
    height: auto !important;
}"""

new_rule = """.nav-tab {
    -webkit-appearance: none !important;
    appearance: none !important;
    border-radius: 10px !important;
    margin: 4px 16px !important;
    padding: 12px 16px !important;
    color: #4B5563 !important;
    font-weight: 500 !important;
    line-height: normal !important;
    display: flex !important;
    align-items: center !important;
    box-sizing: border-box !important;
    overflow: visible !important;
    min-height: 44px !important;
    height: auto !important;
}"""

if old_rule in html:
    html = html.replace(old_rule, new_rule)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Nav tab appearance fixed.")
else:
    print("WARNING: Exact match failed")

