import sys

# 1. Fix JS Error
with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_js = """        const loyaltyModes = document.querySelectorAll('input[name="loyalty_mode"]');
        const modeCards = document.querySelectorAll('input[name="loyalty_mode"] + .role-icon').map(el => el.parentElement);"""
new_js = """        const loyaltyModes = document.querySelectorAll('input[name="loyalty_mode"]');
        const modeCards = Array.from(document.querySelectorAll('input[name="loyalty_mode"] + .role-icon')).map(el => el.parentElement);"""

js = js.replace(old_js, new_js)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Fix HTML Colors
with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Cashback Card
html = html.replace(
    '<div class="role-icon" style="color:#10B981; background:rgba(16, 185, 129, 0.1);"><i class="fa-solid fa-wallet"></i></div>',
    '<div class="role-icon" style="color:var(--accent-violet); background:rgba(139, 92, 246, 0.1);"><i class="fa-solid fa-wallet"></i></div>'
)
# Stamps Card
html = html.replace(
    '<div class="role-icon" style="color:#F59E0B; background:rgba(245, 158, 11, 0.1);"><i class="fa-solid fa-stamp"></i></div>',
    '<div class="role-icon" style="color:var(--accent-violet); background:rgba(139, 92, 246, 0.1);"><i class="fa-solid fa-stamp"></i></div>'
)
# Membership Card
html = html.replace(
    '<div class="role-icon" style="color:#3B82F6; background:rgba(59, 130, 246, 0.1);"><i class="fa-solid fa-id-card-clip"></i></div>',
    '<div class="role-icon" style="color:var(--accent-violet); background:rgba(139, 92, 246, 0.1);"><i class="fa-solid fa-id-card-clip"></i></div>'
)
# Prepaid Card
html = html.replace(
    '<div class="role-icon" style="color:#EC4899; background:rgba(236, 72, 153, 0.1);"><i class="fa-solid fa-money-bill-transfer"></i></div>',
    '<div class="role-icon" style="color:var(--accent-violet); background:rgba(139, 92, 246, 0.1);"><i class="fa-solid fa-money-bill-transfer"></i></div>'
)
# Custom Card
html = html.replace(
    '<div class="role-icon" style="color:var(--text-main); background:var(--bg-input);"><i class="fa-solid fa-wand-magic-sparkles"></i></div>',
    '<div class="role-icon" style="color:var(--accent-violet); background:rgba(139, 92, 246, 0.1);"><i class="fa-solid fa-wand-magic-sparkles"></i></div>'
)

# Panel Headers
html = html.replace('color:#10B981;', 'color:var(--accent-violet);')
html = html.replace('color:#F59E0B;', 'color:var(--accent-violet);')

# Slider Accent Color
html = html.replace('accent-color: #10B981;', 'accent-color: var(--accent-violet);')

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated JS Map error and HTML Colors.")
