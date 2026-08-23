import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add a container for the schedule summary in the Appointments tab
summary_html = """
                                <div id="schedule-summary-container" style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:20px; margin-bottom:24px; display:none;">
                                    <h3 style="margin:0 0 16px 0; font-size:15px; font-weight:700; color:#000000;"><i class="fa-solid fa-calendar-check" style="color:#10b981; margin-right:8px;"></i> Horario Configurado</h3>
                                    <div id="schedule-summary-content" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:12px;">
                                        <!-- JS will populate -->
                                    </div>
                                </div>
"""

# Inject it right before the appointments-list-container glass-card
if 'id="appointments-list-container"' in html and 'id="schedule-summary-container"' not in html:
    html = html.replace(
        '<div class="glass-card" style="padding: 24px;">\n                                    <div id="appointments-list-container"',
        summary_html + '\n                                <div class="glass-card" style="padding: 24px;">\n                                    <div id="appointments-list-container"'
    )
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Schedule summary container injected into index.html.")


with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update saveComplexSchedule to render the summary
old_save = """window.saveComplexSchedule = function() {
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
};"""

new_save = """window.renderScheduleSummary = function() {
    const container = document.getElementById('schedule-summary-container');
    const content = document.getElementById('schedule-summary-content');
    if(!container || !content) return;
    
    if(!state.schedules || Object.keys(state.schedules).length === 0) {
        container.style.display = 'none';
        return;
    }
    
    container.style.display = 'block';
    content.innerHTML = '';
    
    const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    let hasAnyShift = false;
    
    days.forEach(day => {
        const shifts = state.schedules[day] || [];
        if(shifts.length > 0) {
            hasAnyShift = true;
            let shiftsText = shifts.map(s => `<div style="background:#f3f4f6; padding:4px 8px; border-radius:6px; font-size:12px; font-weight:600; color:#374151;">${s.start} - ${s.end}</div>`).join('');
            content.innerHTML += `
                <div style="border:1px solid #e5e7eb; border-radius:8px; padding:12px;">
                    <div style="font-weight:700; font-size:13px; color:#111827; margin-bottom:8px;">${day}</div>
                    <div style="display:flex; flex-direction:column; gap:4px;">${shiftsText}</div>
                </div>
            `;
        }
    });
    
    if(!hasAnyShift) container.style.display = 'none';
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
    state.schedules = JSON.parse(JSON.stringify(window.scheduleData)); // Deep copy
    console.log("Horarios guardados en estado:", state.schedules);
    
    // Update UI Summary
    window.renderScheduleSummary();
    
    document.getElementById('schedule-config-modal').style.display='none';
    if(typeof showToast === 'function') showToast("Franjas horarias configuradas y guardadas exitosamente", "success");
};"""

if 'window.saveComplexSchedule = function()' in js:
    js = js.replace(old_save, new_save)
    with open('dashboard.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Dashboard JS summary logic injected.")

