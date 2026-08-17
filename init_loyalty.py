import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

init_loyalty_logic = """
// --- LOYALTY TAB INIT ---
window.initLoyaltyTab = function() {
    // 1. Loyalty Mode (Hybrid, Cashback, Stamps, Custom)
    const mode = state.activeMode || 'hybrid';
    const card = document.getElementById(`loyalty-mode-${mode}`);
    if (card) {
        document.querySelectorAll('.role-card[id^="loyalty-mode-"]').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        const radio = card.querySelector('input');
        if(radio) radio.checked = true;
    }

    // 2. Toggles & Sliders
    const safeSetChecked = (id, val) => { const el = document.getElementById(id); if(el) el.checked = !!val; };
    const safeSetValue = (id, val) => { const el = document.getElementById(id); if(el) el.value = val; };

    safeSetChecked('toggle-cashback', state.cashbackActive !== false);
    safeSetValue('cashback-slider', state.cashbackPercent || 10);
    const cbDisplay = document.getElementById('cashback-percent-display');
    if(cbDisplay) cbDisplay.textContent = (state.cashbackPercent || 10) + '%';
    const cbExample = document.getElementById('cashback-example');
    if(cbExample) cbExample.textContent = state.cashbackPercent || 10;

    safeSetChecked('toggle-stamps', state.stampsActive !== false);
    safeSetValue('stamps-total', state.stampsTotal || 5);
    safeSetValue('stamps-reward', state.stampsReward || 'Premio Gratis');

    safeSetChecked('toggle-vip', state.vipActive !== false);
    
    // VIP Tiers
    if (state.vipTiers) {
        if (state.vipTiers.bronce) {
            safeSetValue('vip-bronce-cb', state.vipTiers.bronce.cashbackPercent || 5);
            safeSetValue('vip-bronce-perk', state.vipTiers.bronce.perk || '');
        }
        if (state.vipTiers.plata) {
            safeSetValue('vip-plata-min', state.vipTiers.plata.minSpent || 1000);
            safeSetValue('vip-plata-cb', state.vipTiers.plata.cashbackPercent || 10);
            safeSetValue('vip-plata-perk', state.vipTiers.plata.perk || '');
        }
        if (state.vipTiers.oro) {
            safeSetValue('vip-oro-min', state.vipTiers.oro.minSpent || 3000);
            safeSetValue('vip-oro-cb', state.vipTiers.oro.cashbackPercent || 15);
            safeSetValue('vip-oro-perk', state.vipTiers.oro.perk || '');
        }
    }

    // Prepaid
    safeSetChecked('toggle-prepaid', state.prepaidActive === true);
    safeSetValue('pre-amount', state.prepaidAmount || 500);
    safeSetValue('pre-bonus', state.prepaidBonus || 100);
    const panelPrepaid = document.getElementById('panel-prepaid-config');
    if (panelPrepaid) panelPrepaid.style.display = state.prepaidActive ? 'block' : 'none';
};
"""

# Find where to inject initLoyaltyTab
if 'window.initLoyaltyTab' not in js:
    # Append it to the file
    js += init_loyalty_logic
    print("Injected initLoyaltyTab")

# Find the tab switching logic to call it when tab-loyalty is opened
tab_switch_code = """
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                if(tab.hasAttribute('onclick')) return; // Skip if it has inline onclick
                const target = tab.getAttribute('data-tab');
                if(!target) return;
                
                document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active-tab'));
                const targetTab = document.getElementById(target);
                if (targetTab) targetTab.classList.add('active-tab');
                
                // Call initializers based on tab
                if (target === 'tab-loyalty' && window.initLoyaltyTab) {
                    window.initLoyaltyTab();
                }
"""

if "if (target === 'tab-loyalty' && window.initLoyaltyTab)" not in js:
    # Need to inject the call into the tab click listener
    old_tab_listener = """
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active-tab'));
                const targetTab = document.getElementById(target);
                if (targetTab) targetTab.classList.add('active-tab');
            });
"""
    new_tab_listener = """
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active-tab'));
                const targetTab = document.getElementById(target);
                if (targetTab) targetTab.classList.add('active-tab');
                
                // Call initializers based on tab
                if (target === 'tab-loyalty' && window.initLoyaltyTab) {
                    window.initLoyaltyTab();
                }
            });
"""
    if old_tab_listener in js:
        js = js.replace(old_tab_listener, new_tab_listener)
        print("Added call to initLoyaltyTab on tab switch")
    else:
        print("WARNING: Could not find exact tab click listener.")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
