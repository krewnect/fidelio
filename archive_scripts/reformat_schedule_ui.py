import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the renderScheduleDays block entirely
old_block_pattern = re.compile(r'window\.renderScheduleDays = function\(\)\s*\{.*?(?=\};)\};', re.DOTALL)

new_block = """window.renderScheduleDays = function() {
    // REFORMATTED CLEAN LAYOUT
    const container = document.getElementById('schedule-days-container');
    if (!container) return;
    
    // Solo renderizar si el modal está visible para evitar bugs (aunque ya lo llamamos en el onclick del botón)
    container.innerHTML = '';
    const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    
    // Estilos globales de borde para no duplicar CSS
    container.style.padding = '0';
    container.style.gap = '0';
    
    days.forEach(day => {
        const shifts = window.scheduleData[day] || [];
        
        let shiftsHtml = '';
        if (shifts.length === 0) {
            shiftsHtml = `<div style="font-size:14px; color:var(--text-muted); padding:10px 0; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-moon"></i> Cerrado</div>`;
        } else {
            shifts.forEach((shift, index) => {
                shiftsHtml += `
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom: ${index === shifts.length - 1 ? '0' : '12px'};">
                        <input type="time" class="premium-input schedule-time-input" data-day="${day}" data-index="${index}" data-type="start" value="${shift.start}" style="padding:10px 14px; font-size:14px; font-family:inherit; border-radius:10px; background:var(--surface-light); border:1px solid var(--border-soft); width:130px; color:var(--text-main);">
                        <span style="color:var(--text-muted); font-size:13px; font-weight:600;">a</span>
                        <input type="time" class="premium-input schedule-time-input" data-day="${day}" data-index="${index}" data-type="end" value="${shift.end}" style="padding:10px 14px; font-size:14px; font-family:inherit; border-radius:10px; background:var(--surface-light); border:1px solid var(--border-soft); width:130px; color:var(--text-main);">
                        <button onclick="removeShift('${day}', ${index})" style="background:none; border:none; color:#ef4444; width:36px; height:36px; border-radius:10px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:background 0.2s;" onmouseover="this.style.background='rgba(239,68,68,0.1)'" onmouseout="this.style.background='none'"><i class="fa-solid fa-xmark" style="font-size:18px;"></i></button>
                    </div>
                `;
            });
        }
        
        const dayHtml = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; padding:20px 32px; border-bottom:1px solid var(--border-soft); background: ${shifts.length === 0 ? 'rgba(0,0,0,0.02)' : 'transparent'}; transition: background 0.2s ease;">
                <div style="width:120px; padding-top:10px;">
                    <h3 style="margin:0 0 6px 0; font-size:15px; font-weight:700; color:var(--text-main);">${day}</h3>
                    <button onclick="addShift('${day}')" style="background:none; border:none; color:var(--accent-violet); font-size:12px; font-weight:600; cursor:pointer; padding:0; display:flex; align-items:center; gap:4px;"><i class="fa-solid fa-plus"></i> Añadir Turno</button>
                </div>
                <div style="flex:1; display:flex; flex-direction:column; align-items:flex-end;">
                    ${shiftsHtml}
                </div>
            </div>
        `;
        container.innerHTML += dayHtml;
    });
};"""

if old_block_pattern.search(js):
    js = old_block_pattern.sub(new_block, js)
    print("Schedule UI logic replaced.")
else:
    print("Could not find renderScheduleDays function.")

# Ensure scheduleData doesn't reset if it's already there (so we don't wipe out their data if we reload JS)
init_pattern = re.compile(r'window\.scheduleData\s*=\s*\{.*?\};', re.DOTALL)
new_init = """window.scheduleData = window.scheduleData || {
    'Lunes': [{start: '09:00', end: '18:00'}],
    'Martes': [{start: '09:00', end: '18:00'}],
    'Miércoles': [{start: '09:00', end: '18:00'}],
    'Jueves': [{start: '09:00', end: '18:00'}],
    'Viernes': [{start: '09:00', end: '18:00'}],
    'Sábado': [{start: '10:00', end: '14:00'}],
    'Domingo': []
};"""
js = init_pattern.sub(new_init, js)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
