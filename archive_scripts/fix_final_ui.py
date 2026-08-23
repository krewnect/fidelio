import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix white stripe by making sure the builder wrapper stretches and body background matches
html = html.replace('body {', 'body {\n            background-color: #f9fafb !important;')
html = html.replace('#app-content {', '#app-content {\n            background-color: #f9fafb !important;')
html = html.replace('.builder-preview-container {', '.builder-preview-container {\n            background-color: #f9fafb !important;')

# 2. Fix the "amontonado" Citas y Pagos layout
target_grid_citas = '<div style="display:grid; gap:16px; margin-bottom:24px;">\n                                <div>\n                                    <label class="premium-label"><i class="fa-solid fa-calendar-check"'
replacement_grid_citas = '<div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:16px; margin-bottom:24px;">\n                                <div>\n                                    <label class="premium-label"><i class="fa-solid fa-calendar-check"'
html = html.replace(target_grid_citas, replacement_grid_citas)

# Same for Beneficios Visibles
target_grid_beneficios = '<div style="display:grid; gap:16px; margin-bottom:24px;">\n                                <div>\n                                    <label class="premium-label">Total de sellos (Meta)</label>'
replacement_grid_beneficios = '<div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:16px; margin-bottom:24px;">\n                                <div>\n                                    <label class="premium-label">Total de sellos (Meta)</label>'
html = html.replace(target_grid_beneficios, replacement_grid_beneficios)

# 3. Add default values to Inputs so they don't say "Restaurante" all the time
# I will change "Restaurante & Gastronomía" to "Mi Negocio / Especialidad" in the HTML input
html = html.replace('value="Restaurante & Gastronomía"', 'value="Mi Negocio / Especialidad"')

# In JS, update `dashboard_v2.js` to change the default as well
with open('dashboard_v2.js', 'r', encoding='utf-8') as jsf:
    js = jsf.read()

js = js.replace('let pCat = "Restaurante & Gastronomía";', 'let pCat = "Mi Negocio / Especialidad";')

with open('dashboard_v2.js', 'w', encoding='utf-8') as jsf:
    jsf.write(js)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
