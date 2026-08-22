with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the 4 remaining broken alerts
html = html.replace("onclick=\"alert('Abriendo tutorial de Campañas Push...')\"", "onclick=\"document.getElementById('support-gemini-input').value = 'Cómo usar Campañas Push'; sendSupportGeminiMessage();\"")
html = html.replace("onclick=\"alert('Abriendo tutorial de 8 Programas...')\"", "onclick=\"document.getElementById('support-gemini-input').value = 'Explícame los 8 programas de lealtad'; sendSupportGeminiMessage();\"")
html = html.replace("onclick=\"alert('Abriendo tutorial de Citas y Stripe...')\"", "onclick=\"document.getElementById('support-gemini-input').value = 'Cómo cobro con Stripe y agendo citas'; sendSupportGeminiMessage();\"")
html = html.replace("onclick=\"alert('Abriendo tutorial de Súper Admin...')\"", "onclick=\"document.getElementById('support-gemini-input').value = 'Cómo atender clientes en el Inbox'; sendSupportGeminiMessage();\"")

import re
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
