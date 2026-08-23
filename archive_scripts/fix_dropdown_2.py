import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = r'<label class="premium-label" style="color:var\(--accent-violet\);">Campaña de Fidelización Asociada</label>.*?<p style="font-size:12px; color:var\(--text-muted\); margin-top:4px;">Asocia este diseño a un programa específico\. El diseño será único para la campaña seleccionada\.</p>\s*</div>'
html = re.sub(target, '', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
