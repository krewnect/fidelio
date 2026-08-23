import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Add the flip button listener logic inside initFidelio (we'll just append it to the DOMContentLoaded handlers)
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
        
        // Also allow clicking the card itself to flip
        card3d.addEventListener('click', (e) => {
            // Don't flip if they are trying to click something else inside, just flip on generic card clicks
            card3d.classList.toggle('is-flipped');
            if (card3d.classList.contains('is-flipped')) {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-left"></i> Ver Frente';
            } else {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Ver Reverso (3D)';
            }
        });
    }
"""

# We can append this right after the window.selectCampaign block at the bottom
js += flip_logic

# Also update the updatePassRender function to handle the new IDs
# The old updatePassRender function:
update_pass_pattern = r'function updatePassRender\(\) \{.*?\}(?=\n\n|\n    function|\n    const)'
new_update_pass = """function updatePassRender() {
        const pName = document.getElementById('rest-name')?.value || "Mi Negocio";
        
        // Use the new free-text category input
        const catInput = document.getElementById('business-category-input');
        let pCat = "Restaurante & Gastronomía";
        if (catInput) {
            pCat = catInput.value;
        } else {
            // Fallback for old select if it still exists somewhere
            const oldCatSel = document.getElementById('business-category-select');
            if (oldCatSel) pCat = oldCatSel.options[oldCatSel.selectedIndex]?.text;
        }
        
        const pDesc = document.getElementById('rest-desc')?.value || "";
        const cPri = document.getElementById('color-primary')?.value || "#1e1b4b";
        const cAcc = document.getElementById('color-accent')?.value || "#8b5cf6";
        const pIcon = document.getElementById('rest-icon')?.value || "fa-crown";
        const pReward = document.getElementById('stamps-reward')?.value || "Bebida de Cortesía";
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
            rIcon.className = 'fa-solid ' + pIcon;
        }
        
        if (rFront) {
            rFront.style.background = `linear-gradient(135deg, ${cPri}, ${cAcc})`;
        }
    }"""

js = re.sub(update_pass_pattern, new_update_pass, js, flags=re.DOTALL)

with open('dashboard.js', 'w') as f:
    f.write(js)
