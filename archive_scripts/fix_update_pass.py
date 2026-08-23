import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# We need to replace the entire updatePassRender function.
# Let's find it.
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
        
        if (rIcon) rIcon.className = 'fa-solid ' + pIcon;
        if (rFront) rFront.style.background = `linear-gradient(135deg, ${cPri}, ${cAcc})`;
        
        // Safely update legacy UI elements if they exist
        const bannerContainer = document.getElementById('render-banner-container');
        const bannerImg = document.getElementById('render-banner-img');
        if (bannerContainer && bannerImg) {
            if (state.customBannerUrl) {
                bannerContainer.classList.remove('hidden');
                bannerImg.src = state.customBannerUrl;
            } else {
                bannerContainer.classList.add('hidden');
                bannerImg.src = '';
            }
        }

        const sampleClient = state.customers[0] || { tier: "Oro VIP", balance: 0, stamps: 0 };
        const clientTier = sampleClient.vip_tier || sampleClient.tier || 'Bronce';
        let currentTierConfig = state.vipTiers.oro;

        if (clientTier.toLowerCase().includes('oro')) {
            passRender.classList.add('tier-border-oro');
            currentTierConfig = state.vipTiers.oro;
        } else if (clientTier.toLowerCase().includes('plata')) {
            passRender.classList.add('tier-border-plata');
            currentTierConfig = state.vipTiers.plata;
        } else {
            passRender.classList.add('tier-border-bronce');
            currentTierConfig = state.vipTiers.bronce;
        }

        const vipCaption = document.getElementById('render-vip-caption');
        if (vipCaption) {
            if (state.vipActive) {
                vipCaption.style.display = 'block';
                vipCaption.textContent = currentTierConfig.name.toUpperCase();
            } else {
                vipCaption.style.display = 'none';
            }
        }

        const cashbackContainer = document.getElementById('render-cashback-container');
        if (cashbackContainer) {
            if (state.cashbackActive) {
                cashbackContainer.style.display = 'block';
                const bal = sampleClient.current_balance !== undefined ? sampleClient.current_balance : (sampleClient.balance || 0);
                const rBal = document.getElementById('render-balance');
                const rRate = document.getElementById('render-cashback-rate');
                if (rBal) rBal.textContent = `$${bal.toFixed(2)} MXN`;
                if (rRate) rRate.textContent = `${currentTierConfig.cashbackPercent}% acumulable (${currentTierConfig.name})`;
            } else {
                cashbackContainer.style.display = 'none';
            }
        }

        const stampsContainer = document.getElementById('render-stamps-container');
        if (stampsContainer) {
            if (state.stampsActive) {
                stampsContainer.style.display = 'block';
                const stampsGrid = document.getElementById('render-stamps-grid');
                if (stampsGrid) {
                    stampsGrid.innerHTML = '';
                    for (let i = 1; i <= state.stampsTotal; i++) {
                        const node = document.createElement('div');
                        if (i <= sampleClient.stamps) {
                            node.className = 'stamp-coin filled';
                            node.style.backgroundColor = state.colorAccent;
                            node.innerHTML = '<i class="fa-solid fa-check"></i>';
                        } else {
                            node.className = 'stamp-coin empty';
                            node.textContent = i;
                        }
                        stampsGrid.appendChild(node);
                    }
                }
                const rewardTxt = document.getElementById('render-reward-text');
                if (rewardTxt) rewardTxt.textContent = `Premio: ${state.stampsReward}`;
            } else {
                stampsContainer.style.display = 'none';
            }
        }

        const promoStrip = document.getElementById('render-promo-strip');
        if (promoStrip) {
            if (state.dynamicActive && state.dynamicDesc.trim() !== '') {
                promoStrip.style.display = 'flex';
                const rPromoText = document.getElementById('render-promo-text');
                if (rPromoText) rPromoText.textContent = state.dynamicDesc;
            } else {
                promoStrip.style.display = 'none';
            }
        }
    }"""

js = re.sub(pattern, new_function, js, flags=re.DOTALL)

with open('dashboard.js', 'w') as f:
    f.write(js)
