import re

with open('dashboard.js', 'r') as f:
    js = f.read()

pattern = r'function updatePassRender\(\) \{.*?\n    \}(?=\n\n    // --- UPLOAD HANDLERS ---)'

new_function = """function updatePassRender() {
        const passRender = document.getElementById('pass-render');
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
        const pReward = document.getElementById('stamps-reward')?.value || state.stampsReward || "Bebida de Cortesía Gratis";
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
        
        if (rIcon) rIcon.className = 'fa-solid ' + pIcon;
        if (rFront) rFront.style.background = `linear-gradient(135deg, ${cPri}, ${cAcc})`;
        
        const bannerContainer = document.getElementById('render-banner-container');
        const bannerImg = document.getElementById('render-banner-img');
        if (bannerContainer && bannerImg) {
            if (state.customBannerUrl) {
                bannerContainer.style.display = 'block';
                bannerImg.src = state.customBannerUrl;
            } else {
                bannerContainer.style.display = 'block';
                bannerImg.src = 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&q=80&w=800&h=300'; // Default placeholder
            }
        }

        const sampleClient = state.customers[0] || { tier: "Oro VIP", balance: 0, stamps: 0 };
        const clientTier = sampleClient.vip_tier || sampleClient.tier || 'Bronce';
        let currentTierConfig = state.vipTiers.oro;

        if (clientTier.toLowerCase().includes('oro')) {
            currentTierConfig = state.vipTiers.oro;
        } else if (clientTier.toLowerCase().includes('plata')) {
            currentTierConfig = state.vipTiers.plata;
        } else {
            currentTierConfig = state.vipTiers.bronce;
        }

        const vipCaption = document.getElementById('render-vip-caption');
        if (vipCaption) {
            vipCaption.textContent = currentTierConfig.name.toUpperCase();
        }

        const rBal = document.getElementById('render-balance');
        if (rBal) {
            const bal = sampleClient.current_balance !== undefined ? sampleClient.current_balance : (sampleClient.balance || 0);
            rBal.textContent = `$${bal.toFixed(2)}`;
        }
    }"""

js = re.sub(pattern, new_function, js, flags=re.DOTALL)

with open('dashboard.js', 'w') as f:
    f.write(js)
