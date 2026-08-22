import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove inline background: var(--surface), box-shadow, border-radius on elements that are already panels
# Actually, I'll just strip specific known inline properties that clash with the new aesthetic

def clean_inline_style(match):
    style = match.group(1)
    # Remove old surface background
    style = re.sub(r'background:\s*var\(--surface\);?', '', style)
    # Remove old shadows
    style = re.sub(r'box-shadow:\s*var\(--shadow-[^)]*\);?', '', style)
    style = re.sub(r'box-shadow:\s*0 10px 30px rgba\(0,0,0,0\.03\);?', '', style)
    # Remove old borders if they conflict
    style = re.sub(r'border-radius:\s*20px;?', '', style)
    
    # Also fix buttons that use var(--accent-violet) directly in inline styles where a class should do it
    style = style.strip()
    if style.endswith('style="') or style.endswith('style=" '): 
        # basically if empty style block, we can just return nothing
        pass
        
    return 'style="' + style + '"'

html = re.sub(r'style="([^"]*)"', clean_inline_style, html)

# Also ensure any standalone div that was acting as a panel gets the class if it lacks it
# We know some had: div style="background: var(--surface); padding: 32px;"
html = re.sub(r'<div([^>]*)style="([^"]*padding:\s*32px[^"]*)"', r'<div class="content-panel"\1style="\2"', html)

# Fix any duplicated classes just in case
html = html.replace('class="content-panel class="content-panel"', 'class="content-panel"')
html = html.replace('class="content-panel" class="content-panel"', 'class="content-panel"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Inline styles cleaned.")
