import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

profile_js = """
window.showCustomerProfile = function(id) {
    if (!state || !state.customers) return;
    const c = state.customers.find(x => x.id === id);
    if (!c) return;

    const comp = c.computed || {};
    const name = c.full_name || c.name || 'Cliente sin nombre';
    
    document.getElementById('cp-name').textContent = name;
    document.getElementById('cp-id').textContent = c.id;
    document.getElementById('cp-avatar').textContent = name.charAt(0).toUpperCase();
    
    document.getElementById('cp-tier').textContent = comp.tier || 'Bronce VIP';
    document.getElementById('cp-balance').textContent = '$' + (comp.balance || 0).toFixed(2) + ' MXN';
    document.getElementById('cp-spent').textContent = '$' + (comp.spent || 0).toFixed(2) + ' MXN';
    document.getElementById('cp-visits').textContent = (c.visits || 0) + ' Visitas';
    
    document.getElementById('cp-phone').textContent = c.phone || 'N/A';
    document.getElementById('cp-email').textContent = c.email || 'N/A';
    document.getElementById('cp-bday').textContent = comp.bdayFormatted || 'N/A';
    
    document.getElementById('cp-anniv').textContent = comp.annivFormatted || 'N/A';
    document.getElementById('cp-last-visit').textContent = comp.lastVisitFormatted || 'N/A';
    
    const statusDiv = document.getElementById('cp-status');
    statusDiv.innerHTML = `<span class="badge-status ${comp.statusClass}" style="padding:4px 8px; font-size:11px;">${comp.statusText}</span>`;

    document.getElementById('modal-customer-profile').style.display = 'flex';
};
"""

js += "\n\n" + profile_js

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'src="dashboard\.js\?v=\d+"', 'src="dashboard.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
