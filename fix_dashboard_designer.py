import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Add flip logic safely
flip_logic = """
    // --- 3D CARD FLIP LOGIC ---
    const btnFlipCard = document.getElementById('btn-flip-card');
    const card3d = document.getElementById('pass-render');
    if (btnFlipCard && card3d) {
        btnFlipCard.addEventListener('click', () => {
            card3d.classList.toggle('is-flipped');
            if (card3d.classList.contains('is-flipped')) {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-left"></i> Ver Frente';
            } else {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Ver Reverso (3D)';
            }
        });
        
        card3d.addEventListener('click', (e) => {
            card3d.classList.toggle('is-flipped');
            if (card3d.classList.contains('is-flipped')) {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-left"></i> Ver Frente';
            } else {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Ver Reverso (3D)';
            }
        });
    }
"""
js = js.replace('// --- WALLET SELECTOR ---', flip_logic + '\n    // --- WALLET SELECTOR ---')

# Replace updatePassRender content safely
old_update_pass = """    function updatePassRender() {
        if (!passRender) return;
        scheduleAutoSave(); // Trigger auto-save debouncer
        passRender.style.backgroundColor = state.colorPrimary;
        document.getElementById('render-name').textContent = state.restaurantName;
        
        const logoContainer = document.getElementById('render-logo-container');
        if (state.customLogoUrl) {
            logoContainer.innerHTML = `<img src="${state.customLogoUrl}" style="width:28px; height:28px; border-radius:6px; object-fit:cover;"> <span id="render-name">${state.restaurantName}</span>`;
        } else {
            logoContainer.innerHTML = `<i class="fa-solid ${state.iconClass}" id="render-icon" style="color:${state.colorAccent}"></i> <span id="render-name">${state.restaurantName}</span>`;
        }"""

new_update_pass = """    function updatePassRender() {
        if (!passRender) return;
        scheduleAutoSave();
        
        const pName = document.getElementById('rest-name')?.value || state.restaurantName || "Mi Negocio";
        const catInput = document.getElementById('business-category-input');
        let pCat = "Restaurante & Gastronomía";
        if (catInput) {
            pCat = catInput.value;
        } else {
            const oldCatSel = document.getElementById('business-category-select');
            if (oldCatSel) pCat = oldCatSel.options[oldCatSel.selectedIndex]?.text;
        }
        
        const pDesc = document.getElementById('rest-desc')?.value || state.dynamicDesc || "";
        const cPri = document.getElementById('color-primary')?.value || state.colorPrimary || "#1e1b4b";
        const cAcc = document.getElementById('color-accent')?.value || state.colorAccent || "#8b5cf6";
        const pIcon = document.getElementById('rest-icon')?.value || state.iconClass || "fa-crown";
        const pReward = document.getElementById('stamps-reward')?.value || state.stampsReward || "Bebida de Cortesía";
        const pPolicies = document.getElementById('pass-policies')?.value || "";

        const rName = document.getElementById('render-name');
        const rCat = document.getElementById('render-category');
        const rDesc = document.getElementById('render-promo-text');
        const rIcon = document.getElementById('render-icon');
        const rReward = document.getElementById('render-reward-text');
        const rPolicies = document.getElementById('render-policies-text');
        const rFront = document.getElementById('pass-front-face');

        if (rName) rName.textContent = pName;
        if (rCat) rCat.textContent = pCat;
        if (rDesc) rDesc.textContent = pDesc;
        if (rReward) rReward.textContent = pReward;
        if (rPolicies) rPolicies.textContent = pPolicies;
        
        if (rIcon) {
            // Keep it simple
            rIcon.className = 'fa-solid ' + pIcon;
        }
        
        if (rFront) {
            rFront.style.background = `linear-gradient(135deg, ${cPri}, ${cAcc})`;
        }"""

js = js.replace(old_update_pass, new_update_pass)

# Also need to fix safeAdd business-category-select which causes an error if categorySelect is null? No, safeAdd handles it.

with open('dashboard.js', 'w') as f:
    f.write(js)
