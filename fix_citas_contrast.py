import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make the inputs have high contrast dark backgrounds with clear white borders
js = js.replace(
    'background:var(--surface-light); border:1px solid var(--border-soft);',
    'background:#1f2937; border:1px solid rgba(255,255,255,0.2);'
)

# Make the day container separators more visible but clean
js = js.replace(
    'border-bottom:1px solid var(--border-soft); background: ${shifts.length === 0 ? \'rgba(0,0,0,0.02)\' : \'transparent\'};',
    'border-bottom:1px solid rgba(255,255,255,0.05); background: ${shifts.length === 0 ? \'rgba(255,255,255,0.02)\' : \'transparent\'};'
)

# We also need to fix the modal container itself. It's in index.html
with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Dashboard JS colors fixed.")


with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace(
    '''<div class="modal-content" style="background:var(--surface); width:95%; max-width:600px; max-height:85vh; border-radius:20px; padding:0; position:relative; box-shadow:0 25px 50px rgba(0,0,0,0.3); display:flex; flex-direction:column; overflow:hidden;">''',
    '''<div class="modal-content" style="background:#111827; width:95%; max-width:600px; max-height:85vh; border-radius:20px; border:1px solid rgba(255,255,255,0.1); padding:0; position:relative; box-shadow:0 25px 50px rgba(0,0,0,0.5); display:flex; flex-direction:column; overflow:hidden;">'''
)

html = html.replace(
    '''<div style="padding:24px 32px; border-bottom:1px solid var(--border-soft); display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.02);">''',
    '''<div style="padding:24px 32px; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.03);">'''
)

html = html.replace(
    '''<div style="padding:24px 32px; border-top:1px solid var(--border-soft); background:var(--bg-color);">''',
    '''<div style="padding:24px 32px; border-top:1px solid rgba(255,255,255,0.05); background:#111827;">'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Index HTML colors fixed.")
