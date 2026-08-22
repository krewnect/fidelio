import time
import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Inject window.onbeforeunload warning if there are unsaved changes
injection = """
window.addEventListener('beforeunload', function (e) {
    const builderActive = document.getElementById('tab-builder') && document.getElementById('tab-builder').classList.contains('active');
    if (builderActive) {
        e.preventDefault();
        e.returnValue = 'Tienes cambios sin guardar en tu campaña. ¿Seguro que quieres salir?';
    }
});
"""

if 'beforeunload' not in js:
    js += injection
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'src=\"dashboard_v2\.js\?v=\d+\"', 'src=\"dashboard_v2.js?v=' + str(int(time.time())) + '\"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
