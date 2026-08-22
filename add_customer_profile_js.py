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

js = js.replace('window.showCustomerQR = function(id, name) {', profile_js + '\nwindow.showCustomerQR = function(id, name) {')

# Now update the onclick handler for the CRM table
target = """<button class="btn btn-outline" style="padding:6px 10px; font-size:12px; margin-left:4px;" title="Ver Perfil Detallado" onclick="if(typeof Swal !== \\'undefined\\'){Swal.fire('Perfil del Cliente','Detalles extendidos del cliente muy pronto.','info');}else{alert('Detalles del perfil pronto.');}">"""
replacement = """<button class="btn btn-outline" style="padding:6px 10px; font-size:12px; margin-left:4px;" title="Ver Perfil Detallado" onclick="window.showCustomerProfile('${c.id}')">"""

js = js.replace(target, replacement)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
