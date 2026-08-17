import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_builder = """window.populateBuilderCampaignSelect = function() {
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

new_builder = """function getBuilderCampaigns() {
    let camps = state.campaigns || [];
    if (camps.length === 0) {
        camps = [
            { id: 'camp_1', name: 'Monedero Digital General', config: { type: 'cashback', colorPrimary: '#1e1b4b', colorAccent: '#8b5cf6', iconClass: 'fa-wallet' } },
            { id: 'camp_2', name: 'Tarjeta de Sellos', config: { type: 'stamps', colorPrimary: '#0f172a', colorAccent: '#f59e0b', iconClass: 'fa-star', stampsTotal: 10 } },
            { id: 'camp_3', name: 'Membresía VIP', config: { type: 'hybrid', colorPrimary: '#3f3f46', colorAccent: '#eab308', iconClass: 'fa-crown' } }
        ];
    }
    return camps;
}

window.populateBuilderCampaignSelect = function() {
    const sel = document.getElementById('builder-campaign-select');
    if (!sel) return;
    
    sel.innerHTML = '<option value="">-- Selecciona una campaña --</option>';
    
    const camps = getBuilderCampaigns();
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
    if (!campaignId) {
        state.currentCampaignId = null;
        if(window.checkRedundancy) window.checkRedundancy();
        return;
    }
    state.currentCampaignId = campaignId;
    
    const camps = getBuilderCampaigns();
    let camp = camps.find(c => c.id === campaignId);
    
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
        
        if (typeof showToast === 'function') showToast("Cargando ajustes predeterminados de campaña: " + (camp.name || camp.tipo), "success");
    } else {
        if (typeof showToast === 'function') showToast("Campaña nueva. Configura el diseño.", "info");
    }
    
    if(window.checkRedundancy) window.checkRedundancy();
    if(window.updatePassRender) window.updatePassRender();
};"""

if old_builder in js:
    js = js.replace(old_builder, new_builder)
    print("Dashboard JS builder logic updated.")
else:
    print("WARNING: Could not find exact old builder logic to replace.")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
