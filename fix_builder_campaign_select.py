import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# INJECT CAMPAIGN SELECT IN BUILDER
target_html = """                                <div>
                                    <label class="premium-label">Nombre del Negocio</label>"""

injection = """                                <div style="margin-bottom: 24px;">
                                    <label class="premium-label" style="color:var(--accent-violet);">Campaña de Fidelización Asociada</label>
                                    <select id="builder-campaign-select" class="premium-input" style="font-weight:600; border-color:var(--accent-violet);" onchange="if(window.loadCampaignToBuilder) window.loadCampaignToBuilder(this.value)">
                                        <option value="">-- Selecciona una campaña --</option>
                                    </select>
                                    <p style="font-size:12px; color:var(--text-muted); margin-top:4px;">Asocia este diseño a un programa específico. El diseño será único para la campaña seleccionada.</p>
                                </div>
                                
                                <div>
                                    <label class="premium-label">Nombre del Negocio</label>"""

if target_html in html:
    html = html.replace(target_html, injection)
    print("Injected builder campaign select HTML.")
else:
    print("Could not find target html for builder select.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# INJECT JS LOGIC FOR CAMPAIGN SELECT
js_injection = """
// --- MULTI-CARD BUILDER LOGIC ---
window.populateBuilderCampaignSelect = function() {
    const sel = document.getElementById('builder-campaign-select');
    if (!sel) return;
    
    // Clear
    sel.innerHTML = '<option value="">-- Selecciona una campaña --</option>';
    
    // Mock campaigns if state.campaigns is empty
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
    });
    
    if (state.currentCampaignId) {
        sel.value = state.currentCampaignId;
    }
};

window.loadCampaignToBuilder = function(campaignId) {
    if (!campaignId) return;
    state.currentCampaignId = campaignId;
    
    // Generate a fresh mock config based on the ID to simulate loading distinct designs
    if (campaignId === 'camp_2') {
        document.getElementById('program-type-select').value = 'stamps';
        document.getElementById('color-primary').value = '#1e1b4b';
        document.getElementById('color-accent').value = '#4ade80';
    } else if (campaignId === 'camp_3') {
        document.getElementById('program-type-select').value = 'cashback';
        document.getElementById('color-primary').value = '#000000';
        document.getElementById('color-accent').value = '#fbbf24';
        document.getElementById('rest-name').value = 'Membresía VIP';
    } else {
        document.getElementById('program-type-select').value = 'cashback';
        document.getElementById('color-primary').value = '#1e1b4b';
        document.getElementById('color-accent').value = '#8b5cf6';
    }
    
    if (window.updatePassRender) window.updatePassRender();
    if (typeof showToast === 'function') showToast("Diseño cargado para la campaña seleccionada.", "success");
};

// Make sure to call populateBuilderCampaignSelect when switching to tab-builder
const origSwitchTab = window.switchTab;
window.switchTab = function(tabId) {
    if (origSwitchTab) origSwitchTab(tabId);
    if (tabId === 'tab-builder' && window.populateBuilderCampaignSelect) {
        window.populateBuilderCampaignSelect();
    }
};
"""

js += js_injection
with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Injected JS logic for builder campaign select.")

