import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Restore the outer grid to 2fr 1fr so the ROI banner is wide enough
html = html.replace(
    '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 24px; margin-bottom: 24px;" class="stagger-1">',
    '<div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px; margin-bottom: 24px;" class="stagger-1">'
)

# Add flex-wrap and gap to the inner ROI banner so it never overlaps text
html = html.replace(
    '<div class="metric-card-hover" style="background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%); border-radius: var(--radius-md); padding: 40px; color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-lg); position: relative; overflow: hidden;">',
    '<div class="metric-card-hover" style="background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%); border-radius: var(--radius-md); padding: 40px; color: white; display: flex; justify-content: space-between; align-items: center; gap: 32px; flex-wrap: wrap; box-shadow: var(--shadow-lg); position: relative; overflow: hidden;">'
)

# And make sure the inner left side text doesn't force a width that causes overlapping
html = html.replace(
    'max-width: 450px;',
    'max-width: 100%;'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
