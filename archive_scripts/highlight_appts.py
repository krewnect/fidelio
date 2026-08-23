import re
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            <div style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:16px; display:flex; flex-direction:column; gap:12px; box-shadow:0 2px 5px rgba(0,0,0,0.02); opacity: ${isProcessed ? '0.7' : '1'};">"""

replacement = """            <div style="background:${isProcessed ? '#ffffff' : '#fff1f2'}; border:2px solid ${isProcessed ? '#e5e7eb' : '#f43f5e'}; border-radius:12px; padding:16px; display:flex; flex-direction:column; gap:12px; box-shadow:0 4px 10px rgba(0,0,0,0.05); opacity: ${isProcessed ? '0.7' : '1'};">"""

js = js.replace(target, replacement)
with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
