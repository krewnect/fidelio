import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; margin-left:4px;" title="Escanear QR" onclick="window.showCustomerQR('${c.id}', '${c.name.replace(/'/g, "\\\\'")}')">"""

replacement = """                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; margin-left:4px;" title="Escanear QR" onclick="window.showCustomerQR('${c.id}', '${(c.full_name || c.name || 'Cliente').replace(/'/g, "\\\\'")}')">"""

text = text.replace(target, replacement)

target2 = """                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:var(--accent-violet); border-color:rgba(139, 92, 246, 0.2);" title="Enviar Push a Apple/Google Wallet" onclick="alert('Redactando Notificación Push para ${c.name}')">"""

replacement2 = """                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:var(--accent-violet); border-color:rgba(139, 92, 246, 0.2);" title="Enviar Push a Apple/Google Wallet" onclick="alert('Redactando Notificación Push para ${(c.full_name || c.name || 'Cliente').replace(/'/g, "\\\\'")}')">"""

text = text.replace(target2, replacement2)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(text)
