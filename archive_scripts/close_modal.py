import re
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """                else {
                    if (typeof showToast === 'function') showToast('Horarios guardados en la nube', 'success');
                }"""
replacement = """                else {
                    if (typeof showToast === 'function') showToast('Horarios guardados en la nube', 'success');
                    const modal = document.getElementById('schedule-config-modal');
                    if (modal) modal.style.display = 'none';
                }"""

js = js.replace(target, replacement)
with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
