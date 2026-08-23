import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the glass card padding
html = html.replace(
    '<div style="position: relative; z-index: 2; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); box-shadow: inset 0 0 20px rgba(255,255,255,0.05);">',
    '<div style="position: relative; z-index: 2; background: rgba(255,255,255,0.05); padding: 24px; border-radius: 20px; backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); box-shadow: inset 0 0 20px rgba(255,255,255,0.05); min-width: max-content;">'
)

# Fix the text to never wrap
html = html.replace(
    '<div style="font-size: 13px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; margin-bottom: 8px;">Ingreso Atribuido a Lealtad</div>',
    '<div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.8; margin-bottom: 8px; white-space: nowrap;">Ingreso Atribuido a Lealtad</div>'
)

# Since we used min-width: max-content on the inner glass card, let's make sure the grid doesn't squeeze it too hard.
# The grid is: grid-template-columns: 2fr 1fr;
# We will change it to auto-fit or minmax(300px, 1fr) for the right side? No, minmax(auto, 1fr) is better.
html = html.replace(
    '<div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px; margin-bottom: 24px;" class="stagger-1">',
    '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 24px; margin-bottom: 24px;" class="stagger-1">'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
