import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the dynamic bridge loading
old_dynamic = """                const bridge = document.createElement('script');
                bridge.src = 'magic_bridge.js';
                document.body.appendChild(bridge);"""

if old_dynamic in html:
    html = html.replace(old_dynamic, "")
    print("Removed dynamic bridge")
else:
    print("Could not find dynamic bridge")

# Insert magic_bridge.js statically in the head or right before the closing body
# We already have a block at the bottom for HANDLERS.
static_injection = """
    <script src="magic_bridge.js"></script>
    <!-- MAGIC ENGINE TEST HANDLERS -->"""

html = html.replace("<!-- MAGIC ENGINE TEST HANDLERS -->", static_injection)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
