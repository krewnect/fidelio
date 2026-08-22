import re

with open('live_dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        if (!res.ok) throw new Error("Failed to fetch");
        const data = await res.json();
        const list = document.getElementById('campaigns-list');
        if (!list) return;
        
        list.innerHTML = data.campaigns.map(c => `"""

replacement = """        if (!res.ok) throw new Error("Failed to fetch");
        const data = await res.json();
        
        // Store in state so other tabs (Stripe, Builder) can read it
        if (typeof state !== 'undefined') {
            state.campaigns = data.campaigns;
        }
        
        const list = document.getElementById('campaigns-list');
        if (!list) return;
        
        list.innerHTML = data.campaigns.map(c => `"""

js = js.replace(target, replacement)

with open('live_dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
