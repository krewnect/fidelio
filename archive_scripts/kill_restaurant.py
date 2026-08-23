import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = "business_type: businessType || 'restaurant'"
replacement = "business_type: businessType || 'business'"

if target in js:
    js = js.replace(target, replacement)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Killed restaurant in app.js")
