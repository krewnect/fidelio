import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Make removeBranch async
js = js.replace(
    "window.removeBranch = function(id) {",
    "window.removeBranch = async function(id) {"
)

new_inline = """try {
                if (window.supabaseClient && state.tenantId) {
                    const { error } = await window.supabaseClient
                        .from('merchants')
                        .update({ branches: state.branches })
                        .eq('id', state.tenantId);
                    if (error) alert("Error en DB: " + error.message);
                }
            } catch (ex) {
                alert("Crash inline DB: " + ex.message);
            }"""

js = js.replace(
    "if (window.saveDesignToSupabase) window.saveDesignToSupabase();",
    new_inline
)

with open('dashboard.js', 'w') as f:
    f.write(js)
