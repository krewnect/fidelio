import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Emojis in the UI
html = html.replace('🤖', '')
html = html.replace('✨', '')
html = html.replace('⚡', '')
html = html.replace('🚀', '')
html = html.replace('🪄', '')
html = html.replace('🧠', '')
html = html.replace('💬', '')
html = html.replace('🔔', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('🤖', '')
js = js.replace('✨', '')
js = js.replace('⚡', '')
js = js.replace('🚀', '')
js = js.replace('🪄', '')
js = js.replace('🧠', '')
js = js.replace('💬', '')
js = js.replace('🔔', '')

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

