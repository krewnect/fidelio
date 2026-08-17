import os
import re

files_to_update = [
    'index.html',
    'scanner.html',
    'dashboard.js',
    'merchant-public.html'
]

replacements = [
    (r'Monedero Digital', 'Saldo Digital'),
    (r'Monedero Virtual', 'Saldo Digital'),
    (r'Monedero Electrónico', 'Saldo Digital'),
    (r'Monedero de Prepago', 'Saldo de Recargas'),
    (r'Monedero Prepago', 'Saldo de Recargas'),
    (r'monedero pre-pagado', 'saldo de recargas'),
    (r'Monedero pre-pagado', 'Saldo de recargas'),
    (r'monederos', 'saldos digitales'),
    (r'Monederos', 'Saldos Digitales'),
    (r'Monedero', 'Saldo Digital'),
    (r'monedero', 'saldo digital')
]

for file_name in files_to_update:
    filepath = os.path.join('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app', file_name)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for old, new in replacements:
            content = re.sub(old, new, content)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_name}")

print("Done")
