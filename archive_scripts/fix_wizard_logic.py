with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """window.createNewCampaign = function() {
    state.currentCampaignId = generateUUID();
    state.restaurantName = "Nueva Campaña";
    state.colorPrimary = "#000000";
    state.colorAccent = "#8b5cf6";
    if (typeof showToast === 'function') showToast("Nueva campaña creada, edita y guarda.", "info");
    
    // Redirect logic: Professionals skip Loyalty and go directly to Builder
    const isPro = (window.merchantData && window.merchantData.business_type === 'professional');
    if (isPro) {
        state.activeMode = 'stamps';
        const builderTabBtn = document.querySelector('.nav-tab[data-tab="tab-builder"]');
        if(builderTabBtn) builderTabBtn.click();
    } else {
        const loyaltyTabBtn = document.querySelector('.nav-tab[data-tab="tab-loyalty"]');
        if(loyaltyTabBtn) loyaltyTabBtn.click();
    }
    updatePassRender();
};"""

replacement = """window.createNewCampaign = function() {
    // En lugar de tirarlos directo a los settings, abrimos el Asistente Mágico
    const modal = document.getElementById('modal-quick-campaign');
    if(modal) {
        modal.style.display = 'flex';
        document.getElementById('quick-wizard-loading').style.display = 'none';
        
        // Asignar un ID nuevo temporalmente por si deciden avanzar
        state.currentCampaignId = generateUUID();
    }
};

window.applyQuickTemplate = function(type) {
    const loader = document.getElementById('quick-wizard-loading');
    if(loader) loader.style.display = 'block';

    setTimeout(() => {
        // Configuraciones mágicas pre-armadas basadas en la selección
        if(type === 'cafeteria') {
            state.restaurantName = "Cafetería / Restaurante";
            state.colorPrimary = "#451a03";
            state.colorAccent = "#d97706";
            state.iconClass = "fa-mug-hot";
            state.stampsReward = "¡Felicidades! Disfruta de un Café Gratis en esta visita.";
            state.dynamicDesc = "Acumula 10 visitas y llévate tu bebida favorita.";
            state.activeMode = 'stamps';
        } else if(type === 'salon') {
            state.restaurantName = "Salón de Belleza VIP";
            state.colorPrimary = "#831843";
            state.colorAccent = "#ec4899";
            state.iconClass = "fa-scissors";
            state.stampsReward = "¡Wow! Llegaste a la meta. Tienes un corte o secado gratis hoy.";
            state.dynamicDesc = "Cada visita cuenta. Premia tu belleza.";
            state.activeMode = 'stamps';
        } else if(type === 'clinica') {
            state.restaurantName = "Clínica Especializada";
            state.colorPrimary = "#064e3b";
            state.colorAccent = "#10b981";
            state.iconClass = "fa-stethoscope";
            state.stampsReward = "¡Gracias por tu lealtad! Tienes 50% de descuento en tu consulta de hoy.";
            state.dynamicDesc = "Cuidando de ti en cada visita.";
            state.activeMode = 'stamps';
        } else {
            // Desde Cero
            state.restaurantName = "Campaña Nueva";
            state.colorPrimary = "#000000";
            state.colorAccent = "#8b5cf6";
            state.iconClass = "fa-star";
            state.stampsReward = "Felicidades, ganaste un premio.";
            state.dynamicDesc = "Acumula sellos para ganar.";
        }

        // Aplicar a los inputs visuales si existen
        const catSelect = document.getElementById('business-category-select');
        if(catSelect) catSelect.value = type === 'custom' ? 'general' : (type === 'cafeteria' ? 'cafe' : type);
        
        // Trigger update functions
        if(typeof updatePassRender === 'function') updatePassRender();
        if(typeof saveDesignToSupabase === 'function') saveDesignToSupabase();
        
        // Cerrar modal
        const modal = document.getElementById('modal-quick-campaign');
        if(modal) modal.style.display = 'none';

        // Lanzar celebración
        if (typeof showToast === 'function') showToast("¡Magia lista! Tu campaña ha sido pre-configurada.", "success");
        
        // Redirigir al constructor visual para que la vean y hagan ajustes mínimos
        const isPro = (window.merchantData && window.merchantData.business_type === 'professional');
        if (isPro) {
            const builderTabBtn = document.querySelector('.nav-tab[data-tab="tab-builder"]');
            if(builderTabBtn) builderTabBtn.click();
        } else {
            const loyaltyTabBtn = document.querySelector('.nav-tab[data-tab="tab-loyalty"]');
            if(loyaltyTabBtn) loyaltyTabBtn.click();
        }

    }, 800); // Simulamos "creación con inteligencia"
};"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
