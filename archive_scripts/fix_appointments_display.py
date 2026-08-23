import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX APPOINTMENTS (Remove inline display:none which overrides tab activation)
html = html.replace('<section id="tab-appointments" class="tab-content" style="display:none;">', '<section id="tab-appointments" class="tab-content">')
html = html.replace('<button class="nav-tab" data-tab="tab-appointments" id="nav-appointments" style="display:none;">', '<button class="nav-tab" data-tab="tab-appointments" id="nav-appointments">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Appointments inline styles removed.")
