import re
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        try {
            if (merchantData.appointment_settings && merchantData.appointment_settings.schedules) {
                window.scheduleData = merchantData.appointment_settings.schedules;
            }
        } catch(e) { console.error("Error restoring schedules:", e); }"""

replacement = """        try {
            if (merchantData.appointment_settings && merchantData.appointment_settings.schedules) {
                window.scheduleData = merchantData.appointment_settings.schedules;
            }
            if (typeof state !== 'undefined') state.schedules = window.scheduleData;
            if (window.state) window.state.schedules = window.scheduleData;
        } catch(e) { console.error("Error restoring schedules:", e); }"""

js = js.replace(target, replacement)
with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
