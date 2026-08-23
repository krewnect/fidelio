import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the main campaign cards background
js = js.replace(
    '<div class="campaign-magic-inner" >',
    '<div class="campaign-magic-inner" style="background: linear-gradient(135deg, #7C3AED 0%, #4C1D95 100%); height: 100%; border-radius: 20px; position: relative; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 10px 25px rgba(124, 58, 237, 0.2);">'
)

# Fix the special cards background
js = js.replace(
    '<div ></div>',
    '<div style="height: 6px; background: linear-gradient(90deg, #7C3AED, #4C1D95); margin: -24px -24px 16px -24px; border-radius: 24px 24px 0 0;"></div>'
)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

