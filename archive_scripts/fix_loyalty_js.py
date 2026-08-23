import sys

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update the Event Listener for Role Cards to handle new modes
old_listener = """                    if(mode === 'cashback') {
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
                    }
                });
            }"""

new_listener = """                    const customPanel = document.getElementById('panel-loyalty-custom');
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
                    }
                });
            }"""
js = js.replace(old_listener, new_listener)

# 2. Add Prepaid auto-calculator listener
auto_calc_js = """
        const preAmount = document.getElementById('pre-amount');
        const preBonus = document.getElementById('pre-bonus');
        const preTotal = document.getElementById('pre-total-display');
        if (preAmount && preBonus && preTotal) {
            const updatePrepaidTotal = () => {
                const total = (parseFloat(preAmount.value) || 0) + (parseFloat(preBonus.value) || 0);
                preTotal.textContent = '$' + total;
            };
            preAmount.addEventListener('input', updatePrepaidTotal);
            preBonus.addEventListener('input', updatePrepaidTotal);
        }
        
        // Save Button Logic
"""
js = js.replace("        // Save Button Logic", auto_calc_js)

# 3. Update Save Payload
old_save = """                        vipActive: vipActive,
                        vipTiers: vipTiers
                    }).eq('id', state.tenantId);"""

new_save = """                        vipActive: vipActive,
                        vipTiers: vipTiers,
                        customRules: {
                            membership: { price: document.getElementById('mem-price')?.value, perk: document.getElementById('mem-perk')?.value },
                            prepaid: { amount: document.getElementById('pre-amount')?.value, bonus: document.getElementById('pre-bonus')?.value },
                            custom: { name: document.getElementById('cus-name')?.value, rules: document.getElementById('cus-rules')?.value }
                        }
                    }).eq('id', state.tenantId);"""
js = js.replace(old_save, new_save)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated dashboard.js with new loyalty logic.")
