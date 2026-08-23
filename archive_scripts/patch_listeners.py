import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Make sure we have both 'change' and 'input'
listener_patch = """
    safeAdd('program-type-select', 'change', updatePassRender);
    safeAdd('program-type-select', 'input', updatePassRender);
    safeAdd('stamps-total', 'input', updatePassRender);
    safeAdd('stamps-total', 'change', updatePassRender);"""

js = js.replace("safeAdd('program-type-select', 'change', updatePassRender);", "")
js = js.replace("safeAdd('stamps-total', 'input', updatePassRender);", "")

# Add them back before // --- UPLOAD HANDLERS ---
js = js.replace('// --- UPLOAD HANDLERS ---', listener_patch + '\n    // --- UPLOAD HANDLERS ---')

with open('dashboard.js', 'w') as f:
    f.write(js)
