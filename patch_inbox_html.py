import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_menu = """<div class="nav-tab admin-only-item" data-tab="tab-inbox" style="display:none;"><i class="fa-solid fa-inbox"></i> Inbox de Soporte</div>"""
new_menu = """<div class="nav-tab admin-only-item" data-tab="tab-inbox" style="display:none; justify-content:space-between; align-items:center;">
                    <div><i class="fa-solid fa-inbox"></i> Inbox de Soporte</div>
                    <span id="inbox-alert-badge" style="display:none; background:#EF4444; color:white; font-size:10px; font-weight:800; padding:2px 6px; border-radius:10px; align-items:center; justify-content:center;">0</span>
                </div>"""

if old_menu in html:
    html = html.replace(old_menu, new_menu)
else:
    print("WARNING: Could not find sidebar menu in HTML")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML Inbox Alert patched.")
