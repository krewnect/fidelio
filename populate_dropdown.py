import re

with open('live_dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        // Store in state so other tabs (Stripe, Builder) can read it
        if (typeof state !== 'undefined') {
            state.campaigns = data.campaigns;
        }"""

replacement = """        // Store in state so other tabs (Stripe, Builder) can read it
        if (typeof state !== 'undefined') {
            state.campaigns = data.campaigns;
        } else {
            window.state = { campaigns: data.campaigns };
        }
        
        // Populate Stripe Dropdown immediately
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

js = js.replace(target, replacement)

with open('live_dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
