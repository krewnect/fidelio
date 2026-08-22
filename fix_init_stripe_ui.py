import re

with open('live_dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """    sel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
    let camps = state.campaigns || [];
    if (camps.length === 0) {
        camps = [
            { id: 'camp_1', name: 'Monedero Digital General' },
            { id: 'camp_2', name: 'Tarjeta de Sellos' },
            { id: 'camp_3', name: 'Membresía VIP' }
        ];
    }
    
    camps.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c.id;
        opt.textContent = c.name || c.tipo || 'Programa';
        sel.appendChild(opt);
    });"""

replacement = """    // Populated dynamically by loadCampaigns
    if (sel.options.length <= 1) {
        // If not populated yet (only has default option), try to use state if available
        let camps = (window.state && window.state.campaigns) ? window.state.campaigns : [];
        if (camps.length > 0) {
            sel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
            camps.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.name || c.type || 'Programa';
                sel.appendChild(opt);
            });
        }
    }"""

js = js.replace(target, replacement)

with open('live_dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
