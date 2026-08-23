// Simulate the JS logic
const merchantData = {
    id: '6ebd41a1-d0e3-4547-8ffd-930b07623c76',
    appointment_settings: {
        schedules: {
            "Lunes": [{"start":"09:00","end":"18:00"}]
        }
    }
};

let scheduleData = merchantData.appointment_settings.schedules;
let state = { tenantId: merchantData.id };

scheduleData["Lunes"][0].start = "11:00"; // simulated input

const targetState = state;
targetState.schedules = JSON.parse(JSON.stringify(scheduleData));

let processed = merchantData.appointment_settings.processed_appointments || [];
const newSettings = {
    schedules: targetState.schedules,
    landing_prefs: {},
    processed_appointments: processed
};

merchantData.appointment_settings = newSettings;

console.log(JSON.stringify(newSettings, null, 2));
