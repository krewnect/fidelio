import re

with open('dashboard.js', 'r') as f:
    js = f.read()

old_call = """        const { error } = await window.supabaseClient
            .from('merchants')
            .update(updates)
            .eq('id', state.tenantId);
            
        if (!error) {
            showToast("Guardado automático en la nube ☁️", "success");
        } else {
            console.error("Supabase Save Error:", error);
            showToast("Error de conexión BD: " + (error.message || "Fallo desconocido"), "error");
        }"""

new_call = """        try {
            const { error } = await window.supabaseClient
                .from('merchants')
                .update(updates)
                .eq('id', state.tenantId);
                
            if (!error) {
                showToast("Guardado automático en la nube ☁️", "success");
            } else {
                console.error("Supabase Save Error:", error);
                alert("SUPABASE DENEGADO: " + error.message);
                showToast("Error BD: " + error.message, "error");
            }
        } catch (ex) {
            alert("SUPABASE CRASH: " + ex.message + "\\n" + ex.stack);
        }"""

js = js.replace(old_call, new_call)

with open('dashboard.js', 'w') as f:
    f.write(js)
