import sys

js_content = """
    // --- LOYALTY RULES LOGIC ---
    const tabLoyalty = document.getElementById('tab-loyalty');
    if (tabLoyalty) {
        // UI Selectors
        const loyaltyModes = document.querySelectorAll('input[name="loyalty_mode"]');
        const modeCards = document.querySelectorAll('input[name="loyalty_mode"] + .role-icon').map(el => el.parentElement);
        
        const toggleCashback = document.getElementById('toggle-cashback');
        const cashbackSlider = document.getElementById('cashback-slider');
        const cashbackDisplay = document.getElementById('cashback-percent-display');
        const cashbackExample = document.getElementById('cashback-example');
        
        const toggleStamps = document.getElementById('toggle-stamps');
        const stampsTotal = document.getElementById('stamps-total');
        const stampsReward = document.getElementById('stamps-reward');
        
        const toggleVip = document.getElementById('toggle-vip');
        const vipRows = document.querySelectorAll('#tab-loyalty table tbody tr');
        
        // Populate Initial Values from State
        if (state) {
            // Set Mode
            const activeMode = state.activeMode || 'hybrid';
            loyaltyModes.forEach(radio => {
                if(radio.value === activeMode) radio.checked = true;
                const card = radio.closest('.role-card');
                if(radio.checked) card.classList.add('active');
                else card.classList.remove('active');
            });
            
            // Set Cashback
            toggleCashback.checked = state.cashbackActive !== false;
            cashbackSlider.value = state.cashbackPercent || 10;
            cashbackDisplay.textContent = cashbackSlider.value + '%';
            cashbackExample.textContent = cashbackSlider.value;
            
            // Set Stamps
            toggleStamps.checked = state.stampsActive !== false;
            stampsTotal.value = state.stampsTotal || 5;
            stampsReward.value = state.stampsReward || 'Premio Gratis';
            
            // Set VIP
            toggleVip.checked = state.vipActive !== false;
            if (state.vipTiers) {
                if(state.vipTiers.bronce) {
                    document.getElementById('vip-bronce-cb').value = state.vipTiers.bronce.cashbackPercent || 5;
                    document.getElementById('vip-bronce-perk').value = state.vipTiers.bronce.perk || 'Beneficio Base';
                }
                if(state.vipTiers.plata) {
                    document.getElementById('vip-plata-min').value = state.vipTiers.plata.minSpent || 1000;
                    document.getElementById('vip-plata-cb').value = state.vipTiers.plata.cashbackPercent || 10;
                    document.getElementById('vip-plata-perk').value = state.vipTiers.plata.perk || 'Beneficio Plata';
                }
                if(state.vipTiers.oro) {
                    document.getElementById('vip-oro-min').value = state.vipTiers.oro.minSpent || 3000;
                    document.getElementById('vip-oro-cb').value = state.vipTiers.oro.cashbackPercent || 15;
                    document.getElementById('vip-oro-perk').value = state.vipTiers.oro.perk || 'Beneficio Oro';
                }
            }
        }
        
        // Event Listeners for UI interaction
        document.querySelectorAll('.role-card').forEach(card => {
            if(card.id.startsWith('loyalty-mode-')) {
                card.addEventListener('click', () => {
                    document.querySelectorAll('.role-card[id^="loyalty-mode-"]').forEach(c => c.classList.remove('active'));
                    card.classList.add('active');
                    card.querySelector('input').checked = true;
                    
                    const mode = card.querySelector('input').value;
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
                    }
                });
            }
        });
        
        if (cashbackSlider) {
            cashbackSlider.addEventListener('input', (e) => {
                cashbackDisplay.textContent = e.target.value + '%';
                cashbackExample.textContent = e.target.value;
            });
        }
        
        // Save Button Logic
        const btnSaveLoyalty = document.getElementById('btn-save-loyalty');
        if (btnSaveLoyalty) {
            btnSaveLoyalty.addEventListener('click', async () => {
                const activeMode = document.querySelector('input[name="loyalty_mode"]:checked').value;
                const cashbackActive = toggleCashback.checked;
                const cashbackPercent = parseInt(cashbackSlider.value);
                
                const stampsActive = toggleStamps.checked;
                const totalStamps = parseInt(stampsTotal.value);
                const reward = stampsReward.value;
                
                const vipActive = toggleVip.checked;
                const vipTiers = {
                    bronce: { 
                        name: "Bronce", minSpent: 0, 
                        cashbackPercent: parseInt(document.getElementById('vip-bronce-cb').value), 
                        perk: document.getElementById('vip-bronce-perk').value 
                    },
                    plata: { 
                        name: "Plata VIP", minSpent: parseInt(document.getElementById('vip-plata-min').value), 
                        cashbackPercent: parseInt(document.getElementById('vip-plata-cb').value), 
                        perk: document.getElementById('vip-plata-perk').value 
                    },
                    oro: { 
                        name: "Oro VIP", minSpent: parseInt(document.getElementById('vip-oro-min').value), 
                        cashbackPercent: parseInt(document.getElementById('vip-oro-cb').value), 
                        perk: document.getElementById('vip-oro-perk').value 
                    }
                };
                
                btnSaveLoyalty.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Guardando...';
                btnSaveLoyalty.disabled = true;
                
                try {
                    const { error } = await window.supabaseClient.from('merchants').update({
                        activeMode: activeMode,
                        cashbackActive: cashbackActive,
                        cashbackPercent: cashbackPercent,
                        stampsActive: stampsActive,
                        stampsTotal: totalStamps,
                        stampsReward: reward,
                        vipActive: vipActive,
                        vipTiers: vipTiers
                    }).eq('id', state.tenantId);
                    
                    if (error) throw error;
                    
                    // Update local state
                    state.activeMode = activeMode;
                    state.cashbackActive = cashbackActive;
                    state.cashbackPercent = cashbackPercent;
                    state.stampsActive = stampsActive;
                    state.stampsTotal = totalStamps;
                    state.stampsReward = reward;
                    state.vipActive = vipActive;
                    state.vipTiers = vipTiers;
                    
                    // Re-render card preview if mode changed
                    updatePassRender();
                    
                    showToast('Reglas de Fidelización guardadas exitosamente.', 'success');
                } catch (err) {
                    console.error("Error saving loyalty config:", err);
                    showToast('Error al guardar: ' + err.message, 'warning');
                } finally {
                    btnSaveLoyalty.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Guardar Reglas';
                    btnSaveLoyalty.disabled = false;
                }
            });
        }
    }
"""

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
insert_idx = -1
for i in range(len(lines)-1, -1, -1):
    if "})();" in lines[i]:
        insert_idx = i
        break
        
if insert_idx != -1:
    lines = lines[:insert_idx] + [js_content] + lines[insert_idx:]
    with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Injected JS logic successfully.")
else:
    print("Could not find insert point in JS.")
