import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Force absolute Hex colors for btn-primary to ensure it is purple and visible
old_css = ".btn-primary { background: var(--primary); color: white; box-shadow: 0 4px 14px rgba(139,92,246,0.3); border:none; }"
new_css = ".btn-primary { background: #8b5cf6 !important; color: white !important; box-shadow: 0 4px 14px rgba(139,92,246,0.3); border:none; }"
html = html.replace(old_css, new_css)

old_css_hover = ".btn-primary:hover { background: #7c3aed; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(139,92,246,0.4); border:none; }"
new_css_hover = ".btn-primary:hover { background: #7c3aed !important; color: white !important; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(139,92,246,0.4); border:none; }"
html = html.replace(old_css_hover, new_css_hover)

# Also fix the inline styles that might be using var(--primary) or var(--accent-violet) that could be failing
html = html.replace('background: var(--primary);', 'background: #8b5cf6 !important;')
html = html.replace('background: var(--accent-violet);', 'background: #8b5cf6 !important;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Button colors forced to Hex #8b5cf6.")
