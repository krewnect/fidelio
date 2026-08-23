import re

# 1. ADD PREMIUM CSS FOR PREVIEW AND STAMPS
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

premium_css = """
/* PREMIUM PASS PREVIEW */
.pass-preview-card {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    position: relative;
    overflow: hidden;
}

.pass-preview-card::before {
    content: '';
    position: absolute;
    top: 0; left: -50%; width: 200%; height: 100%;
    background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%);
    transform: rotate(30deg);
    pointer-events: none;
}

.stamp-coin {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 800;
    color: #fff;
    background: rgba(255,255,255,0.1);
    border: 2px solid rgba(255,255,255,0.2);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
}
.stamp-coin.filled {
    box-shadow: 0 0 10px rgba(255,255,255,0.5), inset 0 2px 4px rgba(255,255,255,0.5);
    border-color: rgba(255,255,255,0.8);
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23fff"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>');
    background-size: 60%;
    background-repeat: no-empty;
    background-position: center;
}
"""
if ".pass-preview-card {" not in css:
    css += premium_css
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Premium CSS injected.")

# 2. FIX JS LOGIC IN DASHBOARD
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace mock loadCampaignToBuilder with real data loader
mock_loader_pattern = re.compile(r'window\.loadCampaignToBuilder = function\(campaignId\)\s*\{.*?(?=\};)\};', re.DOTALL)

real_loader = """window.loadCampaignToBuilder = function(campaignId) {
    if (!campaignId) {
        state.currentCampaignId = null;
        if(window.checkRedundancy) window.checkRedundancy();
        return;
    }
    state.currentCampaignId = campaignId;
    
    let camp = state.campaigns ? state.campaigns.find(c => c.id === campaignId) : null;
    if (camp && camp.config) {
        const c = camp.config;
        
        const pt = document.getElementById('program-type-select');
        if(pt && c.type) pt.value = c.type;
        
        const cPri = document.getElementById('color-primary');
        if(cPri && c.colorPrimary) cPri.value = c.colorPrimary;
        
        const cAcc = document.getElementById('color-accent');
        if(cAcc && c.colorAccent) cAcc.value = c.colorAccent;
        
        const rIcon = document.getElementById('rest-icon');
        if(rIcon && c.iconClass) rIcon.value = c.iconClass;
        
        const st = document.getElementById('stamps-total');
        if(st && c.stampsTotal) st.value = c.stampsTotal;
        
        if (typeof showToast === 'function') showToast("Diseño cargado desde la campaña: " + (camp.name || camp.tipo), "success");
    } else {
        if (typeof showToast === 'function') showToast("Campaña nueva. Configura el diseño.", "info");
    }
    
    if(window.checkRedundancy) window.checkRedundancy();
    if(window.updatePassRender) window.updatePassRender();
};"""

if mock_loader_pattern.search(js):
    js = mock_loader_pattern.sub(real_loader, js)
    print("Real loadCampaignToBuilder injected.")
else:
    js += '\n' + real_loader
    print("Real loadCampaignToBuilder appended.")

# Replace redundancy logic to target the parent correctly and run on load
old_redundancy = """// Listener para ocultar redundancias si se selecciona una campaña
document.addEventListener('DOMContentLoaded', () => {
    const campSel = document.getElementById('builder-campaign-select');
    if(campSel) {
        campSel.addEventListener('change', (e) => {
            const isCamp = !!e.target.value;
            // Campos redundantes: Mensaje Corto (Promo) y Premio a Desbloquear
            const msgInput = document.getElementById('rest-desc');
            const rewardInput = document.getElementById('stamps-reward');
            
            if(msgInput && msgInput.parentElement) msgInput.parentElement.style.display = isCamp ? 'none' : 'block';
            if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = isCamp ? 'none' : 'block';
        });
    }
});"""

new_redundancy = """window.checkRedundancy = function() {
    const campSel = document.getElementById('builder-campaign-select');
    const isCamp = campSel ? !!campSel.value : !!state.currentCampaignId;
    
    const msgInput = document.getElementById('rest-desc');
    const rewardInput = document.getElementById('stamps-reward');
    
    if(msgInput && msgInput.parentElement) msgInput.parentElement.style.display = isCamp ? 'none' : 'block';
    if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = isCamp ? 'none' : 'block';
};

document.addEventListener('DOMContentLoaded', () => {
    const campSel = document.getElementById('builder-campaign-select');
    if(campSel) {
        campSel.addEventListener('change', window.checkRedundancy);
    }
    setTimeout(window.checkRedundancy, 100);
});"""

if old_redundancy in js:
    js = js.replace(old_redundancy, new_redundancy)
    print("Redundancy JS replaced.")
else:
    js += '\n' + new_redundancy
    print("Redundancy JS appended.")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
