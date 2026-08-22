import re

with open('live_dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's forcefully populate the dropdown directly in loadDataFromSupabase AND loadCampaigns just to be absolutely sure.
target = """        // Populate Stripe Dropdown immediately
        const stripeSel = document.getElementById('stripe-campaign-select');
        if (stripeSel) {
            stripeSel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
            data.campaigns.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.name || c.type || 'Programa';
                stripeSel.appendChild(opt);
            });
        }"""

replacement = """        // Populate Stripe Dropdown immediately
        const stripeSel = document.getElementById('stripe-campaign-select');
        if (stripeSel) {
            stripeSel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
            data.campaigns.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.name || c.type || 'Programa';
                stripeSel.appendChild(opt);
            });
            console.log("Dropdown populated with:", data.campaigns.length, "campaigns");
        }"""

js = js.replace(target, replacement)

# Add a failsafe click handler to the monetization tab to repopulate it on click just in case
tab_logic = """                if(targetTab === 'tab-leads' && typeof window.loadLeads === 'function') window.loadLeads();"""
tab_logic_replacement = """                if(targetTab === 'tab-stripe') {
                    const sel = document.getElementById('stripe-campaign-select');
                    let camps = (window.state && window.state.campaigns) ? window.state.campaigns : [];
                    if (sel && camps.length > 0) {
                        sel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
                        camps.forEach(c => {
                            const opt = document.createElement('option');
                            opt.value = c.id;
                            opt.textContent = c.name || c.type || 'Programa';
                            sel.appendChild(opt);
                        });
                    }
                }
                if(targetTab === 'tab-leads' && typeof window.loadLeads === 'function') window.loadLeads();"""

js = js.replace(tab_logic, tab_logic_replacement)

with open('live_dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
