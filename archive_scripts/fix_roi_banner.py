import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the dark gradient with pure Fidelio Purple gradient
html = html.replace(
    'background: linear-gradient(135deg, var(--accent-violet) 0%, #1e0542 100%);',
    'background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);'
)

# Also fix the weird background glow inside the banner
html = html.replace(
    'background: var(--bg-input);',
    'background: rgba(255, 255, 255, 0.1);'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

