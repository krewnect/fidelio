import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove 'Creador de Tarjetas' from sidebar
target_sidebar = '<button class="nav-tab" data-tab="tab-builder" id="nav-builder"><i class="fa-solid fa-wand-magic-sparkles"></i> Creador de Tarjetas</button>'
html = html.replace(target_sidebar, '<!-- Creador de Tarjetas oculto del sidebar (fusionado) -->')

# 2. Add "Volver a Mis Campañas" button in tab-builder
target_builder_h1 = '<h1 style="font-size: 24px; font-weight: 800; letter-spacing: -1px; color: #111827;">✨ Creador de Tarjetas Mágico</h1>'
back_btn = """
                            <button onclick="document.querySelector('.nav-tab[data-tab=\\'tab-campaigns\\']').click()" style="background:transparent; border:none; color:#6b7280; font-size:14px; font-weight:600; cursor:pointer; margin-bottom:16px; display:flex; align-items:center; gap:8px; padding:0; transition:color 0.2s;" onmouseover="this.style.color='#111827'" onmouseout="this.style.color='#6b7280'">
                                <i class="fa-solid fa-arrow-left"></i> Volver a Mis Campañas
                            </button>
                            <h1 style="font-size: 24px; font-weight: 800; letter-spacing: -1px; color: #111827;">✨ Creador Mágico</h1>"""
html = html.replace(target_builder_h1, back_btn)

# 3. Fix the "Mis Campañas" empty state if it's boring, and add the "Nueva Campaña" button nicely.
# Wait, let's just make sure tab-campaigns looks like a unified control center.
target_campaigns_header = """                    <div>
                        <h1>Mis Campañas</h1>
                        <p>Selecciona una campaña para editarla o crea una nueva.</p>
                    </div>"""
new_campaigns_header = """                    <div>
                        <h1 style="font-size:28px; font-weight:800; letter-spacing:-1px;">Gestión de Campañas</h1>
                        <p style="color:var(--text-muted);">Crea, diseña y edita las reglas de tus tarjetas desde un solo lugar.</p>
                    </div>"""
html = html.replace(target_campaigns_header, new_campaigns_header)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Now update the javascript logic
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make sure selectCampaign switches to tab-builder
target_select = """window.selectCampaign = function(id) {
    state.currentCampaignId = id;
    const isPro = (window.merchantData && window.merchantData.business_type === 'professional');
    
    // Redirect logic: Professionals skip Loyalty and go directly to Builder
    if (isPro) {
        state.activeMode = 'stamps';
        const builderTabBtn = document.querySelector('.nav-tab[data-tab="tab-builder"]');
        if(builderTabBtn) builderTabBtn.click();
    } else {
        const loyaltyTabBtn = document.querySelector('.nav-tab[data-tab="tab-loyalty"]');
        if(loyaltyTabBtn) loyaltyTabBtn.click();
    }"""

replacement_select = """window.selectCampaign = function(id) {
    state.currentCampaignId = id;
    
    // FUSION: Siempre mandamos al tab-builder (que ahora es el Creador Unificado) sin importar el plan
    const builderTabBtn = document.querySelector('.nav-tab[data-tab="tab-builder"]');
    if(builderTabBtn) {
        // We have to manually trigger the tab switch since the button is hidden
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-builder').classList.add('active');
        
        // Also highlight "Mis Campañas" in the sidebar so the user knows where they are
        const campBtn = document.querySelector('.nav-tab[data-tab="tab-campaigns"]');
        if(campBtn) campBtn.classList.add('active');
    }"""

js = js.replace(target_select, replacement_select)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
