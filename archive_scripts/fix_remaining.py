import re

# Fix index.html CSS
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Just in case, clean up any lingering var(--surface) that grep caught
html = re.sub(r'background:\s*var\(--surface\);?', '', html)
html = re.sub(r'var\(--shadow-[^)]*\)', '0 10px 30px rgba(0,0,0,0.05)', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Fix dashboard_v2.js
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r'background:\s*var\(--surface\);?', 'background: #ffffff;', js)
js = js.replace('var(--shadow-sm)', '0 10px 30px rgba(0,0,0,0.05)')
js = js.replace('.btn-primary', '.fidelio-btn-primary')

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Remaining inline/JS overrides cleaned.")
