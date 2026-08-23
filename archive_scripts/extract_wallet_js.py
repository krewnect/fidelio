import sys

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add toggle-prepaid declarations
js = js.replace("        const toggleVip = document.getElementById('toggle-vip');", "        const toggleVip = document.getElementById('toggle-vip');\n        const togglePrepaid = document.getElementById('toggle-prepaid');\n        const panelPrepaidConfig = document.getElementById('panel-prepaid-config');")

# 2. Fix the state loading and show/hide logic for prepaid
old_update_ui = """                if(mode === 'membership' || mode === 'prepaid' || mode === 'custom') {
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
                }"""
new_update_ui = """                if(mode === 'membership' || mode === 'custom') {
                    toggleCashback.checked = false;
                    toggleStamps.checked = false;
                    toggleVip.checked = false;
                    
                    if(customPanel) {
                        customPanel.style.display = 'block';
                        if(mode === 'membership') setMem.style.display = 'block';
                        if(mode === 'custom') setCus.style.display = 'block';
                        
                        if(cardTitle) {
                            document.getElementById('custom-panel-title').innerHTML = `<i class="fa-solid fa-sliders" style="color:var(--accent-violet); margin-right:8px;"></i> Configuración: ${cardTitle}`;
                        }
                    }
                }"""
js = js.replace(old_update_ui, new_update_ui)

# Add logic for togglePrepaid inside `if (state)`
old_custom_rules_load = """                if(state.customRules.prepaid) {
                    if(document.getElementById('pre-amount')) {
                        document.getElementById('pre-amount').value = state.customRules.prepaid.amount || 500;
                        const updatePrepaidTotal = () => {
                            const total = (parseFloat(document.getElementById('pre-amount').value) || 0) + (parseFloat(document.getElementById('pre-bonus').value) || 0);
                            if(document.getElementById('pre-total-display')) document.getElementById('pre-total-display').textContent = '$' + total;
                        };
                        updatePrepaidTotal();
                    }
                    if(document.getElementById('pre-bonus')) document.getElementById('pre-bonus').value = state.customRules.prepaid.bonus || 100;
                }"""
js = js.replace(old_custom_rules_load, "")

# And inject Prepaid state at the end of state load
old_end_state_load = """                    if(document.getElementById('cus-rules')) document.getElementById('cus-rules').value = state.customRules.custom.rules || '';
                }
            }
        }"""
new_end_state_load = """                    if(document.getElementById('cus-rules')) document.getElementById('cus-rules').value = state.customRules.custom.rules || '';
                }
            }
            if(togglePrepaid) {
                togglePrepaid.checked = state.prepaidActive === true;
                if(panelPrepaidConfig) panelPrepaidConfig.style.display = togglePrepaid.checked ? 'block' : 'none';
                if(document.getElementById('pre-amount')) document.getElementById('pre-amount').value = state.prepaidAmount || 500;
                if(document.getElementById('pre-bonus')) document.getElementById('pre-bonus').value = state.prepaidBonus || 100;
            }
        }"""
js = js.replace(old_end_state_load, new_end_state_load)

# Add Event Listener for togglePrepaid
old_prepaid_listeners = """        const preAmount = document.getElementById('pre-amount');
        const preBonus = document.getElementById('pre-bonus');
        const preTotal = document.getElementById('pre-total-display');
        if (preAmount && preBonus && preTotal) {
            const updatePrepaidTotal = () => {
                const total = (parseFloat(preAmount.value) || 0) + (parseFloat(preBonus.value) || 0);
                preTotal.textContent = '$' + total;
            };
            preAmount.addEventListener('input', updatePrepaidTotal);
            preBonus.addEventListener('input', updatePrepaidTotal);
        }"""
new_prepaid_listeners = """        const preAmount = document.getElementById('pre-amount');
        const preBonus = document.getElementById('pre-bonus');
        const preTotal = document.getElementById('pre-total-display');
        const prePay = document.getElementById('pre-pay-display');
        
        if (togglePrepaid && panelPrepaidConfig) {
            togglePrepaid.addEventListener('change', (e) => {
                panelPrepaidConfig.style.display = e.target.checked ? 'block' : 'none';
                if (window.updatePassRender) window.updatePassRender();
            });
        }
        
        if (preAmount && preBonus && preTotal) {
            const updatePrepaidTotal = () => {
                const amount = parseFloat(preAmount.value) || 0;
                const bonus = parseFloat(preBonus.value) || 0;
                const total = amount + bonus;
                if(prePay) prePay.textContent = amount;
                preTotal.textContent = '$' + total;
                if (window.updatePassRender) window.updatePassRender();
            };
            preAmount.addEventListener('input', updatePrepaidTotal);
            preBonus.addEventListener('input', updatePrepaidTotal);
            updatePrepaidTotal();
        }"""
js = js.replace(old_prepaid_listeners, new_prepaid_listeners)

# Update Save Payload
old_save = """                        vipActive: vipActive,
                        vipTiers: vipTiers,
                        customRules: {
                            membership: { price: document.getElementById('mem-price')?.value, perk: document.getElementById('mem-perk')?.value },
                            prepaid: { amount: document.getElementById('pre-amount')?.value, bonus: document.getElementById('pre-bonus')?.value },
                            custom: { name: document.getElementById('cus-name')?.value, rules: document.getElementById('cus-rules')?.value }
                        }
                    }).eq('id', state.tenantId);"""
new_save = """                        vipActive: vipActive,
                        vipTiers: vipTiers,
                        prepaidActive: togglePrepaid ? togglePrepaid.checked : false,
                        prepaidAmount: document.getElementById('pre-amount') ? parseFloat(document.getElementById('pre-amount').value) : 500,
                        prepaidBonus: document.getElementById('pre-bonus') ? parseFloat(document.getElementById('pre-bonus').value) : 100,
                        customRules: {
                            membership: { price: document.getElementById('mem-price')?.value, perk: document.getElementById('mem-perk')?.value },
                            custom: { name: document.getElementById('cus-name')?.value, rules: document.getElementById('cus-rules')?.value }
                        }
                    }).eq('id', state.tenantId);"""
js = js.replace(old_save, new_save)

# Update state variables after save
old_state_update = """                    state.vipTiers = vipTiers;
                    
                    // Re-render card preview if mode changed
                    updatePassRender();"""
new_state_update = """                    state.vipTiers = vipTiers;
                    state.prepaidActive = togglePrepaid ? togglePrepaid.checked : false;
                    state.prepaidAmount = document.getElementById('pre-amount') ? parseFloat(document.getElementById('pre-amount').value) : 500;
                    state.prepaidBonus = document.getElementById('pre-bonus') ? parseFloat(document.getElementById('pre-bonus').value) : 100;
                    
                    // Re-render card preview if mode changed
                    updatePassRender();"""
js = js.replace(old_state_update, new_state_update)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
    
print("Extracted Wallet JS.")
