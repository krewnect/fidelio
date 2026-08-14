import sys

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I need to create a helper function that shows/hides the panels and call it on click and on load.
# Let's find the initial state load section for loyalty mode.
old_initial = """            // Set Mode
            const activeMode = state.activeMode || 'hybrid';
            loyaltyModes.forEach(radio => {
                if(radio.value === activeMode) radio.checked = true;
                const card = radio.closest('.role-card');
                if(radio.checked) card.classList.add('active');
                else card.classList.remove('active');
            });"""

new_initial = """            // Set Mode
            const activeMode = state.activeMode || 'hybrid';
            
            const updateLoyaltyUI = (mode, cardTitle) => {
                const customPanel = document.getElementById('panel-loyalty-custom');
                const standardPanel = document.getElementById('panel-loyalty-standard');
                const setMem = document.getElementById('settings-membership');
                const setPre = document.getElementById('settings-prepaid');
                const setCus = document.getElementById('settings-custom-prog');
                
                if(customPanel) customPanel.style.display = 'none';
                if(setMem) setMem.style.display = 'none';
                if(setPre) setPre.style.display = 'none';
                if(setCus) setCus.style.display = 'none';
                if(standardPanel) standardPanel.style.display = 'none';

                if(mode === 'cashback') {
                    if(standardPanel) standardPanel.style.display = 'block';
                    toggleCashback.checked = true;
                    toggleStamps.checked = false;
                    toggleVip.checked = false;
                } else if (mode === 'stamps') {
                    if(standardPanel) standardPanel.style.display = 'block';
                    toggleCashback.checked = false;
                    toggleStamps.checked = true;
                    toggleVip.checked = false;
                } else if (mode === 'hybrid') {
                    if(standardPanel) standardPanel.style.display = 'block';
                    toggleCashback.checked = true;
                    toggleStamps.checked = true;
                    toggleVip.checked = true;
                } else if (mode === 'membership' || mode === 'prepaid' || mode === 'custom') {
                    toggleCashback.checked = false;
                    toggleStamps.checked = false;
                    toggleVip.checked = false;
                    
                    if(customPanel) {
                        customPanel.style.display = 'block';
                        if(mode === 'membership') setMem.style.display = 'block';
                        if(mode === 'prepaid') setPre.style.display = 'block';
                        if(mode === 'custom') setCus.style.display = 'block';
                        
                        if(cardTitle) {
                            document.getElementById('custom-panel-title').innerHTML = `<i class="fa-solid fa-sliders" style="color:var(--accent-violet); margin-right:8px;"></i> Configuración: ${cardTitle}`;
                        }
                    }
                }
            };
            
            loyaltyModes.forEach(radio => {
                if(radio.value === activeMode) {
                    radio.checked = true;
                    updateLoyaltyUI(activeMode, radio.closest('.role-card').querySelector('h4').textContent);
                }
                const card = radio.closest('.role-card');
                if(radio.checked) card.classList.add('active');
                else card.classList.remove('active');
            });
            
            // Also expose updateLoyaltyUI to the click listeners later
            window.updateLoyaltyUI = updateLoyaltyUI;
"""
js = js.replace(old_initial, new_initial)

old_click = """                    const mode = card.querySelector('input').value;
                    const customPanel = document.getElementById('panel-loyalty-custom');
                    const setMem = document.getElementById('settings-membership');
                    const setPre = document.getElementById('settings-prepaid');
                    const setCus = document.getElementById('settings-custom-prog');
                    
                    if(customPanel) customPanel.style.display = 'none';
                    if(setMem) setMem.style.display = 'none';
                    if(setPre) setPre.style.display = 'none';
                    if(setCus) setCus.style.display = 'none';

                    if(mode === 'cashback') {
                        toggleCashback.checked = true;
                        toggleStamps.checked = false;
                        toggleVip.checked = false;
                    } else if (mode === 'stamps') {
                        toggleCashback.checked = false;
                        toggleStamps.checked = true;
                        toggleVip.checked = false;
                    } else if (mode === 'hybrid') {
                        toggleCashback.checked = true;
                        toggleStamps.checked = true;
                        toggleVip.checked = true;
                    } else if (mode === 'membership' || mode === 'prepaid' || mode === 'custom') {
                        toggleCashback.checked = false;
                        toggleStamps.checked = false;
                        toggleVip.checked = false;
                        
                        if(customPanel) {
                            customPanel.style.display = 'block';
                            if(mode === 'membership') setMem.style.display = 'block';
                            if(mode === 'prepaid') setPre.style.display = 'block';
                            if(mode === 'custom') setCus.style.display = 'block';
                            
                            document.getElementById('custom-panel-title').innerHTML = `<i class="fa-solid fa-sliders" style="color:var(--accent-violet); margin-right:8px;"></i> Configuración: ${card.querySelector('h4').textContent}`;
                        }
                    }"""

new_click = """                    const mode = card.querySelector('input').value;
                    if(window.updateLoyaltyUI) {
                        window.updateLoyaltyUI(mode, card.querySelector('h4').textContent);
                    }"""
js = js.replace(old_click, new_click)

# Initialize custom rules if present
old_vip = """                if(state.vipTiers.oro) {
                    document.getElementById('vip-oro-min').value = state.vipTiers.oro.minSpent || 3000;
                    document.getElementById('vip-oro-cb').value = state.vipTiers.oro.cashbackPercent || 15;
                    document.getElementById('vip-oro-perk').value = state.vipTiers.oro.perk || 'Beneficio Oro';
                }
            }
        }"""
new_vip = """                if(state.vipTiers.oro) {
                    document.getElementById('vip-oro-min').value = state.vipTiers.oro.minSpent || 3000;
                    document.getElementById('vip-oro-cb').value = state.vipTiers.oro.cashbackPercent || 15;
                    document.getElementById('vip-oro-perk').value = state.vipTiers.oro.perk || 'Beneficio Oro';
                }
            }
            if (state.customRules) {
                if(state.customRules.membership) {
                    if(document.getElementById('mem-price')) document.getElementById('mem-price').value = state.customRules.membership.price || 199;
                    if(document.getElementById('mem-perk')) document.getElementById('mem-perk').value = state.customRules.membership.perk || '20% OFF en Tienda';
                }
                if(state.customRules.prepaid) {
                    if(document.getElementById('pre-amount')) {
                        document.getElementById('pre-amount').value = state.customRules.prepaid.amount || 500;
                        const updatePrepaidTotal = () => {
                            const total = (parseFloat(document.getElementById('pre-amount').value) || 0) + (parseFloat(document.getElementById('pre-bonus').value) || 0);
                            if(document.getElementById('pre-total-display')) document.getElementById('pre-total-display').textContent = '$' + total;
                        };
                        updatePrepaidTotal();
                    }
                    if(document.getElementById('pre-bonus')) document.getElementById('pre-bonus').value = state.customRules.prepaid.bonus || 100;
                }
                if(state.customRules.custom) {
                    if(document.getElementById('cus-name')) document.getElementById('cus-name').value = state.customRules.custom.name || 'Mi Programa VIP';
                    if(document.getElementById('cus-rules')) document.getElementById('cus-rules').value = state.customRules.custom.rules || '';
                }
            }
        }"""
js = js.replace(old_vip, new_vip)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated JS logic.")
