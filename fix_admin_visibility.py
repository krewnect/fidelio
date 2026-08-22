import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the professional-only logic
old_logic = """            document.querySelectorAll('.plan-professional-only').forEach(el => {
                if(isBusiness && plan !== 'professional') {
                    el.style.display = 'none'; // Solo ocultar si es 100% negocio y NO profesional
                } else {
                    el.style.display = ''; // Mostrar por defecto para professionals
                }
            });"""

new_logic = """            document.querySelectorAll('.plan-professional-only').forEach(el => {
                if(isAdmin) {
                    el.style.display = ''; // Admin ve TODO
                } else if(isBusiness && plan !== 'professional') {
                    el.style.display = 'none'; // Solo ocultar si es 100% negocio y NO profesional
                } else {
                    el.style.display = ''; // Mostrar por defecto para professionals
                }
            });"""

js = js.replace(old_logic, new_logic)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Admin visibility fixed.")
