import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Emojis in dashboard.js to replace
replacements = {
    '👀 ': '',
    '🔥 ': '',
    '🍻 ': ''
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed emojis from dashboard.js")
