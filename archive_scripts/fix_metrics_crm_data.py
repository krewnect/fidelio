import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Strip out everything inside `<div style="flex:1; display:flex; flex-direction:column; gap:12px;">` up to the `Ver CRM Completo` button.
html = re.sub(
    r'<div style="flex:1; display:flex; flex-direction:column; gap:12px;">.*?<button class="btn btn-primary" style="width:100%; margin-top:16px; font-size:13px;">Ver CRM Completo</button>',
    '<div style="flex:1; display:flex; flex-direction:column; gap:12px; justify-content:center; align-items:center; color:var(--text-muted); font-size:14px;"><p>Aún no hay clientes top este mes.</p></div>\n<button class="btn btn-primary" style="width:100%; margin-top:16px; font-size:13px;">Ver CRM Completo</button>',
    html,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Métricas CRM data cleaned.")
