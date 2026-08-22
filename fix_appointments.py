import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add deleteAppointment function
delete_fn = """
window.deleteAppointment = async function(id) {
    if(!confirm('¿Estás seguro de que deseas eliminar esta cita?')) return;
    try {
        const { error } = await window.supabaseClient.from('transactions').delete().eq('id', id);
        if (error) throw error;
        if (typeof window.showToast === 'function') window.showToast('Cita eliminada', 'success');
        if (state && state.transactions) {
            state.transactions = state.transactions.filter(t => t.id !== id);
        }
        window.loadAppointments();
    } catch(err) {
        console.error(err);
        if (typeof window.showToast === 'function') window.showToast('Error al eliminar', 'error');
    }
};
"""

if "window.deleteAppointment =" not in js:
    # insert before window.loadAppointments
    js = js.replace('window.loadAppointments = function() {', delete_fn + '\nwindow.loadAppointments = function() {')

# Modify loadAppointments to filter out past appointments and add the delete button
old_logic = """    const appts = state.transactions
        .filter(t => t.transaction_type === 'appointment_request')
        .sort((a,b) => new Date(b.created_at) - new Date(a.created_at));"""

new_logic = """    const now = new Date();
    const appts = state.transactions
        .filter(t => {
            if (t.transaction_type !== 'appointment_request') return false;
            let details = {};
            try { details = JSON.parse(t.notes || "{}"); } catch(e){}
            if (details.date && details.time) {
                const apptDate = new Date(`${details.date}T${details.time}:00`);
                if (apptDate < now) {
                    // Auto-delete logically passed appointments by hiding them
                    return false;
                }
            }
            return true;
        })
        .sort((a,b) => new Date(b.created_at) - new Date(a.created_at));"""

js = js.replace(old_logic, new_logic)

old_btn_logic = """                    ${phone 
                        ? `<button onclick="markAppointmentProcessed('${t.id}', '${waLink}')" style="cursor:pointer; border:none; flex:1; text-align:center; background:#10b981; color:white; padding:10px; border-radius:8px; font-weight:600; font-size:14px;"><i class="fa-brands fa-whatsapp"></i> Confirmar y Cobrar</button>` 
                        : `<span style="flex:1; text-align:center; background:#f3f4f6; color:#9ca3af; padding:10px; border-radius:8px; font-size:14px;"><i class="fa-solid fa-phone-slash"></i> Sin teléfono</span>`}"""

new_btn_logic = """                    ${phone 
                        ? `<button onclick="markAppointmentProcessed('${t.id}', '${waLink}')" style="cursor:pointer; border:none; flex:1; text-align:center; background:#10b981; color:white; padding:10px; border-radius:8px; font-weight:600; font-size:14px;"><i class="fa-brands fa-whatsapp"></i> Confirmar y Cobrar</button>` 
                        : `<span style="flex:1; text-align:center; background:#f3f4f6; color:#9ca3af; padding:10px; border-radius:8px; font-size:14px;"><i class="fa-solid fa-phone-slash"></i> Sin teléfono</span>`}
                    <button onclick="deleteAppointment('${t.id}')" style="cursor:pointer; border:none; background:#fee2e2; color:#ef4444; padding:10px 16px; border-radius:8px; font-weight:600; font-size:14px; transition:all 0.2s;"><i class="fa-solid fa-trash"></i></button>"""

js = js.replace(old_btn_logic, new_btn_logic)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Appointments fixed.")
