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
    print("Injected startDesignerFlow correctly.")

# Let's find updatePassRender
old_render_logic = """    const renderName = document.getElementById('render-name');
    if (renderName) renderName.textContent = state.restaurantName || "Mi Negocio";"""

new_render_logic = """    const renderName = document.getElementById('render-name');
    if (renderName) renderName.textContent = state.restaurantName || "Mi Negocio";
    
    // VISUAL STAMPS INJECTION
    const stampsView = document.getElementById('render-stamps-view');
    const stampsGrid = document.getElementById('render-stamps-grid');
    if (state.activeMode === 'stampCard' && stampsView && stampsGrid) {
        stampsView.style.display = 'flex';
        let total = parseInt(state.stampsTotal) || 10;
        let html = '';
        for(let i=0; i<total; i++) {
            if(i < 3) {
                html += `<i class="fa-solid fa-circle-check" style="color:var(--accent-violet); font-size:18px;"></i>`;
            } else {
                html += `<i class="fa-solid fa-circle-dot" style="color:#d1d5db; font-size:18px;"></i>`;
            }
        }
        stampsGrid.innerHTML = html;
    } else if (stampsView) {
        stampsView.style.display = 'none';
    }

    // CASHBACK INJECTION
    const renderRewardText = document.getElementById('render-reward-text');
    if (state.activeMode === 'storeCard' && renderRewardText) {
        renderRewardText.textContent = state.cashbackPercent ? `Te devolvemos el ${state.cashbackPercent}% en saldo` : 'Acumula saldo en tus compras';
    } else if (renderRewardText) {
        renderRewardText.textContent = state.stampsReward || 'Bebida de Cortesía Gratis';
    }
"""

if old_render_logic in js:
    js = js.replace(old_render_logic, new_render_logic)
    print("Injected visual render updates correctly.")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

