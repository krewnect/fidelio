import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${c.name.charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${c.name}</strong>"""

replacement = """                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${(c.full_name || c.name || '?').charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${c.full_name || c.name || 'Cliente sin nombre'}</strong>"""

text = text.replace(target, replacement)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(text)
