import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace saveComplexSchedule with a bulletproof try-catch version that uses window.state directly
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
    state.schedules = JSON.parse(JSON.stringify(window.scheduleData)); // Deep copy
    console.log("Horarios guardados en estado:", state.schedules);
    
    // Update UI Summary
    window.renderScheduleSummary();
    
    document.getElementById('schedule-config-modal').style.display='none';
    if(typeof showToast === 'function') showToast("Franjas horarias configuradas y guardadas exitosamente", "success");
};"""

new_save = """window.saveComplexSchedule = function() {
    try {
        console.log("Saving complex schedule...");
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
        
        // Ensure state exists
        if (typeof state === 'undefined') window.state = {};
        
        // Save to state (safely referencing global state)
        const targetState = typeof state !== 'undefined' ? state : window.state;
        targetState.schedules = JSON.parse(JSON.stringify(window.scheduleData));
        console.log("Horarios guardados en estado:", targetState.schedules);
        
        // Update UI Summary safely
        try {
            window.renderScheduleSummary();
        } catch (sumErr) {
            console.error("Error in renderScheduleSummary:", sumErr);
            alert("Error rendering summary: " + sumErr.message);
        }
        
        const modal = document.getElementById('schedule-config-modal');
        if (modal) {
            modal.style.display = 'none';
        } else {
            console.error("Modal element not found to close it!");
        }
        
        if(typeof showToast === 'function') {
            showToast("Franjas horarias guardadas exitosamente", "success");
        } else {
            alert("Franjas horarias guardadas exitosamente");
        }
    } catch (err) {
        console.error("CRASH in saveComplexSchedule:", err);
        alert("CRASH AL GUARDAR HORARIOS: " + err.message);
    }
};"""

js = js.replace(old_save, new_save)


old_summary = """window.renderScheduleSummary = function() {
    const container = document.getElementById('schedule-summary-container');
    const content = document.getElementById('schedule-summary-content');
    if(!container || !content) return;
    
    if(!state.schedules || Object.keys(state.schedules).length === 0) {
        container.style.display = 'none';
        return;
    }
"""

new_summary = """window.renderScheduleSummary = function() {
    const container = document.getElementById('schedule-summary-container');
    const content = document.getElementById('schedule-summary-content');
    if(!container || !content) {
        console.warn("Summary container or content div not found in DOM");
        return;
    }
    
    const targetState = typeof state !== 'undefined' ? state : window.state;
    if(!targetState || !targetState.schedules || Object.keys(targetState.schedules).length === 0) {
        container.style.display = 'none';
        return;
    }
"""
js = js.replace(old_summary, new_summary)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Dashboard JS try-catch wrapped.")
