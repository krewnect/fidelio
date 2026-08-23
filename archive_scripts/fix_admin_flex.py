import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_logic = """            document.querySelectorAll('.plan-business-only').forEach(el => {
                if(isBusiness) {
                    el.style.display = 'flex';
                } else {
                    el.style.display = 'none';
                }
            });"""

new_logic = """            document.querySelectorAll('.plan-business-only').forEach(el => {
                if(isBusiness) {
                    el.style.display = '';
                } else {
                    el.style.display = 'none';
                }
            });"""

js = js.replace(old_logic, new_logic)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Business tabs flex fixed.")
