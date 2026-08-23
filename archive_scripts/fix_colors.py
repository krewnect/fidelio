import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace green hex and classes with violet equivalents
html = html.replace('#10b981', 'var(--accent-violet)')
html = html.replace('#10B981', 'var(--accent-violet)')
html = html.replace('16, 185, 129', '139, 92, 246') # rgba emerald -> rgba violet
html = html.replace('var(--accent-emerald)', 'var(--accent-violet)')
html = html.replace('#34D399', '#6D28D9') # light emerald to dark violet

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
