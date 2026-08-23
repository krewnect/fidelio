import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_code = """                const script = document.createElement('script');
                script.src = 'dashboard_v3.js?v=9999';
                document.body.appendChild(script);"""

new_code = """                const bridge = document.createElement('script');
                bridge.src = 'magic_bridge.js';
                document.body.appendChild(bridge);

                const script = document.createElement('script');
                script.src = 'dashboard_v3.js?v=' + new Date().getTime();
                document.body.appendChild(script);"""

if old_code in html:
    html = html.replace(old_code, new_code)
    print("Patched script loader")
else:
    print("WARNING: Could not find old_code")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
