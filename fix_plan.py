import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = "const isBusiness = plan === 'business' || plan === 'enterprise' || isAdmin;"
replacement = "const isBusiness = plan === 'business' || plan === 'enterprise' || plan === 'restaurant' || isAdmin;"

if target in js:
    js = js.replace(target, replacement)
    
target2 = "const isPro = plan === 'business' || plan === 'enterprise' || isAdmin;"
replacement2 = "const isPro = plan === 'business' || plan === 'enterprise' || plan === 'restaurant' || isAdmin;"

if target2 in js:
    js = js.replace(target2, replacement2)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Fixed plan logic")
