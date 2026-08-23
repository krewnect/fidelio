import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

logo_ui = """
                            <div class="apple-input-group">
                                <label class="apple-label">Logotipo de la Tarjeta (Reemplaza al ícono)</label>
                                <div style="display:flex; align-items:center; gap:16px;">
                                    <div style="flex:1; border: 2px dashed #cbd5e1; background:#f8fafc; border-radius:12px; padding:20px; text-align:center; cursor:pointer; transition:all 0.2s;" onmouseover="this.style.borderColor='#8b5cf6'" onmouseout="this.style.borderColor='#cbd5e1'" onclick="document.getElementById('logo-file-input').click()">
                                        <input type="file" id="logo-file-input" accept="image/png, image/jpeg" style="display:none;">
                                        <i class="fa-solid fa-cloud-arrow-up" style="color:#94a3b8; font-size:20px; margin-bottom:8px;"></i>
                                        <div style="font-size:13px; color:#64748b; font-weight:600;">Subir logo cuadrado (Opcional)</div>
                                    </div>
                                    <button id="btn-remove-logo" style="display:none; background:#fee2e2; color:#ef4444; border:none; padding:12px; border-radius:12px; font-weight:700; cursor:pointer;">Quitar</button>
                                </div>
                            </div>
"""

target = r'<div class="apple-input-group">\s*<label class="apple-label">Banner Wallet \(Opcional\)</label>'
html = re.sub(target, logo_ui + '\n                            <div class="apple-input-group">\n                                <label class="apple-label">Banner Wallet (Opcional)</label>', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
