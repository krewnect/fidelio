import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make the inputs have white background, black text, strong grey border
js = js.replace(
    'background:#1f2937; border:1px solid rgba(255,255,255,0.2); width:130px; color:var(--text-main);',
    'background:#ffffff; border:1px solid #d1d5db; width:130px; color:#000000;'
)

# Make the day container separators more visible but clean, black text for day names
js = js.replace(
    'border-bottom:1px solid rgba(255,255,255,0.05); background: ${shifts.length === 0 ? \'rgba(255,255,255,0.02)\' : \'transparent\'};',
    'border-bottom:1px solid #e5e7eb; background: ${shifts.length === 0 ? \'#f9fafb\' : \'#ffffff\'};'
)
js = js.replace(
    '<h3 style="margin:0 0 6px 0; font-size:15px; font-weight:700; color:var(--text-main);">${day}</h3>',
    '<h3 style="margin:0 0 6px 0; font-size:15px; font-weight:700; color:#000000;">${day}</h3>'
)
js = js.replace(
    '<span style="color:var(--text-muted); font-size:13px; font-weight:600;">a</span>',
    '<span style="color:#4b5563; font-size:13px; font-weight:700;">a</span>'
)
js = js.replace(
    '<div style="font-size:14px; color:var(--text-muted); padding:10px 0; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-moon"></i> Cerrado</div>',
    '<div style="font-size:14px; color:#6b7280; padding:10px 0; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-moon"></i> Cerrado</div>'
)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Dashboard JS white theme fixed.")


with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make modal background pure white
html = html.replace(
    '''<div class="modal-content" style="background:#111827; width:95%; max-width:600px; max-height:85vh; border-radius:20px; border:1px solid rgba(255,255,255,0.1); padding:0; position:relative; box-shadow:0 25px 50px rgba(0,0,0,0.5); display:flex; flex-direction:column; overflow:hidden;">''',
    '''<div class="modal-content" style="background:#ffffff; width:95%; max-width:600px; max-height:85vh; border-radius:20px; border:1px solid #e5e7eb; padding:0; position:relative; box-shadow:0 25px 50px rgba(0,0,0,0.3); display:flex; flex-direction:column; overflow:hidden;">'''
)

# Header background and text
html = html.replace(
    '''<div style="padding:24px 32px; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.03);">
                <div>
                    <h2 style="font-size:20px; margin-bottom:4px; color:var(--text-main);"><i class="fa-solid fa-clock" style="color:var(--accent-violet); margin-right:8px;"></i> Horarios Múltiples</h2>
                    <p style="color:var(--text-muted); font-size:13px; margin:0;">Define múltiples franjas horarias (turnos) para cada día.</p>
                </div>
                <button onclick="document.getElementById('schedule-config-modal').style.display='none'" style="background:var(--bg-input); border:none; width:36px; height:36px; border-radius:50%; font-size:18px; color:var(--text-muted); cursor:pointer; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-times"></i></button>
            </div>''',
    '''<div style="padding:24px 32px; border-bottom:1px solid #e5e7eb; display:flex; justify-content:space-between; align-items:center; background:#ffffff;">
                <div>
                    <h2 style="font-size:20px; margin-bottom:4px; color:#000000;"><i class="fa-solid fa-clock" style="color:#8b5cf6; margin-right:8px;"></i> Horarios Múltiples</h2>
                    <p style="color:#4b5563; font-size:13px; margin:0;">Define múltiples franjas horarias (turnos) para cada día.</p>
                </div>
                <button onclick="document.getElementById('schedule-config-modal').style.display='none'" style="background:#f3f4f6; border:none; width:36px; height:36px; border-radius:50%; font-size:18px; color:#4b5563; cursor:pointer; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-times"></i></button>
            </div>'''
)

# Footer background
html = html.replace(
    '''<div style="padding:24px 32px; border-top:1px solid rgba(255,255,255,0.05); background:#111827;">''',
    '''<div style="padding:24px 32px; border-top:1px solid #e5e7eb; background:#ffffff;">'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Index HTML white theme fixed.")
