import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the card background pop with a glassmorphism frosted glass effect so it's not "sober"
target = 'class="card-face card-front pass-preview-card premium-white-card" style="background: #ffffff;'
replacement = 'class="card-face card-front pass-preview-card premium-white-card" style="background: rgba(255,255,255,0.95); backdrop-filter: blur(20px);'
html = html.replace(target, replacement)

# Do the same for the back
target_back = 'class="card-face card-back pass-preview-card premium-white-card" style="background: #ffffff;'
replacement_back = 'class="card-face card-back pass-preview-card premium-white-card" style="background: rgba(255,255,255,0.95); backdrop-filter: blur(20px);'
html = html.replace(target_back, replacement_back)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
