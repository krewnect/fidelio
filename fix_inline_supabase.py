import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Make the click listener async
old_listener_start = "document.body.addEventListener('click', (e) => {"
new_listener_start = "document.body.addEventListener('click', async (e) => {"
js = js.replace(old_listener_start, new_listener_start)

# Replace the window.saveDesignToSupabase call with direct inline update
old_call = "if (window.saveDesignToSupabase) window.saveDesignToSupabase();"
new_call = """try {
                if (window.supabaseClient && state.tenantId) {
                    const { error } = await window.supabaseClient
                        .from('merchants')
                        .update({ branches: state.branches })
                        .eq('id', state.tenantId);
                    if (!error) {
                        console.log("Sucursal guardada en la base de datos.");
                    } else {
                        alert("Error en DB: " + error.message);
                    }
                }
            } catch (ex) {
                alert("Crash inline DB: " + ex.message);
            }"""

js = js.replace(old_call, new_call)

with open('dashboard.js', 'w') as f:
    f.write(js)
