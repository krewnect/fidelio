import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Make updatePassRender globally available
patch = """    function updatePassRender() {
        window._updatePassRenderGlobal = true; // Debug flag"""
js = js.replace('function updatePassRender() {', patch)

# Add window binding at the end of the IIFE
patch2 = """
    window.updatePassRender = updatePassRender;
    safeAdd('program-type-select', 'change', updatePassRender);"""
js = js.replace("safeAdd('program-type-select', 'change', updatePassRender);", patch2)

with open('dashboard.js', 'w') as f:
    f.write(js)

with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('<select id="program-type-select" class="premium-input" style="font-weight:600;">',
                    '<select id="program-type-select" class="premium-input" style="font-weight:600;" onchange="if(window.updatePassRender) window.updatePassRender();">')
html = html.replace('<input type="number" id="stamps-total" class="premium-input" value="5" min="3" max="10">',
                    '<input type="number" id="stamps-total" class="premium-input" value="5" min="3" max="10" oninput="if(window.updatePassRender) window.updatePassRender();">')

with open('index.html', 'w') as f:
    f.write(html)
