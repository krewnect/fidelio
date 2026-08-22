import re
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            window.supabaseClient.from('merchants').update({
                appointment_settings: newSettings
            }).eq('id', targetState.tenantId).then(({error}) => {
                if (error) console.error("Error saving schedules to DB", error);
                else {
                    if (typeof showToast === 'function') showToast('Horarios guardados en la nube', 'success');
                    const modal = document.getElementById('schedule-config-modal');
                    if (modal) modal.style.display = 'none';
                }
            });"""

replacement = """            window.supabaseClient.from('merchants').update({
                appointment_settings: newSettings
            }).eq('id', window.merchantData.id).select().then(({data, error}) => {
                if (error) {
                    alert("Error en la nube: " + error.message);
                } else if (!data || data.length === 0) {
                    alert("Error de permisos: No tienes autorización para modificar este negocio. Tu sesión puede haber expirado.");
                } else {
                    if (typeof showToast === 'function') showToast('Horarios guardados en la nube', 'success');
                    const modal = document.getElementById('schedule-config-modal');
                    if (modal) modal.style.display = 'none';
                }
            });"""

js = js.replace(target, replacement)
with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
