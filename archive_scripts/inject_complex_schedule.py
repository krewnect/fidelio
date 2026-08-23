import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace old modal with complex one
# Wait, let's find the exact old modal block.
# I will use regex to find `<div class="modal-overlay" id="schedule-config-modal".*?</div>\s*</div>`
old_modal_pattern = re.compile(r'<div class="modal-overlay" id="schedule-config-modal".*?</button>\s*</div>\s*</div>', re.DOTALL)

complex_modal = """
    <!-- COMPLEX SCHEDULE CONFIG MODAL -->
    <div class="modal-overlay" id="schedule-config-modal" style="display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.6); z-index:9999; align-items:center; justify-content:center; backdrop-filter:blur(8px);">
        <div class="modal-content" style="background:var(--surface); width:95%; max-width:600px; max-height:85vh; border-radius:20px; padding:0; position:relative; box-shadow:0 25px 50px rgba(0,0,0,0.3); display:flex; flex-direction:column; overflow:hidden;">
            
            <div style="padding:24px 32px; border-bottom:1px solid var(--border-soft); display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.02);">
                <div>
                    <h2 style="font-size:20px; margin-bottom:4px; color:var(--text-main);"><i class="fa-solid fa-clock" style="color:var(--accent-violet); margin-right:8px;"></i> Horarios Múltiples</h2>
                    <p style="color:var(--text-muted); font-size:13px; margin:0;">Define múltiples franjas horarias (turnos) para cada día.</p>
                </div>
                <button onclick="document.getElementById('schedule-config-modal').style.display='none'" style="background:var(--bg-input); border:none; width:36px; height:36px; border-radius:50%; font-size:18px; color:var(--text-muted); cursor:pointer; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-times"></i></button>
            </div>
            
            <div id="schedule-days-container" style="padding:24px 32px; overflow-y:auto; flex:1; display:flex; flex-direction:column; gap:20px;">
                <!-- JS will populate this with days -->
            </div>
            
            <div style="padding:24px 32px; border-top:1px solid var(--border-soft); background:var(--bg-color);">
                <button class="btn btn-primary" onclick="saveComplexSchedule()" style="width:100%; justify-content:center; background:linear-gradient(135deg, #8b5cf6, #6366f1) !important; color:#fff; border:none; padding:16px; font-size:16px; font-weight:700; border-radius:12px; box-shadow:0 4px 14px rgba(139,92,246,0.4);"><i class="fa-solid fa-floppy-disk"></i> Guardar Franjas Horarias</button>
            </div>
        </div>
    </div>
"""

if old_modal_pattern.search(html):
    html = old_modal_pattern.sub(complex_modal, html)
    print("Complex modal injected via regex.")
else:
    # If not found, inject before </body>
    html = html.replace('</body>', complex_modal + '\n</body>')
    print("Complex modal appended.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# JS logic for complex schedule
js_logic = """
// --- COMPLEX SCHEDULE LOGIC ---
window.scheduleData = {
    'Lunes': [{start: '09:00', end: '18:00'}],
    'Martes': [{start: '09:00', end: '18:00'}],
    'Miércoles': [{start: '09:00', end: '18:00'}],
    'Jueves': [{start: '09:00', end: '18:00'}],
    'Viernes': [{start: '09:00', end: '18:00'}],
    'Sábado': [{start: '10:00', end: '14:00'}],
    'Domingo': []
};

window.renderScheduleDays = function() {
    const container = document.getElementById('schedule-days-container');
    if (!container) return;
    
    container.innerHTML = '';
    const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    
    days.forEach(day => {
        const shifts = window.scheduleData[day] || [];
        
        let shiftsHtml = '';
        if (shifts.length === 0) {
            shiftsHtml = `<div style="font-size:13px; color:var(--accent-amber); padding:8px 0;"><i class="fa-solid fa-moon"></i> Cerrado</div>`;
        } else {
            shifts.forEach((shift, index) => {
                shiftsHtml += `
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                        <input type="time" class="premium-input schedule-time-input" data-day="${day}" data-index="${index}" data-type="start" value="${shift.start}" style="padding:8px; font-size:13px; width:110px;">
                        <span style="color:var(--text-muted); font-size:12px;">a</span>
                        <input type="time" class="premium-input schedule-time-input" data-day="${day}" data-index="${index}" data-type="end" value="${shift.end}" style="padding:8px; font-size:13px; width:110px;">
                        <button onclick="removeShift('${day}', ${index})" style="background:rgba(239,68,68,0.1); border:none; color:#ef4444; width:32px; height:32px; border-radius:8px; cursor:pointer;"><i class="fa-solid fa-trash-can"></i></button>
                    </div>
                `;
            });
        }
        
        const dayHtml = `
            <div style="background:rgba(255,255,255,0.02); border:1px solid var(--border-soft); border-radius:12px; padding:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <h3 style="margin:0; font-size:15px; font-weight:700;">${day}</h3>
                    <button onclick="addShift('${day}')" style="background:none; border:none; color:var(--accent-violet); font-size:13px; font-weight:700; cursor:pointer;"><i class="fa-solid fa-plus"></i> Añadir Turno</button>
                </div>
                <div>${shiftsHtml}</div>
            </div>
        `;
        container.innerHTML += dayHtml;
    });
};

window.addShift = function(day) {
    if(!window.scheduleData[day]) window.scheduleData[day] = [];
    window.scheduleData[day].push({start: '10:00', end: '14:00'});
    window.renderScheduleDays();
};

window.removeShift = function(day, index) {
    if(window.scheduleData[day]) {
        window.scheduleData[day].splice(index, 1);
        window.renderScheduleDays();
    }
};

window.saveComplexSchedule = function() {
    // Collect data from DOM to memory just before saving
    const inputs = document.querySelectorAll('.schedule-time-input');
    inputs.forEach(input => {
        const d = input.getAttribute('data-day');
        const idx = parseInt(input.getAttribute('data-index'));
        const t = input.getAttribute('data-type');
        if(window.scheduleData[d] && window.scheduleData[d][idx]) {
            window.scheduleData[d][idx][t] = input.value;
        }
    });
    
    // Save to state
    state.schedules = window.scheduleData;
    console.log("Horarios guardados en estado:", state.schedules);
    
    document.getElementById('schedule-config-modal').style.display='none';
    if(typeof showToast === 'function') showToast("Franjas horarias configuradas y guardadas exitosamente", "success");
};

// Hook rendering into modal open
document.addEventListener('DOMContentLoaded', () => {
    // Intercept clicks on any element that opens schedule modal
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('button');
        if (btn && btn.getAttribute('onclick') && btn.getAttribute('onclick').includes('schedule-config-modal')) {
            if (btn.getAttribute('onclick').includes('flex') || btn.getAttribute('onclick').includes('block')) {
                // If it's opening the modal
                setTimeout(window.renderScheduleDays, 50);
            }
        }
    });
});
"""
js += js_logic

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Complex schedule JS logic injected.")

