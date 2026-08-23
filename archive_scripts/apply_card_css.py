import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add pass-preview-card class to the front face
html = html.replace('<div class="card-face card-front">', '<div class="card-face card-front pass-preview-card">')

# Add pass-preview-card class to the back face (if it exists)
html = html.replace('<div class="card-face card-back">', '<div class="card-face card-back pass-preview-card">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Injected pass-preview-card class to index.html")
