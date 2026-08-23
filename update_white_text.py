import re

file_path = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def fix_dark_bg_text(match):
    classes = match.group(1)
    if re.search(r'\bbg-[a-z]+-[56789]00\b', classes) and 'text-slate-900' in classes:
        classes = re.sub(r'\btext-slate-900\b', 'text-white', classes)
        classes = re.sub(r'\bhover:text-slate-900\b', 'hover:text-white', classes)
    return 'class="' + classes + '"'

content = re.sub(r'class="([^"]+)"', fix_dark_bg_text, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated text on dark backgrounds")
