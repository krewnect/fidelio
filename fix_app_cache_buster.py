import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Change all references from pass.html to card.html
app_js = app_js.replace("pass.html", "card.html")

# Update cache buster
app_js = re.sub(r'v5_', 'v6_', app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
