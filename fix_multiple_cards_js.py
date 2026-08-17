import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update startDesignerFlow to initialize a unique campaign state
old_designer_flow = """window.startDesignerFlow = function(programType) {
    // They selected a program in tab-loyalty. Move to Step 2.
    showToast(`Paso 2: Diseñando tarjeta para ${programType}. Personaliza los colores.`, "success");"""

new_designer_flow = """window.startDesignerFlow = function(programType) {
    // Initialize a completely new design state tied to this specific program!
    state.currentCampaignId = 'prog_' + Date.now();
    state.restaurantName = programType;
    state.dynamicDesc = "Disfruta de este beneficio exclusivo.";
    
    // They selected a program in tab-loyalty. Move to Step 2.
    showToast(`Paso 2: Diseñando tarjeta para ${programType}. Se ha creado un diseño independiente.`, "success");"""

if old_designer_flow in js:
    js = js.replace(old_designer_flow, new_designer_flow)


# 2. Update updatePassRender to show visual stamps and the custom texts
# We need to find updatePassRender
old_update_pass = """function updatePassRender() {"""

# We'll inject visual stamps logic inside updatePassRender
# Actually, the simplest way is to append logic to updatePassRender if it exists
# Let's search where updatePassRender ends, or just redefine a hook.
# Wait, I can just replace the definition or hook into the end of it.
# Let's look for the end of updatePassRender or just use regex.

# We can find `document.getElementById('render-name').textContent = state.restaurantName;`
# and add our custom text updates.

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
