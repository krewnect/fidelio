import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# FIX: STAMPS VISUAL BUG
# In updatePassRender, the logic creates `stamp-coin`. But wait, in `add_stamps_css.py` I created the css for `.stamp-coin`.
# However, `updatePassRender` has a bug where it doesn't correctly toggle the stamps view if the type is mapped wrong.
# Let's override `updatePassRender` toggle logic.
toggle_logic_old = """        if (pType === 'stamps') {
            if (qrView) qrView.style.display = 'none';
            if (stampsView) stampsView.style.display = 'flex';
            if (configStamps) configStamps.style.display = 'flex';"""

toggle_logic_new = """        if (pType === 'stamps') {
            if (qrView) qrView.style.display = 'none';
            if (stampsView) stampsView.style.display = 'flex';
            if (configStamps) configStamps.style.display = 'flex';
            
            // Force redraw of stamps just in case
            const stampsGrid = document.getElementById('render-stamps-grid');
            if (stampsGrid && !stampsGrid.innerHTML) {
                 stampsGrid.innerHTML = '';
                 for(let i=1; i<=10; i++) {
                     stampsGrid.innerHTML += `<div class="stamp-coin ${i<=3?'filled':'empty'}" style="background-color:${i<=3?cAcc:''};">${i>3?i:''}</div>`;
                 }
            }"""

if toggle_logic_old in js:
    js = js.replace(toggle_logic_old, toggle_logic_new)
    print("Stamps redraw logic injected.")

# FIX: REDUNDANCY (Hide redundant fields based on campaign selection)
redundancy_js = """
// Listener para ocultar redundancias si se selecciona una campaña
document.addEventListener('DOMContentLoaded', () => {
    const campSel = document.getElementById('builder-campaign-select');
    if(campSel) {
        campSel.addEventListener('change', (e) => {
            const isCamp = !!e.target.value;
            // Campos redundantes: Mensaje Corto (Promo) y Premio a Desbloquear
            const msgInput = document.getElementById('rest-desc');
            const rewardInput = document.getElementById('stamps-reward');
            
            if(msgInput && msgInput.parentElement) msgInput.parentElement.style.display = isCamp ? 'none' : 'block';
            if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = isCamp ? 'none' : 'block';
        });
    }
});
"""
js += redundancy_js

# FIX: SAVE DESIGN LOGIC
# Currently `saveDesign` saves everything flat to `state.xxx`.
# We need it to save to `state.campaigns` if `state.currentCampaignId` is set.
# I will override `saveDesign` globally.
old_save_design = """window.saveDesign = async function() {"""

new_save_design = """
window._origSaveDesign = window.saveDesign || async function(){};
window.saveDesign = async function() {
    // Collect data
    const pType = document.getElementById('program-type-select')?.value || 'cashback';
    const cPri = document.getElementById('color-primary')?.value || '#1e1b4b';
    const cAcc = document.getElementById('color-accent')?.value || '#8b5cf6';
    const cIcon = document.getElementById('rest-icon')?.value || 'fa-crown';
    const sTotal = document.getElementById('stamps-total')?.value || '5';
    
    // Si hay campaña seleccionada, guardar ahí
    if (state.currentCampaignId) {
        let camp = state.campaigns.find(c => c.id === state.currentCampaignId);
        if (!camp) {
            camp = { id: state.currentCampaignId };
            state.campaigns.push(camp);
        }
        camp.config = {
            type: pType,
            colorPrimary: cPri,
            colorAccent: cAcc,
            iconClass: cIcon,
            stampsTotal: sTotal,
            customLogoUrl: state.customLogoUrl,
            customBannerUrl: state.customBannerUrl
        };
        console.log("Diseño guardado en la campaña: ", camp.id);
        if (typeof showToast === 'function') showToast("Diseño guardado para " + (camp.name || "la campaña seleccionada"), "success");
    } else {
        // Fallback al global
        state.colorPrimary = cPri;
        state.colorAccent = cAcc;
        state.iconClass = cIcon;
        console.log("Diseño guardado de forma global");
        if (typeof showToast === 'function') showToast("Diseño Global Guardado", "success");
    }
};
"""

js = re.sub(r'window\.saveDesign\s*=\s*async\s*function\(\)\s*\{', new_save_design, js, count=1)
print("saveDesign overridden for multi-card support.")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
