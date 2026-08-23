import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            appointments: appointmentsData || [],
            activeWallet: "apple"
        };"""

replacement = """            appointments: appointmentsData || [],
            activeWallet: "apple"
        };
        
        // Restore schedules from DB
        try {
            if (merchantData.appointment_settings && merchantData.appointment_settings.schedules) {
                window.scheduleData = merchantData.appointment_settings.schedules;
            }
        } catch(e) { console.error("Error restoring schedules:", e); }"""

if target in js:
    js = js.replace(target, replacement)
else:
    print("WARNING: Could not find target in dashboard.js")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
