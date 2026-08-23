import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Put an alert inside saveDesignToSupabase to prove it is executing
old_func = """    window.saveDesignToSupabase = async function saveDesignToSupabase() {
        if (!window.supabaseClient || !state.tenantId) return;"""

new_func = """    window.saveDesignToSupabase = async function saveDesignToSupabase() {
        alert("Ejecutando saveDesignToSupabase. tenantId: " + state.tenantId);
        if (!window.supabaseClient || !state.tenantId) return;"""

js = js.replace(old_func, new_func)

with open('dashboard.js', 'w') as f:
    f.write(js)
