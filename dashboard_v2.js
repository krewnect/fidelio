window.saveDesignToSupabase = async function saveDesignToSupabase() {
    console.log("Global saveDesignToSupabase triggered!");
    if (!state.currentCampaignId) {
        console.log("Auto-generating new campaign ID");
        state.currentCampaignId = generateUUID();
    }
    
    const payload = {
        id: state.currentCampaignId,
        type: state.activeMode || "hybrid",
        name: state.restaurantName,
        description: state.dynamicDesc,
        color_primary: state.colorPrimary,
        color_accent: state.colorAccent,
        logo_url: state.customLogoUrl,
        banner_url: state.customBannerUrl,
        stamp_icon_url: state.iconClass,
        custom_cta_label: state.stampsReward,
        rules_config: {
            cashback_percent: state.cashbackPercent,
            stamps_total: state.stampsTotal,
            vip_tiers: state.vipTiers,
            show_appointment_btn: document.getElementById('builder-btn-appointment')?.value === 'yes',
            show_payment_btn: document.getElementById('builder-btn-payment')?.value === 'yes'
        }
    };

    try {
        const res = await fetch('/api/campaigns', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.merchantSession?.access_token || ''}`
            },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            console.log("Campaña guardada");
            if (typeof showToast === 'function') showToast("Campaña guardada ☁️", "success");
            await window.loadCampaigns();
        } else {
            console.error("Save Error:", await res.text());
            if (typeof showToast === 'function') showToast("Error al guardar campaña", "error");
        }
    } catch (ex) {
        console.error('Error de red saving campaign:', ex);
        if (typeof showToast === 'function') showToast('Error de conexión al guardar campaña', 'error');
    }
}

window.loadCampaigns = async function() {
    try {
        const res = await fetch('/api/campaigns', {
            headers: { 'Authorization': `Bearer ${window.merchantSession?.access_token || ''}` }
        });
        if (!res.ok) throw new Error("Failed to fetch");
        const data = await res.json();
        // Sort newest first
        if (data.campaigns && data.campaigns.length > 0) {
            data.campaigns.sort((a,b) => new Date(b.created_at) - new Date(a.created_at));
            if (!state.currentCampaignId) {
                // Initialize the designer with their newest campaign automatically
                state.currentCampaignId = data.campaigns[0].id;
                selectCampaign(data.campaigns[0].id, true);
            }
        }
        state.campaigns = data.campaigns;
        if (!window.state) window.state = {};
        window.state.campaigns = data.campaigns;
        const stripeSel = document.getElementById('stripe-campaign-select');
        if (stripeSel) {
            stripeSel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
            data.campaigns.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.name || c.type || 'Programa';
                stripeSel.appendChild(opt);
            });
        }
        const list = document.getElementById('campaigns-list');
        if (!list) return;
        
        list.innerHTML = data.campaigns
            .filter(c => !['membership', 'multipass', 'certificates'].includes(c.type))
            .map(c => `
            <div class="campaign-magic-card" style="position:relative; width: 100%; max-width: 340px; height: 180px; border-radius: 20px; cursor:pointer; perspective: 1000px; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);" onclick="openCampaignHub('${c.id}')">
                
                <!-- The actual card using strict Fidelio Brand Colors (no ugly user colors here) -->
                <div class="campaign-magic-inner" style="position:absolute; inset:0; border-radius: 20px; background: linear-gradient(135deg, #2a0845 0%, #6441A5 100%); box-shadow: 0 10px 30px -10px rgba(100, 65, 165, 0.5); overflow: hidden; transition: all 0.4s; display: flex; flex-direction: column;">
                    
                    <!-- Top section with Wallet shape notch -->
                    <div style="padding: 20px 24px; flex: 1; display:flex; flex-direction:column; justify-content:space-between; position:relative; z-index:2;">
                        
                        <!-- Header -->
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div style="width: 44px; height: 44px; background: rgba(255,255,255,0.15); border-radius: 12px; display:flex; align-items:center; justify-content:center; backdrop-filter: blur(10px); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.2);">
                                ${c.logo_url ? `<img src="${c.logo_url}" style="width:100%; height:100%; border-radius:12px; object-fit:cover;">` : `<i class="fa-solid ${c.stamp_icon_url || 'fa-star'}" style="font-size:20px; color:white;"></i>`}
                            </div>
                            
                            <!-- Pulse Live Indicator -->
                            <div style="display:flex; align-items:center; gap:6px; background:rgba(0,0,0,0.3); padding:4px 10px; border-radius:20px; backdrop-filter:blur(5px); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1);">
                                <div style="width:6px; height:6px; background:#10b981; border-radius:50%; box-shadow:0 0 10px #10b981; animation: pulseGlow 2s infinite;"></div>
                                <span style="color:white; font-size:10px; font-weight:800; letter-spacing:1px;">ACTIVA</span>
                            </div>
                        </div>
                        
                        <!-- Title -->
                        <div style="margin-top:auto;">
                            <h3 style="margin:0; font-size:22px; font-weight:800; letter-spacing:-0.5px; color:white; text-shadow: 0 2px 4px rgba(0,0,0,0.3); line-height:1.2;">${c.name || 'Sin Nombre'}</h3>
                            <p style="margin:4px 0 0; color:rgba(255,255,255,0.7); font-size:13px; font-weight:600; letter-spacing: 0.5px; text-transform: uppercase;"><i class="fa-solid fa-qrcode" style="margin-right:4px;"></i> ${c.type === 'stamps' ? 'Tarjeta de Sellos' : 'Wallet Digital'}</p>
                        </div>
                    </div>
                    
                    <!-- Decorative background shapes for that premium Apple Wallet feel -->
                    <div style="position:absolute; top:-20px; right:-20px; width:100px; height:100px; background:radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%); border-radius:50%;"></div>
                    <div style="position:absolute; bottom:-40px; left:-20px; width:150px; height:150px; background:radial-gradient(circle, rgba(0,0,0,0.2) 0%, transparent 70%); border-radius:50%;"></div>

                    <!-- Bottom Action Bar (slides up on hover) -->
                    <div class="campaign-magic-actions" style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 12px 20px; display:flex; justify-content:space-between; align-items:center; transform: translateY(100%); transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: absolute; bottom: 0; left: 0; width: 100%;">
                        <div style="color:#111827; font-size:13px; font-weight:800;"><i class="fa-solid fa-wand-magic-sparkles" style="color:#8b5cf6; margin-right:4px;"></i> Editar Diseño</div>
                        <button class="btn-delete-campaign" onclick="event.stopPropagation(); window.deleteCampaign('${c.id}')" style="background:rgba(239, 68, 68, 0.1); border:none; color:#ef4444; width:32px; height:32px; border-radius:8px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:all 0.2s;" onmouseover="this.style.background='#ef4444'; this.style.color='white';" onmouseout="this.style.background='rgba(239, 68, 68, 0.1)'; this.style.color='#ef4444';"><i class="fa-solid fa-trash"></i></button>
                    </div>
                </div>
            </div>
        `).join('');
        
        const specialList = document.getElementById('special-cards-list');
        if (specialList) {
            specialList.innerHTML = data.campaigns
                .filter(c => ['membership', 'multipass', 'certificates'].includes(c.type))
                .map(c => `
                <div class="metric-card" style="cursor:pointer; border: 1px solid var(--surface-light);" onclick="openCampaignHub('${c.id}')">
                    <div style="width: 100%; height: 100px; background: linear-gradient(135deg, ${c.color_primary||'#333'}, ${c.color_accent||'#666'}); border-radius: 8px 8px 0 0; margin-top:-20px; margin-left:-20px; margin-right:-20px; margin-bottom:15px; width:calc(100% + 40px);"></div>
                    <h3 style="margin-bottom:5px;">${c.name || 'Sin Nombre'}</h3>
                    <p style="color:var(--text-muted); font-size:0.9rem;">Tipo: ${c.type}</p>
                </div>
            `).join('');
        }
    } catch(e) {
        console.error("Error loading campaigns", e);
    }
};

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

window.createNewCampaign = function() {
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
        if(type === 'medico') {
            state.restaurantName = "Dr(a). Nombre / Especialidad";
            state.colorPrimary = "#134e4a";
            state.colorAccent = "#0d9488";
            state.iconClass = "fa-stethoscope";
            state.stampsReward = "¡Felicidades! Tienes 50% de Descuento en tu próxima consulta.";
            state.dynamicDesc = "Acumula tus visitas y cuida de tu salud.";
            state.activeMode = 'stamps';
            state.category = type;
        } else if(type === 'belleza') {
            state.restaurantName = "Nombre - Estilista/Barbero";
            state.colorPrimary = "#312e81";
            state.colorAccent = "#d946ef";
            state.iconClass = "fa-scissors";
            state.stampsReward = "¡Llegaste a la meta! Tienes un servicio de cortesía o Masaje Capilar.";
            state.dynamicDesc = "Cada visita cuenta. Premia tu estilo.";
            state.activeMode = 'stamps';
            state.category = type;
        } else if(type === 'clases') {
            state.restaurantName = "Coach / Instructor";
            state.colorPrimary = "#1e3a8a";
            state.colorAccent = "#3b82f6";
            state.iconClass = "fa-dumbbell";
            state.stampsReward = "¡Logrado! Te has ganado 1 Sesión de Entrenamiento Gratis.";
            state.dynamicDesc = "Acumula tus sesiones y alcanza tus metas.";
            state.activeMode = 'stamps';
            state.category = type;
        } else {
            // Desde Cero
            state.restaurantName = "Campaña Nueva";
            state.colorPrimary = "#000000";
            state.colorAccent = "#8b5cf6";
            state.iconClass = "fa-star";
            state.stampsReward = "Felicidades, ganaste un premio.";
            state.dynamicDesc = "Acumula sellos para ganar.";
            state.activeMode = 'stamps';
            state.category = type;
        }

        // Aplicar a los inputs visuales si existen
        const catSelect = document.getElementById('business-category-select');
        if(catSelect) catSelect.value = type === 'custom' ? 'general' : (type === 'cafeteria' ? 'cafe' : type);
        
        
        // DYNAMIC ICON DROPDOWN POPULATION
        const iconSelect = document.getElementById('rest-icon');
        if (iconSelect) {
            if (type === 'medico') {
                iconSelect.innerHTML = `
                    <option value="fa-heart-pulse">Corazón Médico</option>
                    <option value="fa-stethoscope">Estetoscopio</option>
                    <option value="fa-tooth">Diente (Dentista)</option>
                    <option value="fa-user-doctor">Doctor</option>
                    <option value="fa-eye">Ojo (Oftalmólogo)</option>
                    <option value="fa-bone">Hueso (Traumatólogo)</option>
                `;
                state.customBannerUrl = "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&q=80"; // Clean Medical Abstract
            } else if (type === 'belleza') {
                iconSelect.innerHTML = `
                    <option value="fa-scissors">Tijeras de Estilista</option>
                    <option value="fa-spa">Flor de Spa</option>
                    <option value="fa-spray-can">Spray de Cabello</option>
                    <option value="fa-gem">Diamante</option>
                    <option value="fa-eye">Pestañas / Belleza</option>
                `;
                state.customBannerUrl = "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800&q=80"; // Elegant Salon Abstract
            } else if (type === 'clases') {
                iconSelect.innerHTML = `
                    <option value="fa-dumbbell">Pesa / Gimnasio</option>
                    <option value="fa-person-running">Corredor</option>
                    <option value="fa-fire">Llama de Energía</option>
                    <option value="fa-paw">Huella (Paseador)</option>
                    <option value="fa-medal">Medalla</option>
                `;
                state.customBannerUrl = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&q=80"; // Dark Gym Abstract
            } else {
                iconSelect.innerHTML = `
                    <option value="fa-star">Estrella (General)</option>
                    <option value="fa-crown">Corona VIP</option>
                    <option value="fa-gift">Regalo</option>
                    <option value="fa-gem">Diamante</option>
                `;
                state.customBannerUrl = null; // Default
            }
            iconSelect.value = state.iconClass; // Set the default we picked earlier
        }

        const uniReward = document.getElementById('unified-reward');
        if(uniReward) uniReward.value = state.stampsReward;
        
        const uniDesc = document.getElementById('unified-desc');
        if(uniDesc) uniDesc.value = state.dynamicDesc;
        
        const restName = document.getElementById('rest-name');
        if(restName) restName.value = state.restaurantName;
        
        // Trigger update functions
        if(typeof updatePassRender === 'function') updatePassRender();
        if(typeof saveDesignToSupabase === 'function') saveDesignToSupabase();
        
        // Cerrar modal
        const modal = document.getElementById('modal-quick-campaign');
        if(modal) modal.style.display = 'none';

        // Lanzar celebración
        if (typeof showToast === 'function') showToast("¡Magia lista! Tu campaña ha sido pre-configurada.", "success");
        
        // Redirigir al constructor visual para que la vean y hagan ajustes mínimos
    // FUSION ROUTING
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
    
    const builderTab = document.getElementById('tab-builder');
    if(builderTab) builderTab.classList.add('active');
    
    const campBtn = document.querySelector('.nav-tab[data-tab="tab-campaigns"]');
    if(campBtn) campBtn.classList.add('active');


    }, 800); // Simulamos "creación con inteligencia"
};

window.createNewSpecialCard = function() {
    state.currentCampaignId = generateUUID();
    state.restaurantName = "Nueva Tarjeta Especial";
    state.colorPrimary = "#10b981";
    state.colorAccent = "#8b5cf6";
    state.activeMode = "membership"; // default
    if (typeof showToast === 'function') showToast("Nueva tarjeta creada, edita y guarda.", "info");
    
    const specialTabBtn = document.querySelector('.nav-tab[data-tab="tab-special-cards"]');
    if(specialTabBtn) specialTabBtn.click();
    
    updatePassRender();
};

window.deleteCampaign = async function(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar esta campaña? Esta acción no se puede deshacer.')) return;
    try {
        const res = await fetch('/api/campaigns/' + id, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${window.merchantSession?.access_token || ''}` }
        });
        if (!res.ok) throw new Error('Error al eliminar');
        showToast('Campaña eliminada', 'success');
        window.loadCampaigns();
    } catch (e) {
        showToast(e.message, 'error');
    }
};

window.selectCampaign = async function(id, autoInit = false) {
    try {
        const res = await fetch('/api/campaigns', {
            headers: { 'Authorization': `Bearer ${window.merchantSession?.access_token || ''}` }
        });
        const data = await res.json();
        const camp = data.campaigns.find(c => c.id === id);
        if (!camp) return;

        state.currentCampaignId = camp.id;
        
        // Force stamps for professionals
        if (window.merchantData && window.merchantData.business_type === 'professional') {
            const pType = document.getElementById('program-type-select');
            if (pType) pType.value = 'stamps';
            state.activeMode = 'stamps';
        }
        
        state.restaurantName = camp.name || "Campaña";
        state.dynamicDesc = camp.description || "";
        state.colorPrimary = camp.color_primary || "#000";
        state.colorAccent = camp.color_accent || "#8b5cf6";
        state.customLogoUrl = camp.logo_url || null;
        state.customBannerUrl = camp.banner_url || null;
        if(state.customBannerUrl && state.customBannerUrl.includes('stripe.com')) {
            const linkInput = document.getElementById('stripe-payment-link');
            if(linkInput) linkInput.value = state.customBannerUrl;
        }
        state.iconClass = camp.stamp_icon_url || "fa-burger";
        state.stampsReward = camp.custom_cta_label || "Premio";
        state.activeMode = camp.type || "hybrid";
        const btnRemoveStamp = document.getElementById('btn-remove-stamp');
        if (state.iconClass && state.iconClass.startsWith('data:image')) {
            if (btnRemoveStamp) btnRemoveStamp.style.display = 'inline-block';
        } else {
            if (btnRemoveStamp) btnRemoveStamp.style.display = 'none';
        }

        
        if (camp.rules_config) {
            state.cashbackPercent = camp.rules_config.cashback_percent || 10;
            state.stampsTotal = camp.rules_config.stamps_total || 10;
            if (camp.rules_config.vip_tiers) state.vipTiers = camp.rules_config.vip_tiers;
        }

        // Fill inputs
        const safeVal = (eid, val) => { const e = document.getElementById(eid); if(e) e.value = val; };
        safeVal('rest-name', state.restaurantName);
        safeVal('color-primary', state.colorPrimary);
        safeVal('color-accent', state.colorAccent);
        safeVal('rest-icon', state.iconClass);
        safeVal('stamps-reward', state.stampsReward);
        safeVal('dynamic-desc', state.dynamicDesc);

        // FUSION ROUTING: Manual Tab Switch because button is hidden
        if (!autoInit) {
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
            
            const builderTab = document.getElementById('tab-builder');
            if(builderTab) builderTab.classList.add('active');
            
            const campBtn = document.querySelector('.nav-tab[data-tab="tab-campaigns"]');
            if(campBtn) campBtn.classList.add('active');
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            // Close hub modal if open
            const hub = document.getElementById('modal-campaign-hub');
            if(hub) hub.style.display = 'none';
        }
        
        updatePassRender();
        if (typeof showToast === 'function') showToast("Campaña cargada en el editor", "success");
    } catch(e) {
        console.error("Error selecting campaign", e);
    }
};

window.saveStripeKeys = async function() {
    const linkInput = document.getElementById('stripe-payment-link');
    const campSelect = document.getElementById('stripe-campaign-select');
    
    const paymentLink = linkInput ? linkInput.value : '';
    const campId = campSelect ? campSelect.value : '';
    
    if (!campId) {
        if (typeof showToast === 'function') showToast("Debes seleccionar una tarjeta a monetizar", "warning");
        return;
    }
    
    if (!paymentLink || !paymentLink.includes('stripe.com')) {
        if (typeof showToast === 'function') showToast("Ingresa un Payment Link válido de Stripe", "warning");
        return;
    }
    
    const btn = event ? event.target.closest('button') : null;
    const originalText = btn ? btn.innerHTML : '';
    if(btn) btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Vinculando...';

    // Update campaign in Supabase
    try {
        const { error } = await window.supabaseClient
            .from('campaigns')
            .update({ stripe_payment_link: paymentLink })
            .eq('id', campId);
            
        if (error) throw error;
        
        if (typeof showToast === 'function') showToast("Checkout de Stripe vinculado exitosamente", "success");
        linkInput.value = ''; // clear
    } catch(err) {
        console.error("Error saving Stripe Link:", err);
        if (typeof showToast === 'function') showToast("Error al guardar enlace: " + err.message, "error");
    } finally {
        if(btn) btn.innerHTML = originalText;
    }
};

// POPULATE STRIPE CAMPAIGNS AND HANDLE PRO LOCK
window.initStripeUI = function() {
    const sel = document.getElementById('stripe-campaign-select');
    const lock = document.getElementById('stripe-pro-lock');
    const activeUI = document.getElementById('stripe-active-ui');
    
    let isPro = false;
    if (window.merchantData && (window.merchantData.business_type === 'professional' || window.merchantData.business_type === 'business' || window.merchantData.business_type === 'enterprise')) {
        isPro = true;
    }
    
    if (!isPro) {
        if(lock) lock.style.display = 'block';
        if(activeUI) activeUI.style.display = 'none';
        return;
    } else {
        if(lock) lock.style.display = 'none';
        if(activeUI) activeUI.style.display = 'block';
    }
    
    if (!sel) return;
    
    sel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
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
};

// Hook it into switchTab
const origSwitchTabForStripe = window.switchTab;
window.switchTab = function(tabId) {
    if (origSwitchTabForStripe) origSwitchTabForStripe(tabId);
    if (tabId === 'tab-builder' && window.populateBuilderCampaignSelect) {
        window.populateBuilderCampaignSelect();
    }
    if (tabId === 'tab-stripe' && window.initStripeUI) {
        window.initStripeUI();
    }
};


// --- FIDELIO UNIVERSAL BUSINESS ENGINE (FIDELITO SUPPORT ASSISTANT) --- //


        state = {
    team: [
        { id: 'usr-001', name: 'Master Admin', email: 'hola@fideliorewards.com', role: 'system', status: 'activo' },
        { id: 'usr-002', name: 'Caja Sucursal 1', email: 'caja1@fidelio.com', role: 'scanner', status: 'activo' }
    ]
};
let saveTimeout = null;

(async function initFidelio() {
    try {
        // Cargar datos reales
        await loadDataFromSupabase();
        await window.loadCampaigns();
    } catch (err) {
        console.error("Dashboard DB init error:", err);
        console.error('DB Init Error:', err.stack); if(typeof showToast==='function') showToast('Error inicializando datos', 'error');
    }

    // PRESETS DICTIONARY FOR MULTI-INDUSTRY GIROS
    const safeAdd = (id, evt, cb) => {
        const el = document.getElementById(id);
        if (el) el.addEventListener(evt, cb);
    };

    const categoryPresets = {
        restaurant: {
            label: "Restaurantes & Gastronomía",
            name: "Mi Negocio",
            color: "#090d16",
            accent: "#5b0eb8",
            icon: "fa-burger",
            reward: "Hamburguesa o Platillo Gratis",
            dynamic: "Martes y Jueves: Doble Cashback en Consumos",
            perkBronce: "Acumulación estándar del 5% de Cashback",
            perkPlata: "Postre de regalo en tu semana de cumpleaños",
            perkOro: "Mesa preferente sin filas + Bebida de cortesía"
        },
        cafe: {
            label: "Cafeterías & Panaderías",
            name: "Café Espresso & Pan",
            color: "#1c140d",
            accent: "#ec7e00",
            icon: "fa-mug-hot",
            reward: "Café Capuchino o Repostería Gratis",
            dynamic: "Mañanas 2x1 en Capuchinos de 8:00 AM a 11:00 AM",
            perkBronce: "Acumulación del 5% en tus cafés diarios",
            perkPlata: "Pan dulce de regalo en cada visita mayor a $150",
            perkOro: "Café de tamaño grande con upgrade sin costo"
        },
        barbershop: {
            label: "Barbershops & Barberías",
            name: "Barbería El Imperio",
            color: "#0d1117",
            accent: "#ec4899",
            icon: "fa-scissors",
            reward: "Corte de Barba o Cera de Peinado Gratis",
            dynamic: "Miércoles de Cerveza de Cortesía con tu Corte",
            perkBronce: "Acumulación del 5% de Cashback en servicios",
            perkPlata: "Bebida premium de cortesía en cada visita",
            perkOro: "Servicio de toalla caliente + Ritual de barba gratis"
        },
        nails: {
            label: "Salones de Uñas & Nails Studios",
            name: "Glamour Nails Studio",
            color: "#180c1e",
            accent: "#ec4899",
            icon: "fa-hand-sparkles",
            reward: "Esmaltado Gelish o Retoque Gratis",
            dynamic: "Jueves de 2x1 en Nail Art y Diseños Especiales",
            perkBronce: "Acumulación del 5% de Cashback en manicure",
            perkPlata: "Exfoliación de manos gratis en cada servicio",
            perkOro: "Cita prioritaria sin espera + Regalo de cumpleaños"
        },
        beauty: {
            label: "Salones de Belleza & Estéticas",
            name: "Belleza & Style House",
            color: "#160914",
            accent: "#a855f7",
            icon: "fa-wand-magic-sparkles",
            reward: "Tratamiento Capilar o Peinado Gratis",
            dynamic: "Lunes y Martes: 20% de Descuento en Tintes",
            perkBronce: "Acumulación del 5% de Cashback en belleza",
            perkPlata: "Ampolleta de hidratación capilar de regalo",
            perkOro: "Styling VIP personalizado + Descuento exclusivo"
        },
        arcade: {
            label: "Arcades, Bowling & Entretenimiento",
            name: "Pixel Arcade & Fun",
            color: "#061320",
            accent: "#06b6d4",
            icon: "fa-gamepad",
            reward: "Bolsa de 50 Fichas o Créditos Gratis",
            dynamic: "Viernes de Horas Mágicas: Doble Crédito en Recargas",
            perkBronce: "Acumulación del 5% de saldo para tus jugadas",
            perkPlata: "10 Fichas extra gratis en cada recarga de $200",
            perkOro: "Pase libre a zona VR + Fichas ilimitadas en tu cumple"
        },
        retail: {
            label: "Tiendas de Ropa & Retail",
            name: "Boutique Urbana",
            color: "#12141d",
            accent: "#00a87e",
            icon: "fa-bag-shopping",
            reward: "Cuponera de $250 MXN o Accesorio Gratis",
            dynamic: "Viernes de Ventas Privadas: 15% Cashback Extra",
            perkBronce: "Acumulación del 5% de Cashback en ropa",
            perkPlata: "Acceso anticipado a colecciones de temporada",
            perkOro: "Asesoría de imagen personal + Ajustes gratis"
        },
        icecream: {
            label: "Heladerías & Postres",
            name: "Nieve & Waffle Gourmet",
            color: "#190e15",
            accent: "#ec4899",
            icon: "fa-ice-cream",
            reward: "Cono Doble o Waffle Especial Gratis",
            dynamic: "Domingos Familiares: 3x2 en Conos y Nieve",
            perkBronce: "Acumulación del 5% de saldo dulce",
            perkPlata: "Toppings ilimitados de regalo en tu helado",
            perkOro: "Malteada grande gratis en tu mes de cumpleaños"
        },
        spa: {
            label: "Spas & Salones de Masaje",
            name: "Lotus Spa & Wellness",
            color: "#081615",
            accent: "#00a87e",
            icon: "fa-spa",
            reward: "Masaje Facial de 30 Minutos Gratis",
            dynamic: "Miércoles de Relax: Aromaterapia de Cortesía",
            perkBronce: "Acumulación del 5% de Cashback en masajes",
            perkPlata: "Sesión de sauna de regalo en tus servicios",
            perkOro: "Upgrade de cabina VIP + Té de bienvenida"
        },
        fitness: {
            label: "Gimnasios & Studios de Fitness",
            name: "Titan Gym & Fitness",
            color: "#160b0b",
            accent: "#ea580c",
            icon: "fa-dumbbell",
            reward: "Pase VIP de 1 Semana para Acompañante",
            dynamic: "Reto del Mes: Completa 12 Visitas y Gana un Shaker",
            perkBronce: "Acumulación del 5% en tus mensualidades",
            perkPlata: "Medición de composición InBody sin costo",
            perkOro: "Sesión de entrenamiento personal 1-a-1 de regalo"
        },
        pets: {
            label: "Veterinarias & Pet Shops",
            name: "Pet Care & Vet",
            color: "#0a151b",
            accent: "#06b6d4",
            icon: "fa-paw",
            reward: "Baño Canino o Juguete Regalo Gratis",
            dynamic: "Jueves de Spa Mascota: Limpieza Dental Gratis",
            perkBronce: "Acumulación del 5% en alimento y estética",
            perkPlata: "Revisión médica veterinaria de regalo al año",
            perkOro: "Corte de uñas + Baño antipulgas cortesía"
        },
        general: {
            label: "Comercio / Servicios Generales",
            name: "Comercio Central",
            color: "#090d16",
            accent: "#5b0eb8",
            icon: "fa-store",
            reward: "Servicio o Producto de Regalo",
            dynamic: "Promoción Especial de Temporada Activa",
            perkBronce: "Acumulación estándar del 5% de Cashback",
            perkPlata: "Beneficio exclusivo de cliente frecuente",
            perkOro: "Atención VIP sin filas + Regalo de cortesía"
        }
    };

    
    // --- PRICING & FOUNDER LOGIC ---
    let isFounder = false;
    let isAnnual = false;
    let totalFoundersUsed = 0;

    async function checkPricingStatus() {
        if (!window.supabaseClient || !window.merchantSession) return;
        const merchantId = window.merchantSession.user.id;
        
        // 1. Get total merchants to determine founder meter
        const { count, error } = await window.supabaseClient
            .from('merchants')
            .select('*', { count: 'exact', head: true });
        
        totalFoundersUsed = count || 0;
        
        // 2. Check if current merchant is a founder. 
        // For simplicity: if they registered when there were <= 25 merchants, they are a founder.
        // We can approximate by checking their position.
        const { data: myRankData } = await window.supabaseClient
            .from('merchants')
            .select('created_at')
            .eq('id', merchantId)
            .single();
            
        if (myRankData) {
            const { count: myRank } = await window.supabaseClient
                .from('merchants')
                .select('*', { count: 'exact', head: true })
                .lte('created_at', myRankData.created_at);
            
            isFounder = (myRank <= 25);
        }

        updatePricingUI();
    }

    function updatePricingUI() {
        const toggle = document.getElementById('billing-cycle-toggle');
        if (toggle) isAnnual = toggle.checked;

        // Meter UI
        const meter = document.getElementById('founder-meter-text');
        if (meter) {
            const left = Math.max(0, 25 - totalFoundersUsed);
            meter.innerHTML = `<i class="fa-solid fa-fire"></i> ${left} / 25 Disponibles`;
            if (left === 0) meter.style.color = 'var(--text-muted)';
        }

        const badge = document.getElementById('pricing-tier-badge');
        const amt = document.getElementById('pricing-amount');
        const period = document.getElementById('pricing-period');
        const desc = document.getElementById('pricing-description');
        
        const hasCustomPrice = window.merchantData && window.merchantData.custom_price !== null && window.merchantData.custom_price !== undefined;

        if (hasCustomPrice) {
            if (badge) {
                badge.style.background = 'linear-gradient(135deg, #10B981 0%, #059669 100%)';
                badge.style.color = 'white';
                badge.innerHTML = 'TARIFA PREFERENCIAL';
            }
            if (amt) amt.textContent = window.merchantData.custom_price.toLocaleString();
            if (desc) desc.textContent = 'Precio especial asignado. Sucursales ilimitadas.';
            if (period) period.textContent = 'mes';
            
            const toggleCycle = document.getElementById('billing-cycle-toggle');
            if (toggleCycle) {
                toggleCycle.disabled = true;
                toggleCycle.parentElement.style.opacity = '0.5';
            }
        }
        else if (isFounder) {
            if (badge) {
                badge.style.background = 'linear-gradient(135deg, #FFD700 0%, #FDB931 100%)';
                badge.innerHTML = 'LICENCIA FOUNDER (DE POR VIDA)';
            }
            if (amt) amt.textContent = isAnnual ? '9,999' : '999';
            if (desc) desc.textContent = 'Sucursales ilimitadas. Soporte VIP.';
        } else {
            if (badge) {
                badge.style.background = 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)';
                badge.style.color = 'white';
                badge.innerHTML = 'LICENCIA ESTÁNDAR';
            }
            if (amt) amt.textContent = isAnnual ? '19,999' : '1,999';
            if (desc) desc.textContent = 'Hasta 20 sucursales. $99 MXN por extra.';
        }

        if (period) period.textContent = isAnnual ? 'año' : 'mes';
    }

    // Bind toggle
    const toggleCycle = document.getElementById('billing-cycle-toggle');
    const labelMo = document.getElementById('label-monthly');
    const labelYr = document.getElementById('label-annual');
    if (toggleCycle) {
        toggleCycle.addEventListener('change', () => {
            if (labelMo) labelMo.style.color = toggleCycle.checked ? 'var(--text-muted)' : 'var(--text-main)';
            if (labelYr) labelYr.style.color = toggleCycle.checked ? 'var(--text-main)' : 'var(--text-muted)';
            updatePricingUI();
        });
        if (labelMo) labelMo.addEventListener('click', () => { toggleCycle.checked = false; toggleCycle.dispatchEvent(new Event('change')); });
        if (labelYr) labelYr.addEventListener('click', () => { toggleCycle.checked = true; toggleCycle.dispatchEvent(new Event('change')); });
    }

    // --- DATABASE SYNC ---


    async function loadDataFromSupabase() {
        if (!window.supabaseClient || !window.merchantSession) return false;
        const merchantId = window.merchantSession.user.id;

        let { data: merchantData, error } = await window.supabaseClient
            .from('merchants')
            .select('*')
            .eq('id', merchantId)
            .single();

        if (error) {
            console.log("El perfil del merchant no existe. Creando perfil por defecto...");
            
            // Auto-create merchant profile if it doesn't exist
            const { data: newMerchant, error: insertError } = await window.supabaseClient
                .from('merchants')
                .insert([{
                    id: merchantId,
                    business_name: "Mi Negocio",
                    industry: "restaurant",
                    color_primary: "#090d16",
                    color_accent: "#5b0eb8",
                    cashback_percent: 5,
                    stamps_total: 10,
                    stamps_reward_text: "Recompensa Gratis",
                    branches: []
                }])
                .select('*')
                .single();
                
            if (insertError) {
                console.error("No se pudo auto-crear el merchant:", insertError);
                console.error('CRASH FATAL: No tenant profile.'); if(typeof showToast==='function') showToast('Error crítico: Cuenta sin perfil de negocio. Contacta a soporte.', 'error');
                return false;
            }
            merchantData = newMerchant;
        }

        window.merchantData = merchantData;
        // Trigger UI update for landing link explicitly when data loads
        if (typeof window.updateLandingUI === 'function') window.updateLandingUI();
        let custQuery = window.supabaseClient.from('customers').select('*');
        if (window.merchantSession.user.email !== 'hola@fideliorewards.com') {
            custQuery = custQuery.eq('merchant_id', merchantId);
        }
        const { data: custData } = await custQuery;

        const { data: transData } = await window.supabaseClient
            .from('transactions')
            .select('*')
            .eq('merchant_id', merchantId);
            
        let appQuery = window.supabaseClient.from('appointments').select('*').order('appointment_date', { ascending: true });
        if (window.merchantSession.user.email !== 'hola@fideliorewards.com') {
            appQuery = appQuery.eq('merchant_id', merchantId);
        }
        const { data: appointmentsData } = await appQuery;
        
        window.checkPlanPermissions = function() {
            if (!window.merchantData) return;
            const plan = window.merchantData.business_type || 'starter';
            const isAdmin = window.merchantSession && window.merchantSession.user && window.merchantSession.user.email === 'hola@fideliorewards.com';
            
            // Professional is the most limited, Business has almost everything
            const isBusiness = plan === 'business' || plan === 'enterprise' || isAdmin;
            const isPro = plan === 'business' || plan === 'enterprise' || isAdmin;
            
            // Toggle Business-only tabs
            document.querySelectorAll('.plan-business-only').forEach(el => {
                if(isBusiness) {
                    el.style.display = 'flex';
                } else {
                    el.style.display = 'none';
                }
            });
            
            // Hide Fidelizacion tab for non-business (professionals)
            const navLoyalty = document.getElementById('nav-loyalty');
            if (navLoyalty) {
                if (isBusiness) {
                    navLoyalty.style.display = 'block';
                } else {
                    navLoyalty.style.display = 'none';
                }
            }
            
            if (!isBusiness) {
                const stampsRadio = document.querySelector('input[name="loyalty_mode"][value="stamps"]');
                if (stampsRadio && !stampsRadio.checked) {
                    stampsRadio.checked = true;
                    setTimeout(() => stampsRadio.dispatchEvent(new Event('change', {bubbles: true})), 100);
                }
                
                const progSelect = document.getElementById('program-type-select');
                if (progSelect && progSelect.value === 'cashback') {
                    progSelect.value = 'stamps';
                    setTimeout(() => progSelect.dispatchEvent(new Event('change', {bubbles: true})), 100);
                }
            }

            // Toggle Pro-only tabs
            document.querySelectorAll('.plan-pro-only').forEach(el => {
                if(isPro) {
                    el.style.display = 'flex';
                } else {
                    el.style.display = 'none';
                }
            });
            
            // Toggle Professional-only tabs
            document.querySelectorAll('.plan-professional-only').forEach(el => {
                if(isBusiness && plan !== 'professional') {
                    el.style.display = 'none'; // Solo ocultar si es 100% negocio y NO profesional
                } else {
                    el.style.display = 'flex'; // Mostrar por defecto para professionals
                }
            });
        };
        
        window.checkPlanPermissions();

        document.getElementById('sub-status-text').innerHTML = merchantData.plan_status === 'active' ? '<i class="fa-solid fa-check-circle"></i> Activo' : '<i class="fa-solid fa-clock"></i> Pruebas / Inactivo';
        state = {
            tenantId: merchantData.id,
            restaurantName: merchantData.business_name || "Mi Negocio",
            category: merchantData.industry || "restaurant",
            colorPrimary: merchantData.color_primary || "#090d16",
            colorAccent: merchantData.color_accent || "#5b0eb8",
            iconClass: "fa-burger",
            customLogoUrl: merchantData.logo_url || null,
            customBannerUrl: merchantData.banner_url || null,
            activeMode: "hybrid",
            cashbackActive: true,
            cashbackPercent: merchantData.cashback_percent || 10,
            stampsActive: true,
            stampsTotal: merchantData.stamps_total || 5,
            stampsReward: merchantData.stamps_reward_text || "Premio Gratis",
            dynamicActive: true,
            dynamicDesc: "Promoción Activa",
            vipActive: true,
                        vipTiers: {
                bronce: { name: "Bronce", minSpent: 0, cashbackPercent: 5, perk: "Beneficio Base" },
                plata: { name: "Plata VIP", minSpent: 1000, cashbackPercent: 10, perk: "Beneficio Plata" },
                oro: { name: "Oro VIP", minSpent: 3000, cashbackPercent: 15, perk: "Beneficio Oro" }
            },
            branches: merchantData.branches || [],
            customers: custData || [],
            transactions: transData || [],
            appointments: appointmentsData || [],
            activeWallet: "apple"
        };
        
        // Restore schedules from DB
        try {
            if (merchantData.appointment_settings && merchantData.appointment_settings.schedules) {
                window.scheduleData = merchantData.appointment_settings.schedules;
            }
            if (typeof state !== 'undefined') state.schedules = window.scheduleData;
            if (window.state) window.state.schedules = window.scheduleData;
        } catch(e) { console.error("Error restoring schedules:", e); }

        // --- INJECT MERCHANT QR ---
        const prefs = window.merchantData.appointment_settings?.landing_prefs || {};
        const bName = window.merchantData.business_name || 'negocio';
        const username = prefs.username || window.merchantData.slug || bName.toLowerCase().replace(/[^a-z0-9]/g, '');
        const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=1000x1000&data=${encodeURIComponent(window.location.origin + '/' + username + '?v=3')}`;
        const qrPreview = document.getElementById('merchant-qr-preview');
        const btnDownloadQr = document.getElementById('btn-download-merchant-qr');
        
        if (qrPreview) {
            qrPreview.src = qrUrl;
        }
        
        if (btnDownloadQr) {
            btnDownloadQr.onclick = () => {
                const a = document.createElement('a');
                a.href = qrUrl;
                a.download = `QR_Mesa_${state.restaurantName}.png`;
                // qrserver doesn't set Content-Disposition by default, so we open it in new tab for mobile/desktop native download
                a.target = '_blank';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            };
        }
        
        if (merchantData.business_type === 'professional') {
            // Force mode to stamps
            const pSelect = document.getElementById('program-type-select');
            if (pSelect) {
                pSelect.value = 'stamps';
                pSelect.disabled = true;
                if (pSelect.parentElement) pSelect.parentElement.style.display = 'none'; // Hide the whole block
            }
            // Hide VIP toggle block
            const vipToggle = document.getElementById('toggle-vip');
            if (vipToggle && vipToggle.parentElement && vipToggle.parentElement.parentElement) {
                vipToggle.parentElement.parentElement.style.display = 'none';
            }
            // Force state
            state.activeMode = 'stamps';
            state.category = type;
            state.cashbackActive = false;
            state.vipActive = false;
        }

        return true;
    }

    function updateDashboardMetrics() {
        if (!state.customers || !state.transactions) return;

        // 1. Clientes Activos
        const totalCustomers = state.customers.length;
        document.getElementById('metric-customers').textContent = totalCustomers.toLocaleString();
        
        // Count in CRM badge as well
        const crmBadge = document.getElementById('crm-count-badge');
        if(crmBadge) crmBadge.textContent = totalCustomers;

        // 2. Pasivo (Cashback Disp.)
        const totalLiability = state.customers.reduce((sum, c) => sum + (c.current_balance || 0), 0);
        document.getElementById('metric-liability').textContent = `$${totalLiability.toLocaleString('es-MX', {minimumFractionDigits: 2})}`;

        // 3. Ventas Impulsadas (Suma de transacciones tipo 'earn')
        const totalSales = state.transactions
            .filter(t => t.type === 'earn')
            .reduce((sum, t) => sum + (t.amount || 0), 0);
        document.getElementById('metric-sales').textContent = `$${totalSales.toLocaleString('es-MX', {minimumFractionDigits: 2})}`;

        // 4. Escaneos Hoy (Transacciones en las últimas 24 horas)
        const now = new Date();
        const yesterday = new Date(now.getTime() - (24 * 60 * 60 * 1000));
        const scansToday = state.transactions.filter(t => new Date(t.created_at) >= yesterday).length;
        document.getElementById('metric-scans').textContent = scansToday.toLocaleString();
        
        // Citas Pendientes
        let processed = [];
        try { processed = window.merchantData.appointment_settings.processed_appointments || []; } catch(e){}
        const pendingCitas = state.transactions.filter(t => t.transaction_type === 'appointment_request' && !processed.includes(t.id)).length;
        const apptBadge = document.getElementById('appointments-count-badge');
        if (apptBadge) {
            if (pendingCitas > 0) {
                apptBadge.style.display = 'inline-block';
                apptBadge.textContent = pendingCitas;
            } else {
                apptBadge.style.display = 'none';
        // --- ADVANCED METRICS TAB ---
        
        // Base Lealtad
        const mAdvLoyalty = document.getElementById('metric-adv-loyalty');
        if(mAdvLoyalty) mAdvLoyalty.textContent = totalCustomers.toLocaleString();
        
        // Ticket Promedio
        const mAdvTicket = document.getElementById('metric-adv-ticket');
        if(mAdvTicket) {
            const earnTx = state.transactions.filter(t => t.type === 'earn');
            const avgTicket = earnTx.length > 0 ? (totalSales / earnTx.length) : 0;
            mAdvTicket.textContent = `$${avgTicket.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        }
        
        // Tasa Redención
        const mAdvRedemp = document.getElementById('metric-adv-redemption');
        if(mAdvRedemp) {
            const burnCount = state.transactions.filter(t => t.type === 'burn').length;
            const earnCount = state.transactions.filter(t => t.type === 'earn').length;
            const totalTx = state.transactions.filter(t => t.type === 'earn' || t.type === 'burn').length;
            const redempRate = totalTx > 0 ? Math.round((burnCount / totalTx) * 100) : 0;
            mAdvRedemp.textContent = `${redempRate}%`;
        }
        
        // Frecuencia
        const mAdvFreq = document.getElementById('metric-adv-freq');
        if(mAdvFreq) {
            const earnCount = state.transactions.filter(t => t.type === 'earn').length;
            const freq = totalCustomers > 0 ? (earnCount / totalCustomers) : 0;
            mAdvFreq.innerHTML = `${freq.toFixed(1)}x<span style="font-size:16px; color:var(--text-muted); font-weight:500;">/mes</span>`;
        }
        
        // Retorno de Inversión (ROI) Matemático
        const mRoi = document.getElementById('metric-roi');
        const mRoiRatio = document.getElementById('metric-roi-ratio');
        if(mRoi && mRoiRatio) {
            // Tabla de Precios Oficial (Mensual, Licencia Founder como baseline para calcular ROI mensual)
            // Professional: $199 (Founder) | $399 (Estandar)
            // Business: $999 (Founder) | $1999 (Estandar)
            // Calculamos asumiendo Licencia Founder Mensual para ser consistentes con los primeros clientes
            const fidelioCost = window.merchantData.tier === 'business' ? 999 : 199;
            
            if (totalSales === 0) {
                mRoi.textContent = '0%';
                mRoiRatio.textContent = '0.00';
            } else {
                const roiPercent = Math.round(((totalSales - fidelioCost) / fidelioCost) * 100);
                mRoi.textContent = (roiPercent > 0 ? '+' : '') + roiPercent + '%';
                
                const ratio = (totalSales / fidelioCost).toFixed(2);
                mRoiRatio.textContent = ratio;
            }
        }
        
        // Loyalty Revenue (ROI panel)
        const mLoyaltyRev = document.getElementById('metric-loyalty-revenue');
        if(mLoyaltyRev) {
            mLoyaltyRev.innerHTML = `+$${totalSales.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})} <span style="font-size:16px; font-weight:600; opacity:0.8; color:white;">MXN</span>`;
        }
        
        // LIVE ACTIVITY FEED
        const feedContainer = document.getElementById('live-activity-feed');
        if(feedContainer) {
            const recentTx = [...state.transactions].sort((a,b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 5);
            
            if(recentTx.length === 0) {
                feedContainer.innerHTML = `<div style='text-align: center; padding: 30px 10px; background: rgba(139,92,246,0.05); border-radius: 16px; border: 1px dashed rgba(139,92,246,0.2);'><div style='font-size:32px; margin-bottom:12px;'>👻</div><h4 style='margin:0 0 8px; font-size:15px; color:var(--text-main);'>Todo está muy tranquilo...</h4><p style='margin:0; font-size:12px; color:var(--text-muted);'>Aún no tienes actividad. ¡Anima a tus clientes a visitarte!</p></div>`;
            } else {
                feedContainer.innerHTML = '';
                recentTx.forEach(tx => {
                    const d = new Date(tx.created_at);
                    const isToday = d.toDateString() === new Date().toDateString();
                    const timeStr = isToday ? d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : d.toLocaleDateString();
                    
                    let icon = '<i class="fa-solid fa-qrcode"></i>';
                    let iconColor = 'var(--accent-violet)';
                    let iconBg = 'var(--bg-input)';
                    let desc = '';
                    
                    // Find customer
                    const c = state.customers.find(cus => cus.id === tx.customer_id);
                    const cName = c ? (c.first_name || 'Cliente') : 'Cliente';
                    
                    if(tx.type === 'earn') {
                        desc = `<strong>${cName}</strong> sumó puntos/cashback por compra de $${(tx.amount||0).toFixed(2)}`;
                    } else if(tx.type === 'burn') {
                        icon = '<i class="fa-solid fa-fire"></i>';
                        iconColor = '#F59E0B';
                        iconBg = 'rgba(245, 158, 11, 0.1)';
                        desc = `<strong>${cName}</strong> canjeó premio/saldo`;
                    } else if(tx.transaction_type === 'appointment_request') {
                        icon = '<i class="fa-regular fa-calendar"></i>';
                        iconColor = '#10b981';
                        iconBg = 'rgba(16, 185, 129, 0.1)';
                        desc = `<strong>${cName}</strong> solicitó una cita`;
                    } else {
                        desc = `<strong>${cName}</strong> registró actividad`;
                    }
                    
                    feedContainer.innerHTML += `
                    <div style="display:flex; align-items:center; gap:12px; font-size:13px; padding: 8px 0; border-bottom: 1px solid var(--border-soft);">
                        <div style="width:32px; height:32px; border-radius:50%; background:${iconBg}; color:${iconColor}; display:flex; align-items:center; justify-content:center; font-size:12px; flex-shrink: 0;">${icon}</div>
                        <div style="flex:1;">${desc}</div>
                        <div style="font-size:11px; color:var(--text-muted); white-space:nowrap;">${timeStr}</div>
                    </div>`;
                });
            }
        }

        // HEATMAP
        const heatmapGrid = document.getElementById('heatmap-grid');
        if(heatmapGrid) {
            const matrix = {
                12: [0,0,0,0,0,0,0], 14: [0,0,0,0,0,0,0], 18: [0,0,0,0,0,0,0], 20: [0,0,0,0,0,0,0]
            };
            
            let maxVal = 0;
            state.transactions.forEach(tx => {
                const d = new Date(tx.created_at);
                let day = d.getDay() - 1; // 0=Mon
                if(day === -1) day = 6;
                const h = d.getHours();
                
                let bucket = 12;
                if(h >= 13 && h < 17) bucket = 14;
                else if(h >= 17 && h < 20) bucket = 18;
                else if(h >= 20) bucket = 20;
                
                matrix[bucket][day]++;
                if(matrix[bucket][day] > maxVal) maxVal = matrix[bucket][day];
            });
            
            let hmHtml = `<div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; text-align:center; font-size:11px; font-weight:700; color:var(--text-muted); margin-bottom:8px;">
                <div></div><div>Lun</div><div>Mar</div><div>Mié</div><div>Jue</div><div>Vie</div><div>Sáb</div><div>Dom</div>
            </div>`;
            
            const labels = {12: '12 PM', 14: '2 PM', 18: '6 PM', 20: '8 PM'};
            [12, 14, 18, 20].forEach(bucket => {
                hmHtml += `<div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px; margin-bottom:4px;">
                    <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">${labels[bucket]}</div>`;
                for(let i=0; i<7; i++) {
                    const val = matrix[bucket][i];
                    const opacity = maxVal > 0 ? (val / maxVal) : 0;
                    hmHtml += `<div class="heatmap-cell" style="background: rgba(76,29,149,${Math.max(0.05, opacity)});" title="${val} visitas"></div>`;
                }
                hmHtml += `</div>`;
            });
            heatmapGrid.innerHTML = hmHtml;
        }

        // LEADERBOARD
        const lbContainer = document.getElementById('leaderboard-container');
        if(lbContainer) {
            const customerSpend = {};
            state.transactions.filter(t => t.type === 'earn').forEach(t => {
                if(!customerSpend[t.customer_id]) customerSpend[t.customer_id] = {id: t.customer_id, spend: 0, visits: 0};
                customerSpend[t.customer_id].spend += (t.amount || 0);
                customerSpend[t.customer_id].visits++;
            });
            
            const sorted = Object.values(customerSpend).sort((a,b) => b.spend - a.spend).slice(0,3);
            if(sorted.length === 0) {
                lbContainer.innerHTML = `<div style='text-align: center; padding: 20px 10px; background: rgba(59,130,246,0.05); border-radius: 16px; border: 1px dashed rgba(59,130,246,0.2);'><div style='font-size:28px; margin-bottom:8px;'>👑</div><p style='margin:0; font-size:12px; color:var(--text-muted);'>Acumula escaneos para ver a tus top fans aquí.</p></div>`;
            } else {
                lbContainer.innerHTML = '';
                const medals = ['#F59E0B', '#9CA3AF', '#D97706'];
                sorted.forEach((cus, idx) => {
                    const cInfo = state.customers.find(c => c.id === cus.id);
                    const name = cInfo ? `${cInfo.first_name || ''} ${cInfo.last_name || ''}`.trim() : 'Cliente Anónimo';
                    lbContainer.innerHTML += `
                    <div style="display:flex; align-items:center; justify-content:space-between; padding:12px; background:var(--bg-input); border-radius:12px; margin-bottom:8px;">
                        <div style="display:flex; align-items:center; gap:12px;">
                            <div style="width:28px; height:28px; border-radius:50%; background:rgba(245,158,11,0.1); color:${medals[idx] || '#10b981'}; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:800;">
                                ${idx+1}
                            </div>
                            <div style="font-weight:700; color:var(--text-main); font-size:14px;">${name}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-weight:800; color:var(--accent-violet);">$${cus.spend.toLocaleString('es-MX', {minimumFractionDigits:2})}</div>
                            <div style="font-size:10px; color:var(--text-muted);">${cus.visits} visitas</div>
                        </div>
                    </div>`;
                });
            }
        }
            }
        }
    }



    
window.updateUnifiedReward = function(val) {
    state.stampsReward = val;
    if (typeof updatePassRender === 'function') updatePassRender();
    scheduleAutoSave();
};

window.updateUnifiedDesc = function(val) {
    state.dynamicDesc = val;
    if (typeof updatePassRender === 'function') updatePassRender();
    scheduleAutoSave();
};

    function scheduleAutoSave() {
        if (saveTimeout) clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            saveDesignToSupabase();
        }, 1500);
    }

    // --- TOAST NOTIFICATIONS ---
    function showToast(message, type = "info") {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = 'toast-msg';
        
        let iconClass = 'fa-circle-info';
        if (type === 'success') iconClass = 'fa-circle-check text-emerald';
        if (type === 'warning') iconClass = 'fa-triangle-exclamation';
        if (type === 'error') iconClass = 'fa-circle-xmark';
        
        let errColor = type === 'error' ? 'color:#ef4444;' : '';
        let autoReportBtn = '';
        
        if (type === 'error') {
            const safeMsg = message.replace(/'/g, "\\'").replace(/"/g, '&quot;');
            autoReportBtn = `<button onclick="window.autoReportError('${safeMsg}', this)" style="margin-left:12px; background:rgba(239, 68, 68, 0.1); color:#ef4444; border:1px solid rgba(239, 68, 68, 0.3); border-radius:6px; padding:4px 8px; font-size:10px; cursor:pointer; font-weight:bold; white-space:nowrap; transition:all 0.2s;">Reportar Problema</button>`;
        }

        toast.innerHTML = `<i class="fa-solid ${iconClass}" style="${errColor}"></i> <span style="flex:1;">${message}</span> ${autoReportBtn}`;
        container.appendChild(toast);

        const delay = type === 'error' ? 10000 : 4000; // Give 10 seconds for errors so they can click report
        setTimeout(() => {
            if(toast) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => toast.remove(), 300);
            }
        }, delay);
    }
    window.showToast = showToast;

    // --- 1-CLICK INTUITIVE PRESET LOAD FUNCTION ---
    window.loadDemoPreset = async function(presetKey) {
        const preset = categoryPresets[presetKey] || categoryPresets.general;
        const categorySel = document.getElementById('business-category-select');
        if (categorySel) categorySel.value = presetKey;

        state.category = presetKey;
        state.restaurantName = preset.name;
        state.colorPrimary = preset.color;
        state.colorAccent = preset.accent;
        state.iconClass = preset.icon;
        state.stampsReward = preset.reward;
        state.dynamicDesc = preset.dynamic;
        
        scheduleAutoSave();

        document.getElementById('rest-name').value = preset.name;
        document.getElementById('color-primary').value = preset.color;
        document.getElementById('color-accent').value = preset.accent;
        document.getElementById('rest-icon').value = preset.icon;
        document.getElementById('stamps-reward').value = preset.reward;
        document.getElementById('dynamic-desc').value = preset.dynamic;
        document.getElementById('tier-bronce-perk').value = preset.perkBronce;
        document.getElementById('tier-plata-perk').value = preset.perkPlata;
        document.getElementById('tier-oro-perk').value = preset.perkOro;

        document.getElementById('header-restaurant-name').textContent = preset.name;
        document.getElementById('header-business-category').textContent = preset.label;
        if(document.getElementById('metrics-cards-issued')) document.getElementById('metrics-cards-issued').textContent = custData.length;

        updatePassRender();

        showToast(`Plantilla cargada en Fidelio: ${preset.name} (${preset.label}).`, "success");
    };

    // --- CATEGORY CHANGE HANDLER (DYNAMIC GIRO ADAPTATION) ---
    const categorySelect = document.getElementById('business-category-select');
    if (categorySelect) {
        categorySelect.addEventListener('change', (e) => {
            window.loadDemoPreset(e.target.value);
        });
    }

    // --- DEMO METALLIC TIER CONTORNO SELECTOR ---
    window.setDemoTier = function(tier) {
        const sampleClient = state.customers[0];
        if (sampleClient) {
            const tierConfig = state.vipTiers[tier];
            sampleClient.tier = tierConfig ? tierConfig.name : (tier === 'oro' ? 'Oro VIP' : tier === 'plata' ? 'Plata VIP' : 'Bronce');
            updatePassRender();

            showToast(`Vista previa del pase actualizada a: ${sampleClient.tier}`, "info");
        }
    };

    // --- BIND CONFIGURABLE VIP TIER INPUTS ---
    const bindVipTierInputs = () => {
        safeAdd('tier-bronce-name', 'input', (e) => {
            state.vipTiers.bronce.name = e.target.value; updatePassRender();

        });
        safeAdd('tier-bronce-cb', 'input', (e) => {
            state.vipTiers.bronce.cashbackPercent = parseFloat(e.target.value) || 5; updatePassRender();

        });
        safeAdd('tier-plata-name', 'input', (e) => {
            state.vipTiers.plata.name = e.target.value; updatePassRender();

        });
        safeAdd('tier-plata-cb', 'input', (e) => {
            state.vipTiers.plata.cashbackPercent = parseFloat(e.target.value) || 10; updatePassRender();

        });
        safeAdd('tier-oro-name', 'input', (e) => {
            state.vipTiers.oro.name = e.target.value; updatePassRender();

        });
        safeAdd('tier-oro-cb', 'input', (e) => {
            state.vipTiers.oro.cashbackPercent = parseFloat(e.target.value) || 15; updatePassRender();

        });
    };

    bindVipTierInputs();

    // --- FIDELITO SUPPORT CHATBOT ASSISTANT ---
    const chatHistory = document.getElementById('ai-chat-history');
    const chatInput = document.getElementById('ai-chat-input');
    const btnSendChat = document.getElementById('btn-send-ai-chat');

    function sendAiChatMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        const userMsg = document.createElement('div');
        userMsg.className = 'chat-msg user';
        userMsg.innerHTML = `<i class="fa-solid fa-user"></i><div><strong>Tú</strong><p>${text}</p></div>`;
        chatHistory.appendChild(userMsg);

        chatInput.value = '';
        chatHistory.scrollTop = chatHistory.scrollHeight;

        setTimeout(() => {
            let aiReply = "¡Hola! Soy Fidelito, tu asistente de soporte de Fidelio. Fidelio es 100% intuitivo. Puedes usar las plantillas rápidas en la parte superior para configurar tu tipo de negocio en 1 clic. ¿Deseas ayuda con las 20 sucursales o con el escáner del mesero?";
            const lower = text.toLowerCase();

            if (lower.includes("plantilla") || lower.includes("demo") || lower.includes("intuitiv")) {
                aiReply = "Soy Fidelito. Puedes hacer clic en las plantillas rápidas arriba del diseñador para ver cómo se adapta la tarjeta Fidelio al instante para Restaurantes, Barberías, Salones de Uñas, Cafeterías y Arcades.";
            } else if (lower.includes("precio") || lower.includes("costo") || lower.includes("999")) {
                aiReply = "La suscripción de Fidelio tiene un costo fijo de $999 MXN/mes por negocio e incluye hasta 20 sucursales con geofencing GPS y las 4 mecánicas de fidelización integradas.";
            }

            const botMsg = document.createElement('div');
            botMsg.className = 'chat-msg bot';
            botMsg.innerHTML = `<img src="fidelio_logo.jpg" alt="Fidelito Avatar" class="fidelito-avatar-img"><div><strong>Fidelito (Asistente de Soporte)</strong><p>${aiReply}</p></div>`;
            chatHistory.appendChild(botMsg);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }, 800);
    }

    if (btnSendChat) {
        btnSendChat.addEventListener('click', sendAiChatMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendAiChatMessage();
        });
    }

    // --- EMAIL SUPPORT TICKET ---
    const btnSendEmailTicket = document.getElementById('btn-send-email-ticket');
    if (btnSendEmailTicket) {
        btnSendEmailTicket.addEventListener('click', () => {
            const subject = document.getElementById('ticket-subject').value;
            const desc = document.getElementById('ticket-desc').value;

            if (!subject || !desc) {
                showToast("Por favor llena el asunto y la descripción de tu correo.", "warning");
                return;
            }

            showToast("Ticket enviado a soporte@fidelio.app. Te responderemos por correo a la brevedad.", "success");
            document.getElementById('ticket-subject').value = '';
            document.getElementById('ticket-desc').value = '';
        });
    }

    // --- MODE TILES HANDLER ---
    const modeTiles = document.querySelectorAll('.mode-tile');
    modeTiles.forEach(tile => {
        tile.addEventListener('click', () => {
            modeTiles.forEach(c => c.classList.remove('active'));
            tile.classList.add('active');

            const mode = tile.getAttribute('data-mode');
            state.activeMode = mode;
            

            applyModeToParams(mode);
            updatePassRender();

            showToast(`Formato de Lealtad actualizado: ${tile.querySelector('strong').textContent}`, "info");
        });
    });

    function applyModeToParams(mode) {
        const checkCb = document.getElementById('mech-cashback-check');
        const checkSt = document.getElementById('mech-stamps-check');
        const checkDy = document.getElementById('mech-dynamic-check');
        const checkVip = document.getElementById('mech-vip-check');

        if (mode === 'cashback') {
            checkCb.checked = true; checkSt.checked = false; checkDy.checked = false; checkVip.checked = false;
        } else if (mode === 'stamps') {
            checkCb.checked = false; checkSt.checked = true; checkDy.checked = false; checkVip.checked = false;
        } else if (mode === 'dynamic') {
            checkCb.checked = false; checkSt.checked = false; checkDy.checked = true; checkVip.checked = false;
        } else if (mode === 'vip') {
            checkCb.checked = false; checkSt.checked = false; checkDy.checked = false; checkVip.checked = true;
        } else if (mode === 'hybrid') {
            checkCb.checked = true; checkSt.checked = true; checkDy.checked = true; checkVip.checked = true;
        }

        state.cashbackActive = checkCb.checked;
        state.stampsActive = checkSt.checked;
        state.dynamicActive = checkDy.checked;
        state.vipActive = checkVip.checked;

        document.getElementById('mech-cashback-body').style.display = checkCb.checked ? 'block' : 'none';
        document.getElementById('mech-stamps-body').style.display = checkSt.checked ? 'block' : 'none';
        document.getElementById('mech-dynamic-body').style.display = checkDy.checked ? 'block' : 'none';
        document.getElementById('mech-vip-body').style.display = checkVip.checked ? 'block' : 'none';
    }

        // --- SUCURSALES (GPS & UPSELL) MANAGER ---
    const branchesContainer = document.getElementById('branches-list-container');
    const btnAddBranchModal = document.getElementById('btn-add-branch-modal');
    
    // Modals
    const modalAddBranch = document.getElementById('modal-add-branch');
    const modalUpsell = document.getElementById('modal-upsell-branches');
    
    // Form Inputs
    const bName = document.getElementById('branch-name');
    const bManager = document.getElementById('branch-manager');
    const bPhone = document.getElementById('branch-phone');
    const bMaps = document.getElementById('branch-maps-url');
    const bLat = document.getElementById('branch-lat');
    const bLng = document.getElementById('branch-lng');
    const bNotes = document.getElementById('branch-notes');
    const btnSubmitBranch = document.getElementById('btn-submit-branch');

    window.downloadBranchesLayout = function() {
        const headers = "Nombre Sucursal,Dirección,Teléfono\n";
        const sample1 = "Sucursal Centro,Av. Principal 123 Centro,5551234567\n";
        const sample2 = "Sucursal Norte,Plaza Norte Local 4,5559876543\n";
        
        const blob = new Blob([headers + sample1 + sample2], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", "Plantilla_Sucursales_Fidelio.csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    window.uploadBranchesCSV = async function(event) {
        if (!window.merchantSession) return showToast('Inicia sesión primero', 'error');
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = async function(e) {
            const text = e.target.result;
            const lines = text.split('\n').filter(line => line.trim() !== '');
            if (lines.length <= 1) {
                showToast('El archivo está vacío o solo tiene cabeceras.', 'warning');
                return;
            }

            const newBranches = [];
            // Skip header (i=1)
            for (let i = 1; i < lines.length; i++) {
                const row = lines[i].split(',');
                if (row.length >= 2) {
                    const name = row[0].trim();
                    const address = row[1].trim(); // Or manager if they put it there, but we map it to notes or manager later. Let's use it as address/notes.
                    const phone = row.length >= 3 ? row[2].trim() : '';

                    if (name) {
                        newBranches.push({
                            merchant_id: window.merchantSession.user.id,
                            name: name,
                            notes: address, // Store address in notes for now
                            phone: phone,
                            is_active: true
                        });
                    }
                }
            }

            if (newBranches.length === 0) return showToast('No se encontraron sucursales válidas.', 'warning');

            showToast(`Importando ${newBranches.length} sucursales...`, 'success');
            
            const { error } = await window.supabaseClient.from('merchant_branches').insert(newBranches);
            
            if (error) {
                showToast('Error al importar: ' + error.message, 'error');
            } else {
                showToast('¡Sucursales importadas correctamente!', 'success');
                // Refresh branches list
                const { data } = await window.supabaseClient.from('merchant_branches').select('*').eq('merchant_id', window.merchantSession.user.id);
                if (data) state.branches = data;
                renderBranches();
            }
        };
        reader.readAsText(file);
        event.target.value = ''; // Reset input
    };

    function renderAppointments() {
        const container = document.getElementById('appointments-list-container');
        if (!container) return;

        container.innerHTML = '';

        if (!state.appointments || state.appointments.length === 0) {
            container.innerHTML = `<p style="color:var(--text-muted); text-align:center; padding: 20px;"><i class="fa-solid fa-calendar-day"></i> Aún no tienes citas agendadas.</p>`;
            return;
        }

        let html = '';
        state.appointments.forEach(app => {
            const dateObj = new Date(app.appointment_date);
            const dateStr = dateObj.toLocaleDateString();
            const timeStr = dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const statusColor = app.status === 'pending' ? 'var(--warning)' : (app.status === 'confirmed' ? 'var(--success)' : 'var(--text-muted)');
            
            html += `
                <div style="background: var(--card-bg); border: 1px solid var(--border-soft); border-radius: 12px; padding: 16px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight: 700; font-size: 16px;">${app.customer_name}</div>
                        <div style="font-size: 13px; color: var(--text-muted); margin-top:4px;"><i class="fa-solid fa-envelope"></i> ${app.customer_email} ${app.customer_phone ? ' | <i class="fa-solid fa-phone"></i> ' + app.customer_phone : ''}</div>
                        <div style="font-size: 14px; margin-top: 8px; color:var(--text-main);"><i class="fa-regular fa-calendar"></i> ${dateStr} a las ${timeStr}</div>
                    </div>
                    <div style="text-align:right;">
                        <span style="display:inline-block; padding: 4px 12px; background: rgba(255,255,255,0.05); border: 1px solid ${statusColor}; color: ${statusColor}; border-radius: 20px; font-size: 12px; font-weight:700; margin-bottom: 8px;">
                            ${app.status ? app.status.toUpperCase() : 'PENDIENTE'}
                        </span>
                        <br>
                        <button class="btn-outline" style="padding: 6px 12px; font-size: 12px; margin-right:4px;" onclick="if(typeof showToast==='function') showToast('La funcionalidad de contacto directo llegará pronto', 'info');">Contactar</button>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    function renderBranches() {
        try {
            const dynBranchesContainer = document.getElementById('branches-list-container');
            const dynBtnAddBranchModal = document.getElementById('btn-add-branch-modal');
            
            if (!dynBranchesContainer) return;
            
            if (!state.branches || state.branches.length === 0) {
                dynBranchesContainer.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 20px;">No tienes sucursales registradas. Añade la primera.</p>';
            } else {
                dynBranchesContainer.innerHTML = '';
                state.branches.forEach((b, idx) => {
                    const div = document.createElement('div');
                    div.style.cssText = "background:white; border:1px solid rgba(0,0,0,0.05); border-radius:12px; padding:20px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 4px 10px rgba(0,0,0,0.02); transition:var(--transition);";
                    div.onmouseover = () => { div.style.borderColor = "rgba(139, 92, 246, 0.3)"; div.style.boxShadow = "0 10px 20px rgba(0,0,0,0.05)"; };
                    div.onmouseout = () => { div.style.borderColor = "rgba(0,0,0,0.05)"; div.style.boxShadow = "0 4px 10px rgba(0,0,0,0.02)"; };
                    
                    const latNum = parseFloat(b.lat);
                    const lngNum = parseFloat(b.lng);
                    const safeLat = isNaN(latNum) ? '0.0000' : latNum.toFixed(4);
                    const safeLng = isNaN(lngNum) ? '0.0000' : lngNum.toFixed(4);
                    
                    div.innerHTML = `
                        <div>
                            <h3 style="margin:0 0 4px 0; font-size:16px; font-weight:700; color:#111827;">${idx + 1}. ${b.name || 'Sucursal sin nombre'}</h3>
                            <div style="display:flex; gap:16px; font-size:13px; color:#6b7280; margin-bottom:8px;">
                                <span><i class="fa-solid fa-user"></i> ${b.manager || 'No asignado'}</span>
                                <span><i class="fa-solid fa-phone"></i> ${b.phone || 'Sin número'}</span>
                            </div>
                            <div style="font-size:12px; color:#9ca3af; display:flex; gap:16px;">
                                <span><i class="fa-solid fa-location-crosshairs"></i> GPS: ${safeLat}, ${safeLng} (Geofence 100m)</span>
                                ${b.mapsUrl ? `<a href="${b.mapsUrl}" target="_blank" style="color:var(--accent-violet); text-decoration:none; font-weight:600;"><i class="fa-solid fa-map"></i> Ver Maps</a>` : ''}
                            </div>
                        </div>
                        <button class="btn btn-outline" style="padding:8px 12px; border-radius:8px; color:#ef4444; border-color:#fee2e2;" onclick="removeBranch(${b.id})">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    `;
                    dynBranchesContainer.appendChild(div);
                });
            }
            
            // Update Add Button UI based on limit
            if (dynBtnAddBranchModal) {
                if (!window.isFounder && state.branches.length >= 20) {
                    dynBtnAddBranchModal.innerHTML = '<i class="fa-solid fa-crown"></i> Desbloquear Más Sucursales';
                    dynBtnAddBranchModal.style.background = 'linear-gradient(135deg, #1e1b4b 0%, #8b5cf6 100%)';
                    dynBtnAddBranchModal.style.border = 'none';
                    dynBtnAddBranchModal.style.color = 'white';
                } else {
                    dynBtnAddBranchModal.innerHTML = '<i class="fa-solid fa-plus"></i> Añadir Sucursal';
                    dynBtnAddBranchModal.style.background = 'var(--accent-violet)';
                    dynBtnAddBranchModal.style.border = 'none';
                    dynBtnAddBranchModal.style.color = 'white';
                }
            }
        } catch(e) {
            console.error("Error en renderBranches:", e);
        }
    }

    // BULLETPROOF EVENT DELEGATION DYNAMIC
    document.body.addEventListener('click', async (e) => {
        const btn = e.target.closest('#btn-add-branch-modal');
        if (btn) {
            e.preventDefault();
            console.log("Btn add branch clicked!");
            if (!state.branches) state.branches = [];
            
            if (!window.isFounder && state.branches.length >= 20) {
                const upsell = document.getElementById('modal-upsell-branches');
                if (upsell) upsell.style.display = 'flex';
            } else {
                const addModal = document.getElementById('modal-add-branch');
                if (addModal) addModal.style.display = 'flex';
                
                const dynName = document.getElementById('branch-name');
                const dynManager = document.getElementById('branch-manager');
                const dynPhone = document.getElementById('branch-phone');
                const dynMaps = document.getElementById('branch-maps-url');
                const dynLat = document.getElementById('branch-lat');
                const dynLng = document.getElementById('branch-lng');
                const dynNotes = document.getElementById('branch-notes');
                
                if (dynName) dynName.value = '';
                if (dynManager) dynManager.value = '';
                if (dynPhone) dynPhone.value = '';
                if (dynMaps) dynMaps.value = '';
                if (dynLat) dynLat.value = '';
                if (dynLng) dynLng.value = '';
                if (dynNotes) dynNotes.value = '';
            }
        }
    });
    
    // BULLETPROOF EVENT DELEGATION DYNAMIC FOR SUBMIT
    document.body.addEventListener('click', async (e) => {
        const btn = e.target.closest('#btn-submit-branch');
        if (btn) {
            e.preventDefault();
            console.log("Btn submit branch clicked!");
            const dynName = document.getElementById('branch-name');
            const dynManager = document.getElementById('branch-manager');
            const dynPhone = document.getElementById('branch-phone');
            const dynMaps = document.getElementById('branch-maps-url');
            const dynLat = document.getElementById('branch-lat');
            const dynLng = document.getElementById('branch-lng');
            const dynNotes = document.getElementById('branch-notes');
            const addModal = document.getElementById('modal-add-branch');
            
            if (!dynName.value || !dynLat.value || !dynLng.value) {
                showToast("El nombre y coordenadas son obligatorios", "warning");
                return;
            }
            
            const newBranch = {
                id: Date.now(),
                name: dynName.value,
                manager: dynManager ? dynManager.value : '',
                phone: dynPhone ? dynPhone.value : '',
                mapsUrl: dynMaps ? dynMaps.value : '',
                lat: parseFloat(dynLat.value),
                lng: parseFloat(dynLng.value),
                notes: dynNotes ? dynNotes.value : ''
            };
            
            if (!state.branches) state.branches = [];
            state.branches.push(newBranch);
            try {
                if (!state.tenantId) { if(typeof showToast==='function') showToast('Error interno: No se pudo identificar tu cuenta', 'error'); } else if (window.supabaseClient && state.tenantId) {
                    const { error } = await window.supabaseClient
                        .from('merchants')
                        .update({ branches: state.branches })
                        .eq('id', state.tenantId);
                    if (!error) {
                        console.log("Sucursal guardada en la base de datos."); showToast("Sucursal guardada exitosamente", "success");
                    } else {
                        if(typeof showToast==='function') showToast('Error de conexión: ' + error.message, 'error');
                    }
                }
            } catch (ex) {
                if(typeof showToast==='function') showToast('Error procesando solicitud: ' + ex.message, 'error');
            }
            
            if (addModal) addModal.style.display = 'none';
            renderBranches();
            showToast(`Sucursal "${newBranch.name}" agregada con éxito a la lista local. Recuerda darle a Guardar y Actualizar Tarjetas al final.`, "success");
        }
    });

    window.removeBranch = async function(id) {
        if(confirm("¿Estás seguro de eliminar esta sucursal de la red de Wallet?")) {
            state.branches = state.branches.filter(b => b.id !== id);
            
            renderBranches();
            try {
                if (!state.tenantId) { if(typeof showToast==='function') showToast('Error interno: No se pudo identificar tu cuenta', 'error'); } else if (window.supabaseClient && state.tenantId) {
                    const { error } = await window.supabaseClient
                        .from('merchants')
                        .update({ branches: state.branches })
                        .eq('id', state.tenantId);
                    if (!error) {
                        console.log("Sucursal guardada en la base de datos."); showToast("Sucursal guardada exitosamente", "success");
                    } else {
                        if(typeof showToast==='function') showToast('Error de conexión: ' + error.message, 'error');
                    }
                }
            } catch (ex) {
                if(typeof showToast==='function') showToast('Error procesando solicitud: ' + ex.message, 'error');
            }
            showToast("Sucursal eliminada. Los clientes ya no recibirán push en esta ubicación.", "info");
        }
    };// --- CUSTOMER ONBOARDING FORM MODAL ---
    const modalOnboarding = document.getElementById('modal-onboarding');
    const btnShowRegister = document.getElementById('btn-show-register-preview');
    const btnCloseOnboarding = document.getElementById('btn-close-onboarding');
    const btnSubmitRegister = document.getElementById('btn-submit-customer-register');

    if (btnShowRegister) {
        btnShowRegister.addEventListener('click', () => {
            modalOnboarding.classList.remove('hidden');
        });
    }

    if (btnCloseOnboarding) {
        btnCloseOnboarding.addEventListener('click', () => {
            modalOnboarding.classList.add('hidden');
        });
    }

    if (btnSubmitRegister) {
        btnSubmitRegister.addEventListener('click', async () => {
            const custName = document.getElementById('cust-name').value;
            const custPhone = document.getElementById('cust-phone').value;
            const custEmail = document.getElementById('cust-email').value;

            if (!custName || !custPhone) {
                if(typeof showToast==='function') showToast('Nombre y teléfono son obligatorios', 'warning');
                return;
            }

            btnSubmitRegister.textContent = 'Registrando...';
            btnSubmitRegister.disabled = true;

            try {
                const { data, error } = await window.supabaseClient
                    .from('customers')
                    .insert([{
                        merchant_id: window.merchantSession.user.id,
                        name: custName,
                        phone: custPhone,
                        email: custEmail,
                        current_balance: 0,
                        lifetime_value: 0,
                        visits: 0
                    }])
                    .select()
                    .single();

                if (error) throw error;

                state.customers.unshift(data);
                
                document.getElementById('modal-add-customer').classList.add('hidden');
                
                // Limpiar form
                document.getElementById('cust-name').value = '';
                document.getElementById('cust-phone').value = '';
                document.getElementById('cust-email').value = '';

                
renderCRMTable();
                updateDashboardMetrics(); // update stats
                
                showToast(`¡Cliente registrado! Código: ${data.id}`, "success");
            } catch (err) {
                if(typeof showToast==='function') showToast('Error registrando cliente: ' + err.message, 'error');
            } finally {
                btnSubmitRegister.textContent = 'Registrar Cliente';
                btnSubmitRegister.disabled = false;
            }
        });
    }
    
    const btnCloseCustomerModal = document.getElementById('btn-close-customer-modal');
    if (btnCloseCustomerModal) {
        btnCloseCustomerModal.addEventListener('click', () => {
            document.getElementById('modal-add-customer').classList.add('hidden');
        });
    }

    // Global function for QR
    window.showCustomerQR = function(customerId, customerName) {
        document.getElementById('qr-modal-name').textContent = customerName;
        document.getElementById('qr-modal-image').src = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${customerId}`;
        
        const btnGw = document.getElementById('btn-generate-gw');
        btnGw.onclick = async () => {
            const originalText = btnGw.innerHTML;
            btnGw.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Generando...';
            btnGw.disabled = true;

            try {
                const { data: { session } } = await supabase.auth.getSession();
                const res = await fetch('/api/wallet/google', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${session.access_token}`
                    },
                    body: JSON.stringify({ customerId })
                });

                const data = await res.json();
                if (!data.success) throw new Error(data.error || 'Error desconocido al generar Google Wallet');
                
                // Open the Google Pay Save URL
                window.open(data.saveUrl, '_blank');

            } catch (err) {
                if(typeof showToast==='function') showToast('Error: ' + err.message, 'error');
            } finally {
                btnGw.innerHTML = originalText;
                btnGw.disabled = false;
            }
        };

        const btnAw = document.getElementById('btn-generate-aw');
        btnAw.onclick = async () => {
            const originalText = btnAw.innerHTML;
            btnAw.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Generando...';
            btnAw.disabled = true;

            try {
                const { data: { session } } = await window.supabaseClient.auth.getSession();
                const res = await fetch('/api/wallet/apple', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${session.access_token}`
                    },
                    body: JSON.stringify({ customerId })
                });

                if (!res.ok) {
                    const errData = await res.json().catch(() => ({}));
                    throw new Error(errData.error || 'Error al generar Apple Wallet');
                }
                
                // It's a binary file download (.pkpass)
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${customerName.replace(/\\s+/g, '_')}_Lealtad.pkpass`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);

            } catch (err) {
                if(typeof showToast==='function') showToast('Error: ' + err.message, 'error');
            } finally {
                btnAw.innerHTML = originalText;
                btnAw.disabled = false;
            }
        };

        document.getElementById('modal-view-qr').classList.remove('hidden');
    };

    // --- CRM MODULE ---
    const crmTableBody = document.getElementById('crm-table-body');
    const crmSearchInput = document.getElementById('crm-search-input');
    const crmFilterTier = document.getElementById('crm-filter-tier');
    const crmFilterStatus = document.getElementById('crm-filter-status');
    const crmCountBadge = document.getElementById('crm-count-badge');

    
    // Listeners para CRM
    document.getElementById('crm-search-input')?.addEventListener('input', renderCRMTable);
    document.getElementById('crm-filter-tier')?.addEventListener('change', renderCRMTable);
    document.getElementById('crm-filter-status')?.addEventListener('change', renderCRMTable);
    document.getElementById('crm-filter-month')?.addEventListener('change', renderCRMTable);
    
function renderCRMTable() {
        const crmTableBody = document.getElementById('crm-table-body');
        const crmSearchInput = document.getElementById('crm-search-input');
        const crmFilterTier = document.getElementById('crm-filter-tier');
        const crmFilterStatus = document.getElementById('crm-filter-status');
        const crmFilterMonth = document.getElementById('crm-filter-month');
        const crmCountBadge = document.getElementById('crm-count-badge');
        
        if (!crmTableBody) return;

        const searchTerm = (crmSearchInput?.value || '').toLowerCase();
        const tierFilter = crmFilterTier?.value || 'all';
        const statusFilter = crmFilterStatus?.value || 'all';
        const monthFilter = crmFilterMonth?.value || 'all';
        
        const now = new Date();
        const currentMonth = String(now.getMonth() + 1).padStart(2, '0');

        let totalLTV = 0;
        let totalFreqDays = 0;
        let validFreqCount = 0;
        let churnRiskCount = 0;

        // PRE-PROCESS CUSTOMERS FOR METRICS
        const processedCustomers = state.customers.map(c => {
            const balance = c.current_balance || 0;
            const spent = parseFloat(c.lifetime_value || 0);
            totalLTV += spent;
            
            const tier = spent > 3000 ? 'Oro VIP' : (spent > 1000 ? 'Plata VIP' : 'Bronce VIP');
            
            const createdDate = new Date(c.created_at || now);
            const lastVisitDate = new Date(c.last_visit || c.created_at || now);
            const daysSinceRegistration = Math.max(1, Math.floor((now - createdDate) / (1000 * 60 * 60 * 24)));
            const daysSinceLastVisit = Math.floor((now - lastVisitDate) / (1000 * 60 * 60 * 24));
            
            const visits = parseInt(c.visits || 0);
            
            // Frequency calculation (days per visit)
            let freqDays = 0;
            let freqText = 'Nuevo';
            if (visits > 1) {
                freqDays = daysSinceRegistration / visits;
                freqText = `1 visita c/${Math.round(freqDays)} días`;
                totalFreqDays += freqDays;
                validFreqCount++;
            } else if (visits === 1) {
                freqText = '1 visita';
            }
            
            // Churn Risk (if they haven't visited in 2x their normal frequency, or > 60 days)
            let status = 'activo';
            let statusClass = 'activo';
            let statusText = 'Activo';
            
            if (visits === 0) {
                status = 'nuevo';
                statusClass = 'bronce';
                statusText = 'Nuevo';
            } else if (daysSinceLastVisit > 60 || (freqDays > 0 && daysSinceLastVisit > (freqDays * 2.5))) {
                status = 'riesgo';
                statusClass = 'riesgo';
                statusText = 'En Riesgo';
                churnRiskCount++;
            }
            
            // Birthday formatting
            let bdayFormatted = 'N/A';
            let bdayMonth = null;
            let isBirthdayMonth = false;
            if (c.birthday) {
                const bDate = new Date(c.birthday + 'T12:00:00Z'); // force midday to avoid timezone shift
                bdayFormatted = bDate.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
                bdayMonth = String(bDate.getMonth() + 1).padStart(2, '0');
                isBirthdayMonth = (bdayMonth === currentMonth);
            }
            
            // Anniversary
            const annivFormatted = createdDate.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' });
            const lastVisitFormatted = lastVisitDate.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });

            return {
                ...c,
                computed: {
                    balance, spent, tier, status, statusClass, statusText, freqText,
                    bdayFormatted, bdayMonth, isBirthdayMonth, annivFormatted, lastVisitFormatted, daysSinceLastVisit
                }
            };
        });

        // UPDATE KPI CARDS
        const kpiTotal = document.getElementById('kpi-total-customers');
        const kpiAvgSpent = document.getElementById('kpi-avg-spent');
        const kpiAvgFreq = document.getElementById('kpi-avg-freq');
        const kpiChurn = document.getElementById('kpi-churn-risk');
        
        if (kpiTotal) kpiTotal.textContent = state.customers.length;
        if (kpiAvgSpent) kpiAvgSpent.textContent = `$${state.customers.length ? (totalLTV / state.customers.length).toFixed(2) : 0} MXN`;
        if (kpiAvgFreq) kpiAvgFreq.textContent = validFreqCount ? `${Math.round(totalFreqDays / validFreqCount)} días` : 'N/A';
        if (kpiChurn) kpiChurn.textContent = churnRiskCount;

        // FILTER
        const filtered = processedCustomers.filter(c => {
            const matchesSearch = (c.full_name || c.name || '').toLowerCase().includes(searchTerm) || 
                                  (c.phone && c.phone.includes(searchTerm)) || 
                                  (c.email && c.email.toLowerCase().includes(searchTerm)) ||
                                  (c.id && c.id.toLowerCase().includes(searchTerm));
            
            const matchesTier = tierFilter === 'all' || c.computed.tier === tierFilter;
            const matchesStatus = statusFilter === 'all' || c.computed.status === statusFilter;
            const matchesMonth = monthFilter === 'all' || c.computed.bdayMonth === monthFilter;

            return matchesSearch && matchesTier && matchesStatus && matchesMonth;
        });

        if (crmCountBadge) crmCountBadge.textContent = filtered.length;
        crmTableBody.innerHTML = '';

        if (filtered.length === 0) {
            crmTableBody.innerHTML = `<tr><td colspan="9" style="text-align:center; color: var(--text-muted); padding: 30px;">No se encontraron registros de clientes.</td></tr>`;
            return;
        }
        filtered.forEach(c => {
            const tr = document.createElement('tr');
            const comp = c.computed;
            const tierClass = comp.tier.includes('Oro') ? 'oro' : comp.tier.includes('Plata') ? 'plata' : 'bronce';
            const bdayAlert = comp.isBirthdayMonth ? `<i class="fa-solid fa-cake-candles" style="color:var(--accent-violet); margin-right:4px;" title="¡Cumpleaños este mes!"></i>` : ``;
            
            // Determine active campaign logic to show appropriate stamps text
            let isStamps = false;
            let stampsGoal = 5;
            if (state.campaigns && state.campaigns.length > 0) {
                isStamps = state.campaigns[0].type === 'stamps';
                if (isStamps) stampsGoal = state.campaigns[0].stamps_goal || 5;
            }

            const phoneDigits = c.phone ? c.phone.replace(/\D/g, '') : '';
            const waAction = phoneDigits ? `window.open('https://wa.me/${phoneDigits}', '_blank')` : `if(typeof showToast==='function') showToast('El cliente no tiene un teléfono registrado', 'warning')`;
            const emailAction = c.email ? `window.open('mailto:${c.email}', '_self')` : `if(typeof showToast==='function') showToast('El cliente no tiene un correo registrado', 'warning')`;
            
            const avgSpend = c.visits && c.visits > 0 ? (comp.spent / c.visits) : 0;

            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${(c.full_name || c.name || '?').charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${c.full_name || c.name || 'Cliente sin nombre'}</strong>
                            <small style="display:block; color:var(--text-muted);">${c.id.substring(0,8)}...</small>
                        </div>
                    </div>
                </td>
                <td>
                    <strong>${c.phone || 'N/A'}</strong>
                    <small style="display:block; color:var(--text-muted);">${c.email || 'Sin correo'}</small>
                </td>
                <td><span class="tier-pill ${tierClass}">${comp.tier}</span></td>
                <td>
                    <strong style="color:#10b981; font-size:14px;">$${comp.balance.toFixed(2)} MXN</strong>
                    <small style="display:block; color:var(--text-muted);">Saldo actual</small>
                </td>
                <td>
                    <strong><i class="fa-solid fa-stamp" style="color:var(--accent-violet);"></i> ${c.visits || 0}/${stampsGoal}</strong>
                    <small style="display:block; color:var(--text-muted);">Visitas registradas</small>
                </td>
                <td>
                    <strong>${comp.lastVisitFormatted}</strong>
                    <small style="display:block; color:var(--text-muted);">${bdayAlert} Cumpleaños: ${comp.bdayFormatted}</small>
                </td>
                <td>
                    <strong style="color:var(--fidelio-violet);">${comp.freqText}</strong>
                    <small style="display:block; color:var(--text-muted);"><span class="badge-status ${comp.statusClass}" style="padding:2px 6px; font-size:9px;">${comp.statusText}</span></small>
                </td>
                <td><strong>$${comp.spent.toFixed(2)} MXN</strong></td>
                <td><strong>$${avgSpend.toFixed(2)} MXN</strong></td>
                <td>
                    <div style="display:flex; gap: 4px; justify-content: flex-end;">
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:#25D366; border-color:rgba(37, 211, 102, 0.2);" title="Enviar WhatsApp" onclick="${waAction}">
                            <i class="fa-brands fa-whatsapp"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:#3b82f6; border-color:rgba(59, 130, 246, 0.2);" title="Enviar Correo Electrónico" onclick="${emailAction}">
                            <i class="fa-regular fa-envelope"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:var(--accent-violet); border-color:rgba(139, 92, 246, 0.2);" title="Enviar Notificación Push a Wallet" onclick="if(typeof Swal !== \'undefined\'){Swal.fire('Notificaciones Push','El envío de notificaciones directas al Apple Wallet/Google Wallet se habilitará cuando contrates un Add-on o subas de plan.','info');}else{if(typeof showToast==='function') showToast('El envío de notificaciones requiere un add-on adicional', 'info');}">
                            <i class="fa-regular fa-bell"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; margin-left:4px;" title="Ver Perfil Detallado" onclick="window.showCustomerProfile('${c.id}')">
                            <i class="fa-solid fa-qrcode"></i>
                        </button>
                    </div>
                </td>
            `;
            crmTableBody.appendChild(tr);
        });
    }

    // --- PASS RENDER FUNCTION WITH METALLIC BORDERS & DYNAMIC CONFIGURABLE TIERS ---
    const passRender = document.getElementById('pass-render');

        
    function renderTeamTable() {
        const tbody = document.getElementById('staff-table-body');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (!state.team || state.team.length === 0) {
            tbody.innerHTML = `<tr><td colspan='5' style='padding:40px; text-align:center;'><div style='display:inline-block; max-width:300px;'><div style='font-size:40px; margin-bottom:16px; color:#a78bfa;'><i class='fa-solid fa-users-viewfinder'></i></div><h4 style='margin:0 0 8px; font-size:18px;'>Tu equipo está vacío</h4><p style='color:var(--text-muted); font-size:14px; margin-bottom:16px;'>Invita a tus cajeros o meseros para que puedan dar puntos y cobrar sin que tú tengas que estar presente.</p></div></td></tr>`;
            return;
        }
        
        state.team.forEach(member => {
            const tr = document.createElement('tr');
            
            const roleBadge = member.role === 'system' 
                ? `<span class="badge-status activo" style="background: rgba(139, 92, 246, 0.1); color: var(--accent-violet); border-color: rgba(139, 92, 246, 0.3);"><i class="fa-solid fa-laptop-code"></i> Sistema</span>`
                : `<span class="badge-status" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.3);"><i class="fa-solid fa-mobile-screen"></i> Escáner</span>`;
                
            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${member.name.charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${member.name}</strong>
                            <small style="display:block; color:var(--text-muted);">ID: ${member.id}</small>
                        </div>
                    </div>
                </td>
                <td>
                    <strong>${member.email}</strong>
                </td>
                <td>${roleBadge}</td>
                <td><span class="badge-status activo">Activo</span></td>
                <td style="text-align:right;">
                    <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:#ef4444; border-color:rgba(239, 68, 68, 0.2);" title="Revocar Acceso" onclick="if(typeof showToast==='function') showToast('Función de revocación próxima a liberarse', 'info')">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }



function updatePassRender() {
        window._updatePassRenderGlobal = true; // Debug flag
        const passRender = document.getElementById('pass-render');
        if (!passRender) return;
        scheduleAutoSave();
        
        const pType = document.getElementById('program-type-select')?.value || 'cashback';
        const sTotal = parseInt(document.getElementById('stamps-total')?.value || '5', 10);
        
        const pName = document.getElementById('rest-name')?.value || state.restaurantName || "Mi Negocio";
        const catInput = document.getElementById('business-category-input');
        let pCat = "Mi Negocio / Especialidad";
        if (catInput) {
            pCat = catInput.value;
        } else {
            const oldCatSel = document.getElementById('business-category-select');
            if (oldCatSel) pCat = oldCatSel.options[oldCatSel.selectedIndex]?.text;
        }
        
        const pDesc = document.getElementById('rest-desc')?.value || state.dynamicDesc || "";
        const cPri = document.getElementById('color-primary')?.value || state.colorPrimary || "#1e1b4b";
        const cAcc = document.getElementById('color-accent')?.value || state.colorAccent || "#8b5cf6";
        const pIcon = document.getElementById('rest-icon')?.value || state.iconClass || "fa-crown";
        const pReward = document.getElementById('stamps-reward')?.value || state.stampsReward || "Bebida de Cortesía Gratis";
        const pPolicies = document.getElementById('pass-policies')?.value || "";
        const showAppt = document.getElementById('builder-btn-appointment')?.value === 'yes';
        const showPay = document.getElementById('builder-btn-payment')?.value === 'yes';

        const linksBack = document.getElementById('render-wallet-links-back');
        const linkAppt = document.getElementById('render-wallet-link-appointment');
        const linkPay = document.getElementById('render-wallet-link-payment');
        if (linksBack) {
            if (showAppt || showPay) {
                linksBack.style.display = 'block';
                if (linkAppt) linkAppt.style.display = showAppt ? 'flex' : 'none';
                if (linkPay) linkPay.style.display = showPay ? 'flex' : 'none';
            } else {
                linksBack.style.display = 'none';
            }
        }

        const rName = document.getElementById('render-name');
        const rCat = document.getElementById('render-category');
        const rDesc = document.getElementById('render-promo-text');
        const rIcon = document.getElementById('render-icon');
        const rReward = document.getElementById('render-reward-text');
        const rPolicies = document.getElementById('render-policies-text');
        const rFront = document.getElementById('pass-front-face');

        if (rName) rName.textContent = pName;
        if (rCat) rCat.textContent = pCat;
        if (rDesc) rDesc.textContent = pDesc;
        if (rReward) rReward.textContent = pReward;
        // Handle Custom Logo vs Icon
        const passLogoCircle = document.querySelector('.pass-logo-circle');
        if (passLogoCircle) {
            if (state.customLogoUrl) {
                passLogoCircle.innerHTML = `<img src="${state.customLogoUrl}" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">`;
            } else {
                passLogoCircle.innerHTML = `<i class="fa-solid ${pIcon}" id="render-icon"></i>`;
            }
        }
        
        // Handle custom border and primary color text
        passRender.style.setProperty('--pass-primary', cPri);
        
        const renderStampsBody = document.getElementById('render-body-stamps');
        const renderCashbackBody = document.getElementById('render-body-cashback');
        const renderStampsGrid = document.getElementById('render-stamps-grid');
        const renderStampsTotalText = document.getElementById('render-stamps-total-text');
        
        if (pType === 'stamps') {
            if(renderStampsBody) renderStampsBody.style.display = 'flex';
            if(renderCashbackBody) renderCashbackBody.style.display = 'none';
            
            // Dynamic Label
            let unitLabel = "SELLOS";
            if (state.category === 'medico') unitLabel = "CONSULTAS";
            if (state.category === 'belleza') unitLabel = "VISITAS";
            if (state.category === 'clases') unitLabel = "CLASES";
            if(renderStampsTotalText) renderStampsTotalText.textContent = sTotal + " " + unitLabel;
            
            // Generate Stamp Grid matching premium design
            if (renderStampsGrid) {
                let html = '<div style="position:absolute; top:50%; left:5%; right:5%; height:2px; background:#f3f4f6; z-index:0; transform:translateY(-50%);"></div>';
                const earnedStamps = 3; // Mock value for preview
                
                // DYNAMIC SHAPES AND ICONS
                let shape = "50%"; // Default circle
                let emptyIcon = null;
                
                if (state.category === 'medico') { shape = "10px"; emptyIcon = "fa-heart"; }
                if (state.category === 'belleza') { shape = "50%"; emptyIcon = "fa-sparkles"; }
                if (state.category === 'clases') { shape = "6px"; emptyIcon = "fa-fire"; }
                
                for(let i=1; i<=sTotal; i++) {
                    if (i <= earnedStamps) {
                        html += `<div style="width:36px; height:36px; border-radius:${shape}; background:${cPri}; color:white; display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:bold; z-index:1; box-shadow:0 0 0 4px #ffffff; transform:scale(1.1); transition:all 0.3s;">
                            <i class="fa-solid ${pIcon}"></i>
                        </div>`;
                    } else {
                        const innerContent = emptyIcon ? `<i class="fa-solid ${emptyIcon}" style="opacity:0.3; font-size:12px;"></i>` : i;
                        html += `<div style="width:36px; height:36px; border-radius:${shape}; background:white; border:2px solid #e5e7eb; color:#9ca3af; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600; z-index:1; box-shadow:0 0 0 4px #ffffff;">
                            ${innerContent}
                        </div>`;
                    }
                }
                renderStampsGrid.innerHTML = html;
            }
        } else {
            if(renderStampsBody) renderStampsBody.style.display = 'none';
            if(renderCashbackBody) renderCashbackBody.style.display = 'flex';
        }
        
        const bannerContainer = document.getElementById('render-banner-container');
        const bannerImg = document.getElementById('render-banner-img');
        if (bannerContainer && bannerImg) {
            if (state.customBannerUrl) {
                bannerContainer.style.display = 'block';
                bannerImg.src = state.customBannerUrl;
            } else {
                bannerContainer.style.display = 'block';
                bannerImg.src = 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&q=80&w=800&h=300';
            }
        }

        const sampleClient = state.customers[0] || { tier: "Oro VIP", balance: 0, stamps: 3 };
        const clientTier = sampleClient.vip_tier || sampleClient.tier || 'Bronce';
        let currentTierConfig = state.vipTiers.oro;

        if (clientTier.toLowerCase().includes('oro')) {
            currentTierConfig = state.vipTiers.oro;
        } else if (clientTier.toLowerCase().includes('plata')) {
            currentTierConfig = state.vipTiers.plata;
        } else {
            currentTierConfig = state.vipTiers.bronce;
        }

        const vipCaption = document.getElementById('render-vip-caption');
        if (vipCaption) {
            vipCaption.textContent = currentTierConfig.name.toUpperCase();
        }

        // Render back of card benefits dynamically
        const renderVipBack = document.getElementById('render-vip-benefits-back');
        const renderVipList = document.getElementById('render-vip-benefits-list');
        if (renderVipBack && renderVipList) {
            if (currentTierConfig.benefits && currentTierConfig.benefits.length > 0) {
                renderVipBack.style.display = 'block';
                renderVipList.innerHTML = currentTierConfig.benefits.map(b => {
                    let typeLabel = b.type;
                    if(b.type === 'cashback') typeLabel = 'Cashback';
                    else if(b.type === 'puntos') typeLabel = 'Multiplicador Puntos';
                    else if(b.type === 'descuento') typeLabel = 'Descuento';
                    else if(b.type === 'producto') typeLabel = 'Producto Gratis';
                    else if(b.type === 'upgrade') typeLabel = 'Upgrade';
                    else if(b.type === 'otro') typeLabel = 'Beneficio';
                    return `<li style="margin-bottom:4px;"><strong>${typeLabel}:</strong> ${b.value}</li>`;
                }).join('');
            } else {
                renderVipBack.style.display = 'none';
                renderVipList.innerHTML = '';
            }
        }

        const rBal = document.getElementById('render-balance');
        if (rBal) {
            const bal = sampleClient.current_balance !== undefined ? sampleClient.current_balance : (sampleClient.balance || 0);
            rBal.textContent = `$${bal.toFixed(2)}`;
        }
        
        const rWalletBlock = document.getElementById('render-wallet-block');
        const rWalletBal = document.getElementById('render-wallet-balance');
        const rCashbackBlock = document.getElementById('render-cashback-block');
        
        // Show Wallet Block if Prepaid is Active
        if (state.prepaidActive === true) {
            if (rWalletBlock) {
                rWalletBlock.style.display = 'block';
                // Mock balance based on the bonus config
                const demoWallet = (state.prepaidAmount || 500) + (state.prepaidBonus || 100);
                if (rWalletBal) rWalletBal.textContent = `$${demoWallet.toFixed(2)}`;
            }
        } else {
            if (rWalletBlock) rWalletBlock.style.display = 'none';
        }
        
        // Hide Cashback and VIP Blocks if mode is stamps or user is professional
        const isProfessional = (window.merchantData && window.merchantData.business_type === 'professional');
        const rVipBlock = document.getElementById('render-vip-block');
        
        if (pType === 'stamps' || state.activeMode === 'stamps' || isProfessional || (state.cashbackActive === false && pType !== 'cashback' && pType !== 'hybrid')) {
            if (rCashbackBlock) rCashbackBlock.style.display = 'none';
            if (rVipBlock) rVipBlock.style.display = 'none';
        } else {
            if (rCashbackBlock) rCashbackBlock.style.display = 'block';
            if (rVipBlock) rVipBlock.style.display = 'block';
        }

        
        // --- PROGRAM TYPE TOGGLE (QR vs Stamps) ---
        const qrView = document.getElementById('render-qr-view');
        const stampsView = document.getElementById('render-stamps-view');
        const configStamps = document.getElementById('stamps-config-group');
        
        if (pType === 'stamps') {
            if (qrView) qrView.style.display = 'none';
            if (stampsView) stampsView.style.display = 'flex';
            if (configStamps) configStamps.style.display = 'flex';
            
            // Force redraw of stamps just in case
            let stampsGrid_injected = document.getElementById('render-stamps-grid');
            if (stampsGrid_injected && !stampsGrid_injected.innerHTML) {
                 stampsGrid_injected.innerHTML = '';
                 for(let i=1; i<=10; i++) {
                     stampsGrid_injected.innerHTML += `<div class="stamp-coin ${i<=3?'filled':'empty'}" style="background-color:${i<=3?cAcc:''};">${i>3?i:''}</div>`;
                 }
            }
            
            // Generate stamps
            const stampsGrid = document.getElementById('render-stamps-grid');
            if (stampsGrid) {
                stampsGrid.innerHTML = '';
                const userStamps = sampleClient.stamps || 3; // Demo default
                // Use custom icon/image for stamps
                const iconSrc = state.iconClass || 'fa-star';
                const isImage = iconSrc.startsWith('data:image') || iconSrc.startsWith('http');

                for (let i = 1; i <= sTotal; i++) {
                    const node = document.createElement('div');
                    if (i <= userStamps) {
                        node.className = 'stamp-coin filled';
                        node.style.backgroundColor = cAcc;
                        if (isImage) {
                            node.innerHTML = `<img src="${iconSrc}" style="width:70%; height:70%; object-fit:contain; border-radius:50%;">`;
                            node.style.backgroundColor = 'rgba(255,255,255,0.9)';
                            node.style.border = `2px solid ${cAcc}`;
                        } else {
                            node.innerHTML = `<i class="fa-solid ${iconSrc}"></i>`;
                        }
                    } else {
                        node.className = 'stamp-coin empty';
                        node.textContent = i;
                    }
                    stampsGrid.appendChild(node);
                }
            }
        } else {
            if (qrView) qrView.style.display = 'flex';
            if (stampsView) stampsView.style.display = 'none';
            if (configStamps) configStamps.style.display = 'none';
        }
        
        // Add "Invitar a un Amigo" link dynamically
        let referLink = document.getElementById('render-refer-link');
        if (!referLink) {
            const qrSection = document.getElementById('render-qr-view');
            if (qrSection) {
                referLink = document.createElement('div');
                referLink.id = 'render-refer-link';
                referLink.style = 'margin-top:16px; width:100%; text-align:center; padding-top:12px; border-top:1px solid rgba(0,0,0,0.05);';
                referLink.innerHTML = `<a href="#" style="color:var(--accent-violet); font-size:12px; font-weight:700; text-decoration:none;"><i class="fa-solid fa-user-plus"></i> Invitar a un amigo y ganar recompensas</a>`;
                qrSection.parentNode.insertBefore(referLink, qrSection.nextSibling);
            }
        }
    }

    
    
    
    
    
    
    window.updatePassRender = updatePassRender;
    safeAdd('program-type-select', 'change', updatePassRender);
    safeAdd('program-type-select', 'input', updatePassRender);
    safeAdd('stamps-total', 'input', updatePassRender);
    safeAdd('stamps-total', 'change', updatePassRender);
    
    // --- PUSH OTA LOGIC ---
    const btnSavePush = document.getElementById('btn-save-design-push');
    const pushModal = document.getElementById('push-update-modal');
    const btnCancelPush = document.getElementById('btn-cancel-push');
    const btnConfirmPush = document.getElementById('btn-confirm-push');
    const btnClosePush = document.getElementById('btn-close-push');
    
    const step1 = document.getElementById('push-modal-step-1');
    const step2 = document.getElementById('push-modal-step-2');
    const step3 = document.getElementById('push-modal-step-3');
    
    const progressBar = document.getElementById('push-progress-bar');
    const progressText = document.getElementById('push-progress-text');
    
    if (btnSavePush && pushModal) {
        btnSavePush.addEventListener('click', () => {
            pushModal.style.display = 'flex';
            step1.style.display = 'block';
            step2.style.display = 'none';
            step3.style.display = 'none';
        });
        
        btnCancelPush.addEventListener('click', () => {
            pushModal.style.display = 'none';
        });
        
        btnClosePush.addEventListener('click', () => {
            pushModal.style.display = 'none';
            showToast("Diseño guardado y sincronizado con éxito", "success");
        });
        
        btnConfirmPush.addEventListener('click', async () => {
            try {
                if (typeof window.saveDesignToSupabase === 'function') {
                    await window.saveDesignToSupabase();
                }
                
                if (!state.tenantId) { console.warn('tenantId null'); } else if (window.supabaseClient && state.tenantId) {
                    const { error } = await window.supabaseClient
                        .from('merchants')
                        .update({ branches: state.branches })
                        .eq('id', state.tenantId);
                    if (error) {
                        console.error("Error en DB: " + error.message);
                    }
                }
            } catch (ex) {
                console.error("Crash inline DB: " + ex.message);
            }
            step1.style.display = 'none';
            step2.style.display = 'block';
            
            let count = 0;
            const total = 1428;
            
            // Simulate network APNs request
            const interval = setInterval(() => {
                count += Math.floor(Math.random() * 80) + 10;
                if (count >= total) {
                    count = total;
                    clearInterval(interval);
                    setTimeout(() => {
                        step2.style.display = 'none';
                        step3.style.display = 'block';
                    }, 500);
                }
                
                const percent = (count / total) * 100;
                if (progressBar) progressBar.style.width = percent + '%';
                if (progressText) progressText.textContent = `${count.toLocaleString()} / ${total.toLocaleString()}`;
                
            }, 100);
        });
    }
    
    // --- UPLOAD HANDLERS ---
    const stampFileInput = document.getElementById('stamp-file-input');
    const btnRemoveStamp = document.getElementById('btn-remove-stamp');
    
    if (stampFileInput) {
        stampFileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => {
                    state.iconClass = evt.target.result;
                    if(btnRemoveStamp) btnRemoveStamp.style.display = 'inline-block';
                    updatePassRender();
                    showToast("Sello personalizado cargado", "success");
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    if (btnRemoveStamp) {
        btnRemoveStamp.addEventListener('click', () => {
            const sel = document.getElementById('rest-icon');
            state.iconClass = sel ? sel.value : 'fa-star';
            if(stampFileInput) stampFileInput.value = '';
            btnRemoveStamp.style.display = 'none';
            updatePassRender();
            showToast("Imagen del sello removida", "info");
        });
    }

    const logoFileInput = document.getElementById('logo-file-input');
    const bannerFileInput = document.getElementById('banner-file-input');
    const btnRemoveLogo = document.getElementById('btn-remove-logo');
    const btnRemoveBanner = document.getElementById('btn-remove-banner');

    if (logoFileInput) {
        logoFileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => {
                    state.customLogoUrl = evt.target.result;
                    
                    btnRemoveLogo.style.display = 'inline-block';
                    updatePassRender();

                    showToast("Logo cargado con éxito en la tarjeta digital.", "success");
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (btnRemoveLogo) {
        btnRemoveLogo.addEventListener('click', () => {
            state.customLogoUrl = null;
            
            logoFileInput.value = '';
            btnRemoveLogo.style.display = 'none';
            updatePassRender();

            showToast("Logo removido.", "info");
        });
    }

    if (bannerFileInput) {
        bannerFileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => {
                    state.customBannerUrl = evt.target.result;
                    
                    btnRemoveBanner.style.display = 'inline-block';
                    updatePassRender();

                    showToast("Imagen de portada de tarjeta aplicada.", "success");
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (btnRemoveBanner) {
        btnRemoveBanner.addEventListener('click', () => {
            state.customBannerUrl = null;
            
            bannerFileInput.value = '';
            btnRemoveBanner.style.display = 'none';
            updatePassRender();

            showToast("Imagen de portada removida.", "info");
        });
    }

    // --- TAB NAVIGATION ---
    const navTabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');

    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Cerrar sidebar en móviles
            const sidebar = document.querySelector('.app-sidebar');
            if(sidebar) sidebar.classList.remove('mobile-open');

            navTabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const targetTab = tab.getAttribute('data-tab');
            if (targetTab) {
                const targetElement = document.getElementById(targetTab);
                if (targetElement) {
                    targetElement.classList.add('active');
                } else {
                    console.warn(`Pestaña en construcción o no encontrada: ${targetTab}`);
                }
                
                if(targetTab === 'tab-stripe') {
                    const sel = document.getElementById('stripe-campaign-select');
                    let camps = (window.state && window.state.campaigns) ? window.state.campaigns : [];
                    if (sel && camps.length > 0) {
                        sel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
                        camps.forEach(c => {
                            const opt = document.createElement('option');
                            opt.value = c.id;
                            opt.textContent = c.name || c.type || 'Programa';
                            sel.appendChild(opt);
                        });
                    }
                }
                if(targetTab === 'tab-leads' && typeof window.loadLeads === 'function') window.loadLeads();
                else if(targetTab === 'tab-global-db' && typeof window.loadGlobalDatabase === 'function') window.loadGlobalDatabase();
                else if(targetTab === 'tab-merchants-control' && typeof window.loadMerchantsControl === 'function') window.loadMerchantsControl();
                else if(targetTab === 'tab-loyalty' && typeof window.initLoyaltyTab === 'function') window.initLoyaltyTab();
                else if(targetTab === 'tab-inbox' && typeof window.loadInbox === 'function') window.loadInbox();
                else if(targetTab === 'tab-fidelio-team' && typeof window.loadFidelioTeam === 'function') window.loadFidelioTeam();
                else if(targetTab === 'tab-campaigns' && typeof window.loadCampaigns === 'function') window.loadCampaigns();
                else if(targetTab === 'tab-appointments' && typeof window.loadAppointments === 'function') window.loadAppointments();
                else if(targetTab === 'tab-bank' && typeof window.loadBankStats === 'function') window.loadBankStats();

                localStorage.setItem('activeFidelioTab', targetTab);
            }
        });
    });

    // Restaurar pestaña activa al recargar (si existe)
    const savedTab = localStorage.getItem('activeFidelioTab');
    if (savedTab) {
        const tabToClick = Array.from(navTabs).find(t => t.getAttribute('data-tab') === savedTab);
        if (tabToClick) tabToClick.click();
    }

    
    // --- 3D CARD FLIP LOGIC ---
    const btnFlipCard = document.getElementById('btn-flip-card');
    const card3d = document.getElementById('pass-render');
    if (btnFlipCard && card3d) {
        btnFlipCard.addEventListener('click', () => {
            card3d.classList.toggle('is-flipped');
            if (card3d.classList.contains('is-flipped')) {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-left"></i> Ver Frente';
            } else {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Ver Reverso (3D)';
            }
        });
        
        card3d.addEventListener('click', (e) => {
            card3d.classList.toggle('is-flipped');
            if (card3d.classList.contains('is-flipped')) {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-left"></i> Ver Frente';
            } else {
                btnFlipCard.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Ver Reverso (3D)';
            }
        });
    }

    // --- WALLET SELECTOR ---
    const btnApple = document.getElementById('btn-apple-wallet');
    const btnGoogle = document.getElementById('btn-google-wallet');

    if (btnApple) {
        btnApple.addEventListener('click', () => {
            btnApple.classList.add('active');
            btnGoogle.classList.remove('active');
            state.activeWallet = 'apple';
            passRender.style.borderRadius = '20px';
            updatePassRender();

        });
    }

    if (btnGoogle) {
        btnGoogle.addEventListener('click', () => {
            btnGoogle.classList.add('active');
            btnApple.classList.remove('active');
            state.activeWallet = 'google';
            passRender.style.borderRadius = '16px';
            updatePassRender();

        });
    }

    // --- INPUT BINDINGS ---
    safeAdd('rest-name', 'input', (e) => {
        state.restaurantName = e.target.value || "Comercio"; updatePassRender();
    });
    safeAdd('business-category-input', 'input', (e) => {
        updatePassRender();
    });
    safeAdd('color-primary', 'input', (e) => {
        state.colorPrimary = e.target.value; updatePassRender();

    });
    safeAdd('color-accent', 'input', (e) => {
        state.colorAccent = e.target.value; updatePassRender();

    });
    safeAdd('rest-icon', 'change', (e) => {
        state.iconClass = e.target.value; updatePassRender();

    });
    safeAdd('mech-cashback-check', 'change', (e) => {
        state.cashbackActive = e.target.checked; updatePassRender();

    });
    safeAdd('cashback-percent', 'input', (e) => {
        state.cashbackPercent = parseFloat(e.target.value) || 0; updatePassRender();

    });
    safeAdd('mech-stamps-check', 'change', (e) => {
        state.stampsActive = e.target.checked; updatePassRender();

    });
    safeAdd('stamps-total', 'input', (e) => {
        state.stampsTotal = parseInt(e.target.value) || 5; updatePassRender();

    });
    safeAdd('stamps-reward', 'input', (e) => {
        state.stampsReward = e.target.value || "Premio"; updatePassRender();

    });
    safeAdd('mech-dynamic-check', 'change', (e) => {
        state.dynamicActive = e.target.checked; updatePassRender();

    });
    safeAdd('dynamic-desc', 'input', (e) => {
        state.dynamicDesc = e.target.value; updatePassRender();

    });
    safeAdd('mech-vip-check', 'change', (e) => {
        state.vipActive = e.target.checked; updatePassRender();

    });

    if (crmSearchInput) {
        crmSearchInput.addEventListener('input', renderCRMTable);
        crmFilterTier.addEventListener('change', renderCRMTable);
        crmFilterStatus.addEventListener('change', renderCRMTable);
    }

    const btnExportCrm = document.getElementById('btn-export-crm');
    if (btnExportCrm) {
        btnExportCrm.addEventListener('click', () => {
            showToast(`Exportando archivo CSV con ${state.customers.length} registros...`, "success");
        });
    }

    const btnAddDemoClient = document.getElementById('btn-add-demo-client');
    if (btnAddDemoClient) {
        btnAddDemoClient.addEventListener('click', () => {
            modalOnboarding.classList.remove('hidden');
        });
    }

    // --- THE BANK MODULE ---
    window.loadBankStats = async function() {
        if (!window.merchantSession) return;
        const merchantId = window.merchantSession.user.id;
        
        const tbody = document.getElementById('bank-table-body');
        if (tbody) tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Calculando saldos...</td></tr>';
        
        // Fetch customers with wallet info
        const { data: customers, error } = await window.supabaseClient
            .from('customers')
            .select('full_name, email, wallet_balance, wallet_deposited, wallet_spent')
            .eq('merchant_id', merchantId)
            .order('wallet_balance', { ascending: false });
            
        if (error) {
            if (error.code === '42703') {
                if (tbody) tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#ef4444;">Faltan las columnas del Monedero. Corre el script SQL primero.</td></tr>';
            } else {
                if (tbody) tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;
            }
            return;
        }

        let totalDeposited = 0;
        let totalUnspent = 0;

        if (!customers || customers.length === 0) {
            if (tbody) tbody.innerHTML = `<tr><td colspan='4' style='padding:40px; text-align:center;'><div style='display:inline-block; max-width:300px;'><div style='font-size:40px; margin-bottom:16px; color:#3b82f6;'><i class='fa-solid fa-face-sad-tear'></i></div><h4 style='margin:0 0 8px; font-size:18px;'>Sin clientes aún</h4><p style='color:var(--text-muted); font-size:14px;'>Comparte tu código QR en tu mostrador o redes sociales para empezar a captar lealtad.</p></div></td></tr>`;
        } else {
            if (tbody) tbody.innerHTML = '';
            customers.forEach(c => {
                const deposited = parseFloat(c.wallet_deposited || 0);
                const spent = parseFloat(c.wallet_spent || 0);
                const balance = parseFloat(c.wallet_balance || 0);
                
                totalDeposited += deposited;
                totalUnspent += balance;

                if (tbody) {
                    tbody.innerHTML += `
                        <tr style="border-bottom: 1px solid var(--border-soft);">
                            <td style="padding: 16px;">
                                <strong>${c.full_name || 'Sin Nombre'}</strong>
                                <div style="font-size:12px; color:var(--text-muted);">${c.email}</div>
                            </td>
                            <td style="padding: 16px; color: #10b981; font-weight: 600;">$${deposited.toFixed(2)}</td>
                            <td style="padding: 16px; color: #ef4444;">$${spent.toFixed(2)}</td>
                            <td style="padding: 16px; font-weight: 700; color: var(--accent-violet);">$${balance.toFixed(2)}</td>
                        </tr>
                    `;
                }
            });
        }

        // Update top metrics
        const domDeposited = document.getElementById('bank-total-deposited');
        const domUnspent = document.getElementById('bank-total-unspent');
        if (domDeposited) domDeposited.textContent = `$${totalDeposited.toFixed(2)}`;
        if (domUnspent) domUnspent.textContent = `$${totalUnspent.toFixed(2)}`;
    };

    // --- MASTER ADMIN SUITE (ADMIN ONLY) ---
    const checkMasterAdmin = () => {
        return window.fidelioAdminRole === 'admin' || window.fidelioAdminRole === 'super_admin';
    };

    
    // 0. EQUIPO FIDELIO (SUPER ADMIN ONLY)
    window.loadFidelioTeam = async function() {
        if (window.fidelioAdminRole !== 'super_admin') return; // Solo super_admin hardcodeado puede verlo por ahora
        
        const tbody = document.getElementById('fidelio-team-body');
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Cargando equipo...</td></tr>';
        
        const { data, error } = await window.supabaseClient.from('fidelio_admins').select('*').order('created_at', { ascending: false });
        if (error) {
            if(error.code === '42P01') {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">La tabla fidelio_admins no existe aún. Por favor corre el script SQL de Master Admin.</td></tr>';
            } else {
                tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;
            }
            return;
        }
        
        tbody.innerHTML = '';
        if(!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">No hay miembros del equipo.</td></tr>';
            return;
        }
        
        data.forEach(m => {
            const date = new Date(m.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' });
            let roleBadge = m.role === 'super_admin' ? '<span class="menu-badge" style="background:var(--accent-violet);color:#fff;font-size:10px;">SUPER ADMIN</span>' : '<span class="menu-badge" style="background:#3b82f6;color:#fff;font-size:10px;">ADMINISTRADOR</span>';
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft);">
                    <td style="padding: 16px;"><strong>${m.email}</strong></td>
                    <td style="padding: 16px;">${roleBadge}</td>
                    <td style="padding: 16px;">${date}</td>
                    <td style="padding: 16px; text-align: right;">
                        ${m.email === 'hola@fideliorewards.com' ? '<span style="color:var(--text-muted);font-size:12px;">Dueño</span>' : `<button class="btn-preset" onclick="removeFidelioAdmin('${m.id}')" title="Revocar Acceso" style="border-color:#ef4444; color:#ef4444;"><i class="fa-solid fa-trash"></i></button>`}
                    </td>
                </tr>
            `;
        });
    };

    window.addFidelioAdmin = async function() {
        if (window.fidelioAdminRole !== 'super_admin') return;
        const emailInput = document.getElementById('new-admin-email');
        const roleSelect = document.getElementById('new-admin-role');
        
        const email = emailInput.value.trim().toLowerCase();
        if(!email) return showToast('Ingresa un correo electrónico.', 'error');
        
        const { error } = await window.supabaseClient.from('fidelio_admins').insert([{
            email: email,
            role: roleSelect.value
        }]);
        
        if (error) {
            showToast('Error al agregar: ' + error.message, 'error');
        } else {
            showToast('Miembro agregado correctamente', 'success');
            emailInput.value = '';
            loadFidelioTeam();
        }
    };

    window.removeFidelioAdmin = async function(id) {
        if (window.fidelioAdminRole !== 'super_admin') return;
        if(!confirm('¿Estás seguro de revocar el acceso a este miembro del equipo?')) return;
        const { error } = await window.supabaseClient.from('fidelio_admins').delete().eq('id', id);
        if(error) showToast('Error al revocar: ' + error.message, 'error');
        else { showToast('Acceso revocado', 'success'); loadFidelioTeam(); }
    };

// 1. LEADS (PROSPECTOS)
    window.loadLeads = async function() {
        if (!checkMasterAdmin()) return;
        const tbody = document.getElementById('leads-table-body');
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Cargando prospectos...</td></tr>';
        
        const { data, error } = await window.supabaseClient
            .from('demo_requests')
            .select('*')
            .order('created_at', { ascending: false });
            
        if (error) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:#ef4444;">Error cargando prospectos: ${error.message}</td></tr>`;
            return;
        }
        
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No hay solicitudes pendientes.</td></tr>';
            return;
        }
        
        tbody.innerHTML = '';
        data.forEach(lead => {
            const date = new Date(lead.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' });
            let statusBadge = '<span class="menu-badge" style="background:#4b5563;color:#fff;font-size:10px;">NUEVO</span>';
            if(lead.status === 'interes') statusBadge = '<span class="menu-badge" style="background:#f59e0b;color:#fff;font-size:10px;">INTERÉS</span>';
            if(lead.status === 'negociacion') statusBadge = '<span class="menu-badge" style="background:#3b82f6;color:#fff;font-size:10px;">NEGOCIACIÓN</span>';
            if(lead.status === 'cerrado') statusBadge = '<span class="menu-badge" style="background:#10b981;color:#fff;font-size:10px;">CERRADO</span>';

            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft);">
                    <td style="padding: 16px;">${date}</td>
                    <td style="padding: 16px;"><strong style="color:var(--text-main);">${lead.name || 'Sin nombre'}</strong></td>
                    <td style="padding: 16px;">
                        <div style="font-size:13px; color:var(--text-muted);"><i class="fa-solid fa-envelope"></i> ${lead.email}</div>
                        <div style="font-size:13px; color:var(--text-muted);"><i class="fa-solid fa-phone"></i> ${lead.phone || 'N/A'}</div>
                    </td>
                    <td style="padding: 16px;">${statusBadge}</td>
                    <td style="padding: 16px; text-align: right; display: flex; gap: 8px; justify-content: flex-end;">
                        <button class="btn-preset" onclick="updateLeadStatus('${lead.id}', 'interes')" title="Interés"><i class="fa-solid fa-fire" style="color:#f59e0b;"></i></button>
                        <button class="btn-preset" onclick="updateLeadStatus('${lead.id}', 'negociacion')" title="Negociación"><i class="fa-solid fa-handshake" style="color:#3b82f6;"></i></button>
                        <button class="btn-preset" onclick="updateLeadStatus('${lead.id}', 'cerrado')" title="Cerrado"><i class="fa-solid fa-check-circle" style="color:#10b981;"></i></button>
                        <button class="btn-preset" onclick="deleteLead('${lead.id}')" title="Borrar" style="border-color:#ef4444; color:#ef4444;"><i class="fa-solid fa-trash"></i></button>
                    </td>
                </tr>
            `;
        });
    };

    window.updateLeadStatus = async function(id, status) {
        if (!checkMasterAdmin()) return;
        const { error } = await window.supabaseClient.from('demo_requests').update({ status: status }).eq('id', id);
        if(error) showToast('Error actualizando lead: ' + error.message, 'error');
        else { showToast('Lead actualizado', 'success'); loadLeads(); }
    };

    window.deleteLead = async function(id) {
        if (!checkMasterAdmin()) return;
        if(!confirm('¿Estás seguro de borrar este lead permanentemente?')) return;
        const { error } = await window.supabaseClient.from('demo_requests').delete().eq('id', id);
        if(error) showToast('Error borrando lead: ' + error.message, 'error');
        else { showToast('Lead borrado', 'success'); loadLeads(); }
    };

    // 2. GLOBAL DATABASE
    let globalDBCache = [];
    window.loadGlobalDatabase = async function() {
        if (!checkMasterAdmin()) return;
        const tbody = document.getElementById('global-db-body');
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Cargando base de datos global...</td></tr>';
        
        // Obtener clientes junto con los datos de su restaurante
        const { data, error } = await window.supabaseClient
            .from('customers')
            .select(`
                id, full_name, email, merchant_id, created_at,
                merchants(business_name, industry)
            `)
            .order('created_at', { ascending: false })
            .limit(1000); 

        if (error) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;
            return;
        }
        
        // Formatear la data para que sea más plana y fácil de filtrar
        globalDBCache = (data || []).map(c => {
            const m = c.merchants || {};
            return {
                id: c.id,
                full_name: c.full_name,
                email: c.email,
                merchant_id: c.merchant_id,
                created_at: c.created_at,
                business_name: m.business_name || 'Desconocido',
                country: m.country || '',
                state: m.state || '',
                industry: m.industry || 'other'
            };
        });
        
        filterGlobalDB(); // Llama el render inicial respetando filtros (si los hubiera en el DOM cacheado)
    };

    window.renderGlobalDB = function(data) {
        const tbody = document.getElementById('global-db-body');
        tbody.innerHTML = '';
        if(data.length === 0) { tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No hay resultados para estos filtros.</td></tr>'; return; }
        
        data.forEach(c => {
            const date = new Date(c.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' });
            
            // Format labels for location/industry
            let locationLabel = c.country ? `${c.country}` : '';
            if(c.state) locationLabel += locationLabel ? `, ${c.state}` : c.state;
            if(!locationLabel) locationLabel = 'N/D';
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft);">
                    <td style="padding: 16px; font-family:monospace; font-size:12px;">${c.id.substring(0,8)}...</td>
                    <td style="padding: 16px;"><strong>${c.full_name}</strong></td>
                    <td style="padding: 16px;">${c.email}</td>
                    <td style="padding: 16px;">
                        <strong style="color:var(--accent-violet);">${c.business_name}</strong>
                        <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">
                            ${locationLabel} &bull; ${c.industry}
                        </div>
                    </td>
                    <td style="padding: 16px;">${date}</td>
                </tr>
            `;
        });
    };

    window.filterGlobalDB = function() {
        const searchInput = document.getElementById('global-db-search')?.value.toLowerCase() || '';
        const filterCountry = document.getElementById('global-db-filter-country')?.value || '';
        const filterState = document.getElementById('global-db-filter-state')?.value.toLowerCase() || '';
        const filterIndustry = document.getElementById('global-db-filter-industry')?.value || '';
        const filterBusiness = document.getElementById('global-db-filter-business')?.value.toLowerCase() || '';

        const filtered = globalDBCache.filter(c => {
            let match = true;
            // Name or email search
            if (searchInput && !c.full_name.toLowerCase().includes(searchInput) && !c.email.toLowerCase().includes(searchInput)) match = false;
            // Country
            if (filterCountry && c.country !== filterCountry) match = false;
            // State
            if (filterState && !c.state.toLowerCase().includes(filterState)) match = false;
            // Industry
            if (filterIndustry && c.industry !== filterIndustry) match = false;
            // Business Name
            if (filterBusiness && !c.business_name.toLowerCase().includes(filterBusiness)) match = false;
            
            return match;
        });
        
        renderGlobalDB(filtered);
    };

    // 3. MERCHANTS CONTROL
    window.loadMerchantsControl = async function() {
        if (!checkMasterAdmin()) return;
        const tbody = document.getElementById('merchants-control-body');
        const listMorosos = document.getElementById('morosos-list');
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Cargando restaurantes...</td></tr>';
        listMorosos.innerHTML = '<div style="text-align:center;color:var(--text-muted);padding:20px;">Cargando...</div>';
        
        const { data, error } = await window.supabaseClient.from('merchants').select('id, business_name, plan_status, created_at');
        if (error) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;
            return;
        }
        
        tbody.innerHTML = '';
        let morososHTML = '';
        
        (data || []).forEach(m => {
            const createdDate = new Date(m.created_at);
            const now = new Date();
            const daysSinceCreated = Math.floor((now - createdDate) / (1000 * 60 * 60 * 24));
            
            let daysLeft = 'N/A';
            let paymentStatus = '<span style="color:#10b981;">Al Día</span>';
            let planBadge = `<span class="menu-badge" style="background:var(--accent-violet);color:#fff;font-size:10px;">${m.plan_status.toUpperCase()}</span>`;
            
            if (m.plan_status === 'trial') {
                daysLeft = 14 - daysSinceCreated;
                if(daysLeft <= 0) {
                    daysLeft = 'Expirado';
                    paymentStatus = '<span style="color:#ef4444;font-weight:700;">Pago Requerido</span>';
                    morososHTML += `
                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border-soft); padding:12px 0;">
                            <div>
                                <strong style="display:block;">${m.business_name}</strong>
                                <span style="font-size:12px; color:var(--text-muted);">Trial expirado hace ${Math.abs(14 - daysSinceCreated)} días</span>
                            </div>
                            <button class="btn-preset" onclick="contactMerchant('${m.id}')"><i class="fa-solid fa-envelope"></i> Aviso</button>
                        </div>
                    `;
                } else {
                    paymentStatus = '<span style="color:#f59e0b;">Trial Activo</span>';
                }
            } else if (m.plan_status === 'active' || m.plan_status === 'lifetime_free') {
                daysLeft = '∞';
                paymentStatus = '<span style="color:#10b981;">Pagado</span>';
            } else if (m.plan_status === 'paused') {
                daysLeft = '-';
                paymentStatus = '<span style="color:#f59e0b;">Pausado</span>';
                planBadge = `<span class="menu-badge" style="background:#f59e0b;color:#fff;font-size:10px;">PAUSED</span>`;
            }

            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft);">
                    <td style="padding: 16px;"><strong>${m.business_name}</strong></td>
                    <td style="padding: 16px;">${planBadge}</td>
                    <td style="padding: 16px;">${daysLeft}</td>
                    <td style="padding: 16px;">${paymentStatus}</td>
                    <td style="padding: 16px; text-align: right;">
                        <button class="btn-preset" onclick="toggleMerchantStatus('${m.id}', '${m.plan_status}')" title="Pausar/Activar">
                            <i class="fa-solid ${m.plan_status === 'paused' ? 'fa-play' : 'fa-pause'}" style="color:var(--text-muted);"></i>
                        </button>
                        <button class="btn-preset" onclick="grantFreeAccount('${m.id}')" title="Regalar Lifetime Free"><i class="fa-solid fa-gift" style="color:var(--accent-violet);"></i></button>
                    </td>
                </tr>
            `;
        });
        
        if(morososHTML === '') listMorosos.innerHTML = '<div style="text-align:center;color:var(--success);padding:20px;">Todos los pagos están al día.</div>';
        else listMorosos.innerHTML = morososHTML;
    };

    window.toggleMerchantStatus = async function(id, currentStatus) {
        if (!checkMasterAdmin()) return;
        const newStatus = currentStatus === 'paused' ? 'active' : 'paused';
        const { error } = await window.supabaseClient.from('merchants').update({ plan_status: newStatus }).eq('id', id);
        if(error) showToast('Error: ' + error.message, 'error');
        else { showToast('Estatus actualizado', 'success'); loadMerchantsControl(); }
    };

    window.grantFreeAccount = async function(id) {
        if (!checkMasterAdmin()) return;
        if(!confirm('¿Estás seguro de regalar una cuenta lifetime free a este restaurante?')) return;
        const { error } = await window.supabaseClient.from('merchants').update({ plan_status: 'lifetime_free' }).eq('id', id);
        if(error) showToast('Error: ' + error.message, 'error');
        else { showToast('Cuenta otorgada', 'success'); loadMerchantsControl(); }
    };

    // 4. MASTER ADMIN (PROMOS)
    window.generatePromoCode = async function() {
        if (!checkMasterAdmin()) return;
        const codeInput = document.getElementById('promo-code-input');
        const typeSelect = document.getElementById('promo-type-select');
        const targetPlanSelect = document.getElementById('promo-target-plan');
        const discountInput = document.getElementById('promo-discount-input');
        const stripeLinkInput = document.getElementById('promo-stripe-link-input');
        const freeBranchesInput = document.getElementById('promo-free-branches-input');
        const customPriceInput = document.getElementById('promo-custom-price-input');
        
        const code = codeInput.value.trim().toUpperCase();
        if(!code) return showToast('Escribe un código válido', 'error');
        
        const type = typeSelect.value;
        let discount_pct = 0;
        let stripe_link = null;
        let free_branches_count = 0;
        let custom_branch_price = null;

        if (type === 'discount') {
            discount_pct = parseInt(discountInput.value) || 0;
            if (discount_pct <= 0 || discount_pct > 100) return showToast('Descuento inválido', 'error');
            stripe_link = stripeLinkInput ? stripeLinkInput.value.trim() : null;
        } else if (type === 'free_branches') {
            free_branches_count = parseInt(freeBranchesInput.value) || 0;
            if (free_branches_count <= 0) return showToast('Cantidad de sucursales inválida', 'error');
        } else if (type === 'custom_branch_price') {
            custom_branch_price = parseFloat(customPriceInput.value);
            if (isNaN(custom_branch_price) || custom_branch_price < 0) return showToast('Precio inválido', 'error');
        }
        
        const { error } = await window.supabaseClient.from('promo_codes').insert([{
            code: code,
            reward_type: type,
            target_plan: targetPlanSelect ? targetPlanSelect.value : 'business',
            discount_pct: discount_pct,
            stripe_payment_link: stripe_link,
            free_branches_count: free_branches_count,
            custom_branch_price: custom_branch_price,
            max_uses: 1, 
            is_active: true
        }]);
        
        if (error) {
            showToast('Error al crear código: ' + error.message, 'error');
        } else {
            showToast('Código promocional activado', 'success');
            codeInput.value = '';
            discountInput.value = '';
            freeBranchesInput.value = '';
            customPriceInput.value = '';
        }
    };

    // 5. INBOX SUPPORT
    window.loadInbox = async function() {
        if (!checkMasterAdmin()) return;
        const tbody = document.getElementById('inbox-table-body');
        const themeFilter = document.getElementById('inbox-theme-filter')?.value || 'all';
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Cargando tickets...</td></tr>';
        
        let query = window.supabaseClient.from('support_tickets').select('*').order('created_at', { ascending: false });
        
        // Simple mapping for theme keywords if we had a dedicated theme column, 
        // since we don't, we might filter by subject keywords for demo purposes.
        if (themeFilter !== 'all') {
            if (themeFilter === 'soporte') query = query.ilike('subject', '%soport%');
            else if (themeFilter === 'facturacion') query = query.ilike('subject', '%pago%');
            else if (themeFilter === 'reporte') query = query.ilike('subject', '%error%');
        }

        const { data, error } = await query;
        
        if (error) {
            if(error.code === '42P01') {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">La tabla support_tickets no existe aún. Corre el script SQL primero.</td></tr>';
            } else {
                tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;
            }
            return;
        }
        
        // Client-side filtering if ilike didn't catch everything perfectly
        let filteredData = data;
        if (themeFilter === 'dudas') {
            filteredData = data.filter(t => !t.subject.toLowerCase().includes('soport') && !t.subject.toLowerCase().includes('pago') && !t.subject.toLowerCase().includes('error'));
        }
        
        if (!filteredData || filteredData.length === 0) {
            tbody.innerHTML = `<tr><td colspan='5' style='padding:40px; text-align:center;'><div style='display:inline-block; max-width:300px;'><div style='font-size:40px; margin-bottom:16px; color:#10b981;'><i class='fa-solid fa-inbox'></i></div><h4 style='margin:0 0 8px; font-size:18px;'>Bandeja Limpia</h4><p style='color:var(--text-muted); font-size:14px;'>¡Todo al día! No tienes mensajes ni tickets pendientes de revisar. Excelente trabajo.</p></div></td></tr>`;
            return;
        }
        
        window.currentInboxTickets = filteredData;
        tbody.innerHTML = '';
        filteredData.forEach((t, index) => {
            const date = new Date(t.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric', hour:'2-digit', minute:'2-digit' });
            let statusBadge = t.status === 'abierto' ? '<span class="menu-badge" style="background:#ef4444;color:#fff;font-size:10px;">ABIERTO</span>' : '<span class="menu-badge" style="background:#10b981;color:#fff;font-size:10px;">RESUELTO</span>';
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft); ${t.status === 'resuelto' ? 'opacity: 0.6;' : ''}">
                    <td style="padding: 16px; font-size:12px; font-family:monospace;">#${t.id.substring(0,8)}</td>
                    <td style="padding: 16px;">
                        <strong>${t.email || 'Desconocido'}</strong>
                        <div style="font-size:12px; color:var(--text-muted);">${t.merchant_id || 'Visitante'}</div>
                    </td>
                    <td style="padding: 16px;">
                        <strong style="display:block;">${t.subject}</strong>
                        <span style="font-size:13px; color:var(--text-muted);">${t.message.substring(0, 50)}${t.message.length>50?'...':''}</span>
                    </td>
                    <td style="padding: 16px;">${statusBadge}</td>
                    <td style="padding: 16px; text-align: right;">
                        <button class="btn-preset" onclick="viewTicketDetail(${index})" title="Ver Detalle"><i class="fa-solid fa-eye" style="color:var(--accent-violet);"></i></button>
                        ${t.status === 'abierto' ? `<button class="btn-preset" onclick="resolveTicket('${t.id}')" title="Marcar Resuelto"><i class="fa-solid fa-check" style="color:var(--accent-violet);"></i></button>` : ''}
                    </td>
                </tr>
            `;
        });
    };

    window.viewTicketDetail = function(index) {
        const t = window.currentInboxTickets[index];
        if(!t) return;
        
        document.getElementById('ticket-modal-subject').innerText = t.subject || 'Sin asunto';
        document.getElementById('ticket-modal-id').innerText = '#' + t.id;
        document.getElementById('ticket-modal-email').innerText = t.email || 'Desconocido';
        document.getElementById('ticket-modal-merchant').innerText = t.merchant_id || 'Visitante';
        
        const dateStr = new Date(t.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric', hour:'2-digit', minute:'2-digit' });
        document.getElementById('ticket-modal-date').innerText = dateStr;
        
        let statusHtml = t.status === 'abierto' ? '<span style="background:#ef4444;color:#fff;padding:4px 8px;border-radius:12px;font-size:10px;font-weight:bold;">ABIERTO</span>' : '<span style="background:#10b981;color:#fff;padding:4px 8px;border-radius:12px;font-size:10px;font-weight:bold;">RESUELTO</span>';
        document.getElementById('ticket-modal-status').innerHTML = statusHtml;
        
        document.getElementById('ticket-modal-message').innerText = t.message || 'Sin contenido';
        
        const actionsDiv = document.getElementById('ticket-modal-actions');
        actionsDiv.innerHTML = '';
        
        // Botón de email
        if(t.email) {
            const mailto = `mailto:${t.email}?subject=RE: ${encodeURIComponent(t.subject)}&body=${encodeURIComponent('\n\n--- Tu mensaje original ---\n' + t.message)}`;
            actionsDiv.innerHTML += `<a href="${mailto}" class="btn btn-secondary" style="padding:10px 16px; text-decoration:none; display:inline-block;"><i class="fa-solid fa-reply"></i> Responder por Correo</a>`;
        }
        
        if(t.status === 'abierto') {
            actionsDiv.innerHTML += `<button class="btn btn-primary" onclick="resolveTicket('${t.id}'); document.getElementById('modal-ticket-detail').style.display='none';" style="padding:10px 16px; background:var(--success); border:none;"><i class="fa-solid fa-check"></i> Marcar Resuelto</button>`;
        }
        
        document.getElementById('modal-ticket-detail').style.display = 'flex';
    };

    window.resolveTicket = async function(id) {
        if (!checkMasterAdmin()) return;
        const { error } = await window.supabaseClient.from('support_tickets').update({ status: 'resuelto' }).eq('id', id);
        if(error) showToast('Error al resolver: ' + error.message, 'error');
        else { showToast('Ticket resuelto', 'success'); loadInbox(); }
    };

    window.contactMerchant = function(merchantId) {
        if(typeof showToast==='function') showToast('Correo automatizado llegará en la próxima versión', 'info');
    };

    // // Initial Render Calls
    renderAppointments();
    renderBranches();
    renderCRMTable();
    updatePassRender();


    // --- ACCOUNT SETTINGS LOGIC ---
    const accEmail = document.getElementById('acc-email');
    const accPassword = document.getElementById('acc-password');
    const btnSaveAccount = document.getElementById('btn-save-account');
    const btnLogout = document.getElementById('btn-logout');

    if (accEmail && window.merchantSession) {
        accEmail.value = window.merchantSession.user.email;
        
        const accBusinessName = document.getElementById('acc-business-name');
        const accBusinessCategory = document.getElementById('acc-business-category');
        if (accBusinessName && window.merchantData) {
            accBusinessName.value = window.merchantData.business_name || '';
            if (window.merchantData.business_name) {
                accBusinessName.readOnly = true;
                accBusinessName.style.backgroundColor = '#f3f4f6';
                accBusinessName.style.cursor = 'not-allowed';
            }
        }
        if (accBusinessCategory && window.merchantData) accBusinessCategory.value = window.merchantData.industry || '';
        
        const avatarUpload = document.getElementById('acc-avatar-upload');
        if (avatarUpload) {
            avatarUpload.addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file || !window.merchantSession) return;
                
                const icon = document.getElementById('acc-camera-icon');
                const originalIcon = icon.className;
                icon.className = 'fa-solid fa-spinner fa-spin';
                
                try {
                    const ext = file.name.split('.').pop();
                    const filename = `avatar_${window.merchantSession.user.id}_${Date.now()}.${ext}`;
                    
                    const { data, error: uploadError } = await window.supabaseClient.storage.from('logos').upload(filename, file, { upsert: true });
                    if (uploadError) throw new Error('Error al subir: ' + uploadError.message);
                    
                    const { data: publicUrlData } = window.supabaseClient.storage.from('logos').getPublicUrl(filename);
                    const newAvatarUrl = publicUrlData.publicUrl;
                    
                    const { error: dbError } = await window.supabaseClient.from('merchants').update({ avatar_url: newAvatarUrl }).eq('id', window.merchantSession.user.id);
                    if (dbError) throw new Error('Error guardando en base de datos');
                    
                    window.merchantData.avatar_url = newAvatarUrl;
                    const avatarEl = document.getElementById('acc-avatar-letter');
                    const avatarContainer = document.getElementById('acc-avatar-container');
                    if(avatarEl) avatarEl.style.display = 'none';
                    if(avatarContainer) avatarContainer.style.backgroundImage = `url(${newAvatarUrl})`;
                    
                    const sbAvatarIcon = document.getElementById('header-business-icon');
                    if (sbAvatarIcon) {
                        sbAvatarIcon.innerHTML = '';
                        sbAvatarIcon.style.backgroundImage = `url(${newAvatarUrl})`;
                        sbAvatarIcon.style.backgroundSize = 'cover';
                        sbAvatarIcon.style.backgroundPosition = 'center';
                        sbAvatarIcon.style.backgroundRepeat = 'no-repeat';
                    }
                    
                    if (typeof showToast === 'function') showToast('Foto de perfil actualizada', 'success');
                } catch (err) {
                    if (typeof showToast === 'function') showToast(err.message, 'error');
                } finally {
                    icon.className = originalIcon;
                }
            });
        }

        const btnSaveAccProfile = document.getElementById('btn-save-acc-profile');
        if (btnSaveAccProfile) {
            btnSaveAccProfile.addEventListener('click', async () => {
                if (!window.merchantSession) return;
                const newName = accBusinessName.value.trim();
                const newCat = accBusinessCategory.value.trim();
                btnSaveAccProfile.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Guardando...';
                const { error } = await window.supabaseClient.from('merchants').update({
                    business_name: newName,
                    industry: newCat
                }).eq('id', window.merchantSession.user.id);
                
                btnSaveAccProfile.innerHTML = '<i class="fa-solid fa-check"></i> Guardar Perfil';
                if (error) {
                    if (typeof showToast === 'function') showToast('Error al actualizar el perfil', 'error');
                } else {
                    if (typeof showToast === 'function') showToast('Perfil actualizado con éxito', 'success');
                    document.getElementById('header-restaurant-name').textContent = newName || 'Mi Cuenta';
                    document.getElementById('header-business-category').textContent = newCat || 'Profesional';
                    window.merchantData.business_name = newName;
                    window.merchantData.industry = newCat;
                    
                    // Actualizar QR si es posible
                    const prefs = window.merchantData.appointment_settings?.landing_prefs || {};
                    const username = prefs.username || window.merchantData.slug || newName.toLowerCase().replace(/[^a-z0-9]/g, '');
                    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=1000x1000&data=${encodeURIComponent(window.location.origin + '/' + username + '?v=3')}`;
                    const qrPreview = document.getElementById('merchant-qr-preview');
                    if (qrPreview) qrPreview.src = qrUrl;
                }
            });
        }
        
        // ADMIN CHECK FOR LEADS TAB & TEAM FIDELIO
        const initializeAdminUI = async () => {
            const userEmail = window.merchantSession.user.email;
            let isAdmin = false;
            let isSuperAdmin = false;

            // Fallback seguro por si la BD falla
            if (userEmail === 'hola@fideliorewards.com') {
                isAdmin = true;
                isSuperAdmin = true;
            }

            try {
                const { data, error } = await window.supabaseClient
                    .from('fidelio_admins')
                    .select('role')
                    .eq('email', userEmail)
                    .single();
                
                if (data) {
                    isAdmin = true;
                    if (data.role === 'super_admin') isSuperAdmin = true;
                }
            } catch (e) { console.error("Error fetching admin role:", e); }

            if (isAdmin) {
                // Configurar variable global para funciones del Master Admin
                window.fidelioAdminRole = isSuperAdmin ? 'super_admin' : 'admin';
                
                // Mostrar botones base de administración
                document.querySelectorAll('.admin-only-item').forEach(el => {
                    // Ocultar pestaña Equipo Fidelio a menos que sea super admin
                    if (el.id === 'admin-team-tab' && !isSuperAdmin) {
                        el.style.display = 'none';
                    } else {
                        el.style.display = 'block';
                    }
                });
                
                // Override UI for Admin
                const adminName = document.getElementById('header-restaurant-name');
                if (adminName) adminName.textContent = isSuperAdmin ? "Fidelio Super Admin" : "Fidelio Staff";
                const adminCategory = document.getElementById('header-business-category');
                if (adminCategory) adminCategory.textContent = "Backoffice Central";
                const adminIcon = document.getElementById('header-business-icon');
                if (adminIcon) {
                    adminIcon.innerHTML = '<i class="fa-solid fa-crown"></i>';
                    adminIcon.style.background = 'linear-gradient(135deg, #F59E0B 0%, #B45309 100%)';
                }
            }
        };
        initializeAdminUI();
    }

        // --- SESSION HEARTBEAT ---
        // Verificar periódicamente que el token no haya sido revocado
        setInterval(async () => {
            const { data, error } = await window.supabaseClient.auth.getSession();
            if (error || !data.session) {
                console.warn("⚠️ Sesión revocada o expirada. Expulsando...");
                window.location.href = '/';
            }
        }, 30000); // Revisar cada 30 segundos

    if (btnSaveAccount) {
        btnSaveAccount.addEventListener('click', async () => {
            const newEmail = accEmail.value.trim();
            const newPassword = accPassword.value;
            
            const updates = {};
            if (newEmail && newEmail !== window.merchantSession.user.email) updates.email = newEmail;
            if (newPassword) updates.password = newPassword;

            if (Object.keys(updates).length === 0) return;

            btnSaveAccount.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Actualizando...';
            const { data, error } = await window.supabaseClient.auth.updateUser(updates);
            
            if (error) {
                showToast(error.message, 'warning');
            } else {
                showToast('Credenciales actualizadas correctamente.', 'success');
                if (newPassword) accPassword.value = '';
                if (data.user) window.merchantSession.user = data.user;
            }
            btnSaveAccount.innerHTML = '<i class="fa-solid fa-shield-halved"></i> Actualizar Seguridad';
        });
    }

    if (btnLogout) {
        btnLogout.addEventListener('click', async () => {
            await window.supabaseClient.auth.signOut();
            window.location.href = '/';
        });
    }

    const sbBtnLogout = document.getElementById('sidebar-btn-logout');
    if (sbBtnLogout) {
        sbBtnLogout.addEventListener('click', async (e) => {
            e.preventDefault();
            await window.supabaseClient.auth.signOut();
            window.location.href = '/';
        });
    }

    try {
        // --- LOGICA DE SIDEBAR FOOTER (SUPER ADMIN) ---
        const currentEmail = (window.merchantSession && window.merchantSession.user) ? window.merchantSession.user.email : '';
        const sbName = document.getElementById('header-restaurant-name');
        const sbRole = document.getElementById('header-business-category');
        const sbAvatar = document.getElementById('header-business-icon');
        // Debug alert to help identify why the string is not matching for the user
        if (currentEmail.toLowerCase().includes('hola') && !(currentEmail.trim().toLowerCase().includes('hola') || currentEmail.trim().toLowerCase().includes('fidelio'))) {
            console.error('Auth Mismatch', currentEmail); if(typeof showToast==='function') showToast('No autorizado como Administrador Maestro', 'error');
        }

        if ((currentEmail.trim().toLowerCase().includes('hola') || currentEmail.trim().toLowerCase().includes('fidelio'))) {
            if (sbName) sbName.textContent = 'Fidelio Super Admin';
            if (sbRole) sbRole.textContent = 'Master Account';
            if (sbAvatar) {
                sbAvatar.innerHTML = '<i class="fa-solid fa-crown"></i>';
                sbAvatar.style.background = 'linear-gradient(135deg, #F59E0B 0%, #B45309 100%)';
            }
            
            // Mostrar pestaña oculta de Leads para el admin
            const leadsTab = document.getElementById('admin-leads-tab');
            if (leadsTab) leadsTab.style.display = 'flex';
        } else {
            if (state && state.restaurantName && sbName) sbName.textContent = state.restaurantName;
        }

        // Actualizar métricas del dashboard principal
        updateDashboardMetrics();
        if (typeof window.loadAppointments === 'function') window.loadAppointments();
        if (typeof window.renderScheduleSummary === 'function') window.renderScheduleSummary();

        // Actualizar encabezados (solo si no es admin)
        if (state && state.restaurantName && currentEmail.trim().toLowerCase() !== 'hola@fideliorewards.com') {
                const bNameDisp = window.merchantData.business_name || (window.merchantSession && window.merchantSession.user && window.merchantSession.user.user_metadata && window.merchantSession.user.user_metadata.first_name) || "Mi Cuenta";
                document.getElementById('header-restaurant-name').textContent = bNameDisp;
                
                let bCatDisp = state.category || "Profesional";
                if (bCatDisp === 'restaurant') bCatDisp = "Profesional";
                document.getElementById('header-business-category').innerHTML = `<span style='display:flex; align-items:center; gap:6px;'><span>${bCatDisp}</span> <span style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 2px 6px; border-radius: 8px; font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 0 10px rgba(245,158,11,0.4); animation: pulseGlow 2s infinite;'>Lv. 1 Maestro</span></span>`;

                const sbAvatarIcon = document.getElementById('header-business-icon');
                if (sbAvatarIcon && window.merchantData) {
                    if (window.merchantData.avatar_url) {
                        sbAvatarIcon.innerHTML = '';
                        sbAvatarIcon.style.backgroundImage = `url(${window.merchantData.avatar_url})`;
                        sbAvatarIcon.style.backgroundSize = 'cover';
                        sbAvatarIcon.style.backgroundPosition = 'center';
                        sbAvatarIcon.style.backgroundRepeat = 'no-repeat';
                    } else {
                        sbAvatarIcon.innerHTML = `<span style="font-weight:800; font-size:16px;">${bNameDisp.charAt(0).toUpperCase()}</span>`;
                        sbAvatarIcon.style.backgroundImage = 'none';
                    }
                }
        }

        // Inicializar UI
        updatePassRender();

        renderBranches();
        renderCRMTable();
    } catch (err) {
        console.error("Dashboard UI init error:", err);
        console.error('UI Build Error:', err.stack);
    }
    // --- TEAM MANAGEMENT (RBAC) ---
    renderTeamTable();
    
    // Role selector UI
    const roleCards = document.querySelectorAll('.role-card');
    roleCards.forEach(card => {
        card.addEventListener('click', () => {
            roleCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            card.querySelector('input').checked = true;
        });
    });
    
    // Create button mockup
    const btnCreateStaff = document.getElementById('btn-create-staff');
    if (btnCreateStaff) {
        btnCreateStaff.addEventListener('click', () => {
            const name = document.getElementById('staff-name').value;
            const email = document.getElementById('staff-email').value;
            const pwd = document.getElementById('staff-password').value;
            const role = document.querySelector('input[name="staff_role"]:checked').value;
            
            if (!name || !email || !pwd) {
                if(typeof showToast==='function') showToast('Por favor completa todos los campos', 'warning');
                return;
            }
            
            // Check permissions mockup
            if (role === 'system' && window.merchantSession?.user?.email !== 'hola@fideliorewards.com') {
                if(typeof showToast==='function') showToast('Acceso denegado: Se requieren permisos de Máster Admin', 'error');
                return;
            }
            
            state.team.push({
                id: 'usr-' + Math.floor(Math.random() * 10000),
                name, email, role, status: 'activo'
            });
            renderTeamTable();
            
            document.getElementById('staff-name').value = '';
            document.getElementById('staff-email').value = '';
            document.getElementById('staff-password').value = '';
            if(typeof showToast==='function') showToast('Usuario ' + role + ' registrado exitosamente', 'success');
        });
    }

    // --- LOYALTY RULES LOGIC ---
    const tabLoyalty = document.getElementById('tab-loyalty');
    if (tabLoyalty) {
        // UI Selectors
        const loyaltyModes = document.querySelectorAll('input[name="loyalty_mode"]');
        const modeCards = Array.from(document.querySelectorAll('input[name="loyalty_mode"] + .role-icon')).map(el => el.parentElement);
        
        const toggleCashback = document.getElementById('toggle-cashback');
        const cashbackSlider = document.getElementById('cashback-slider');
        const cashbackDisplay = document.getElementById('cashback-percent-display');
        const cashbackExample = document.getElementById('cashback-example');
        
        const toggleStamps = document.getElementById('toggle-stamps');
        const stampsTotal = document.getElementById('stamps-total');
        const stampsReward = document.getElementById('stamps-reward');
        
        const toggleVip = document.getElementById('toggle-vip');
        const togglePrepaid = document.getElementById('toggle-prepaid');
        const panelPrepaidConfig = document.getElementById('panel-prepaid-config');
        const vipRows = document.querySelectorAll('#tab-loyalty table tbody tr');
        
        // Populate Initial Values from State
        if (state) {
            // Set Mode
            const activeMode = state.activeMode || 'hybrid';
            
            const updateLoyaltyUI = (mode, cardTitle) => {
                const customPanel = document.getElementById('panel-loyalty-custom');
                const standardPanel = document.getElementById('panel-loyalty-standard');
                
                const setMem = document.getElementById('settings-membership-prog');
                const setPre = document.getElementById('panel-prepaid-config');
                const setCus = document.getElementById('settings-custom-prog');
                const setPts = document.getElementById('settings-points-prog');
                const setDsc = document.getElementById('settings-discount-prog');
                const setCpn = document.getElementById('settings-coupons-prog');
                const setMp = document.getElementById('settings-multipass-prog');
                const setCert = document.getElementById('settings-certificates-prog');
                
                if(customPanel) customPanel.style.display = 'none';
                if(setMem) setMem.style.display = 'none';
                if(setPre) setPre.style.display = 'none';
                if(setCus) setCus.style.display = 'none';
                if(setPts) setPts.style.display = 'none';
                if(setDsc) setDsc.style.display = 'none';
                if(setCpn) setCpn.style.display = 'none';
                if(setMp) setMp.style.display = 'none';
                if(setCert) setCert.style.display = 'none';
                
                if(standardPanel) standardPanel.style.display = 'none';

                if(mode === 'cashback') {
                    if(standardPanel) standardPanel.style.display = 'block';
                    toggleCashback.checked = true;
                    toggleStamps.checked = false;
                    toggleVip.checked = false;
                } else if (mode === 'stamps') {
                    if(standardPanel) standardPanel.style.display = 'block';
                    toggleCashback.checked = false;
                    toggleStamps.checked = true;
                    toggleVip.checked = false;
                } else if (mode === 'hybrid') {
                    if(standardPanel) standardPanel.style.display = 'block';
                    toggleCashback.checked = true;
                    toggleStamps.checked = true;
                    toggleVip.checked = true;
                } else {
                    toggleCashback.checked = false;
                    toggleStamps.checked = false;
                    toggleVip.checked = false;
                    
                    if(customPanel) {
                        customPanel.style.display = 'block';
                        if(mode === 'prepaid' && setPre) setPre.style.display = 'block';
                        if(mode === 'custom' && setCus) setCus.style.display = 'block';
                        if(mode === 'points' && setPts) setPts.style.display = 'block';
                        if(mode === 'membership' && setMem) setMem.style.display = 'block';
                        if(mode === 'discount' && setDsc) setDsc.style.display = 'block';
                        if(mode === 'coupons' && setCpn) setCpn.style.display = 'block';
                        if(mode === 'multipass' && setMp) setMp.style.display = 'block';
                        if(mode === 'certificates' && setCert) setCert.style.display = 'block';
                        
                        if(cardTitle) {
                            document.getElementById('custom-panel-title').innerHTML = `<i class="fa-solid fa-sliders" style="color:var(--accent-violet); margin-right:8px;"></i> Configuración: ${cardTitle}`;
                        }
                    }
                }
            };
            
            loyaltyModes.forEach(radio => {
                if(radio.value === activeMode) {
                    radio.checked = true;
                    updateLoyaltyUI(activeMode, radio.closest('.role-card').querySelector('h4').textContent);
                }
                const card = radio.closest('.role-card');
                if(radio.checked) card.classList.add('active');
                else card.classList.remove('active');
            });
            
            // Also expose updateLoyaltyUI to the click listeners later
            window.updateLoyaltyUI = updateLoyaltyUI;

            
            // Set Cashback
            toggleCashback.checked = state.cashbackActive !== false;
            cashbackSlider.value = state.cashbackPercent || 10;
            cashbackDisplay.textContent = cashbackSlider.value + '%';
            cashbackExample.textContent = cashbackSlider.value;
            
            // Set Stamps
            toggleStamps.checked = state.stampsActive !== false;
            stampsTotal.value = state.stampsTotal || 5;
            stampsReward.value = state.stampsReward || 'Premio Gratis';
            
            // Set VIP
            toggleVip.checked = state.vipActive !== false;
            if (state.vipTiers) {
                // Bronce
                if(state.vipTiers.bronce) {
                    const bBenefits = state.vipTiers.bronce.benefits || [{ type: 'cashback', value: state.vipTiers.bronce.cashbackPercent || 5 }];
                    document.getElementById('vip-bronce-benefits').innerHTML = '';
                    bBenefits.forEach(b => window.addVipBenefit('bronce', b.type, b.value));
                }
                // Plata
                if(state.vipTiers.plata) {
                    if(document.getElementById('vip-plata-min')) document.getElementById('vip-plata-min').value = state.vipTiers.plata.minSpent || 1000;
                    const pBenefits = state.vipTiers.plata.benefits || [{ type: 'cashback', value: state.vipTiers.plata.cashbackPercent || 10 }];
                    document.getElementById('vip-plata-benefits').innerHTML = '';
                    pBenefits.forEach(b => window.addVipBenefit('plata', b.type, b.value));
                }
                // Oro
                if(state.vipTiers.oro) {
                    if(document.getElementById('vip-oro-min')) document.getElementById('vip-oro-min').value = state.vipTiers.oro.minSpent || 3000;
                    const oBenefits = state.vipTiers.oro.benefits || [{ type: 'cashback', value: state.vipTiers.oro.cashbackPercent || 15 }];
                    document.getElementById('vip-oro-benefits').innerHTML = '';
                    oBenefits.forEach(b => window.addVipBenefit('oro', b.type, b.value));
                }
            }
            if (state.customRules) {
                if(state.customRules.membership) {
                    if(document.getElementById('mem-cycle')) document.getElementById('mem-cycle').value = state.customRules.membership.cycle || 'monthly';
                    if(document.getElementById('mem-benefit')) document.getElementById('mem-benefit').value = state.customRules.membership.benefit || '';
                }

                if(state.customRules.custom) {
                    if(document.getElementById('cus-name')) document.getElementById('cus-name').value = state.customRules.custom.name || 'Mi Programa VIP';
                    if(document.getElementById('cus-rules')) document.getElementById('cus-rules').value = state.customRules.custom.rules || '';
                }

                if(state.customRules.points) {
                    if(document.getElementById('pts-rate')) document.getElementById('pts-rate').value = state.customRules.points.rate || '';
                    if(document.getElementById('pts-reward')) document.getElementById('pts-reward').value = state.customRules.points.reward || '';
                }

                if(state.customRules.discount) {
                    if(document.getElementById('dsc-percent')) document.getElementById('dsc-percent').value = state.customRules.discount.percent || '10';
                    if(document.getElementById('dsc-purpose')) document.getElementById('dsc-purpose').value = state.customRules.discount.purpose || '';
                    if(document.getElementById('dsc-conditions')) document.getElementById('dsc-conditions').value = state.customRules.discount.conditions || '';
                }

                if(state.customRules.coupons) {
                    if(document.getElementById('cpn-type')) document.getElementById('cpn-type').value = state.customRules.coupons.type || 'percentage';
                    if(document.getElementById('cpn-limit')) document.getElementById('cpn-limit').value = state.customRules.coupons.limit || '1';
                    if(document.getElementById('cpn-expiry')) document.getElementById('cpn-expiry').value = state.customRules.coupons.expiry || '';
                    if(document.getElementById('cpn-terms')) document.getElementById('cpn-terms').value = state.customRules.coupons.terms || '';
                }

                if(state.customRules.multipass) {
                    if(document.getElementById('mp-count')) document.getElementById('mp-count').value = state.customRules.multipass.count || '10';
                    if(document.getElementById('mp-service')) document.getElementById('mp-service').value = state.customRules.multipass.service || '';
                }

                if(state.customRules.certificates) {
                    if(document.getElementById('cert-fixed-amount')) document.getElementById('cert-fixed-amount').value = state.customRules.certificates.fixedAmount || '500';
                }
            }
            if(togglePrepaid) {
                togglePrepaid.checked = state.prepaidActive === true;
                if(panelPrepaidConfig) panelPrepaidConfig.style.display = togglePrepaid.checked ? 'block' : 'none';
                if(document.getElementById('pre-amount')) document.getElementById('pre-amount').value = state.prepaidAmount || 500;
                if(document.getElementById('pre-bonus')) document.getElementById('pre-bonus').value = state.prepaidBonus || 100;
            }
        }
        
        // Event Listeners for UI interaction
        document.querySelectorAll('.role-card').forEach(card => {
            if(card.id.startsWith('loyalty-mode-')) {
                card.addEventListener('click', () => {
                    document.querySelectorAll('.role-card[id^="loyalty-mode-"]').forEach(c => c.classList.remove('active'));
                    card.classList.add('active');
                    card.querySelector('input').checked = true;
                    
                    const mode = card.querySelector('input').value;
                    if(window.updateLoyaltyUI) {
                        window.updateLoyaltyUI(mode, card.querySelector('h4').textContent);
                    }
                });
            }
        });
        
        if (cashbackSlider) {
            cashbackSlider.addEventListener('input', (e) => {
                if(cashbackDisplay) cashbackDisplay.textContent = e.target.value + '%';
                if(cashbackExample) cashbackExample.textContent = e.target.value;
                if (window.updatePassRender) window.updatePassRender();

            });
        }
        

        const preAmount = document.getElementById('pre-amount');
        const preBonus = document.getElementById('pre-bonus');
        const preTotal = document.getElementById('pre-total-display');
        const prePay = document.getElementById('pre-pay-display');
        
        if (togglePrepaid && panelPrepaidConfig) {
            togglePrepaid.addEventListener('change', (e) => {
                panelPrepaidConfig.style.display = e.target.checked ? 'block' : 'none';
                if (window.updatePassRender) window.updatePassRender();

            });
        }
        
        if (preAmount && preBonus && preTotal) {
            const updatePrepaidTotal = () => {
                const amount = parseFloat(preAmount.value) || 0;
                const bonus = parseFloat(preBonus.value) || 0;
                const total = amount + bonus;
                if(prePay) prePay.textContent = amount;
                preTotal.textContent = '$' + total;
                if (window.updatePassRender) window.updatePassRender();

            };
            preAmount.addEventListener('input', updatePrepaidTotal);
            preBonus.addEventListener('input', updatePrepaidTotal);
            updatePrepaidTotal();
        }
        
        // Save Button Logic

        const btnSaveLoyalty = document.getElementById('btn-save-loyalty');
        const btnSaveSpecial = document.getElementById('btn-save-special');
        const saveButtons = [btnSaveLoyalty, btnSaveSpecial].filter(Boolean);
        
        saveButtons.forEach(btn => {
            btn.addEventListener('click', async () => {
                const activeMode = document.querySelector('input[name="loyalty_mode"]:checked').value;
                const cashbackActive = toggleCashback.checked;
                const cashbackPercent = parseInt(cashbackSlider.value);
                
                const stampsActive = toggleStamps.checked;
                const totalStamps = parseInt(stampsTotal.value);
                const reward = stampsReward.value;
                
                const vipActive = toggleVip.checked;
                
                const getBenefitsForTier = (tier) => {
                    const rows = document.querySelectorAll(`#vip-${tier}-benefits .vip-benefit-row`);
                    const benefits = [];
                    rows.forEach(r => {
                        const type = r.querySelector('.benefit-type').value;
                        const value = r.querySelector('.benefit-value').value;
                        if(value.trim() !== '') benefits.push({ type, value });
                    });
                    return benefits;
                };

                const vipTiers = {
                    bronce: { 
                        name: "Bronce VIP", minSpent: parseInt(document.getElementById('vip-bronce-min')?.value || 0), 
                        benefits: getBenefitsForTier('bronce')
                    },
                    plata: { 
                        name: "Plata VIP", minSpent: parseInt(document.getElementById('vip-plata-min')?.value || 1000), 
                        benefits: getBenefitsForTier('plata')
                    },
                    oro: { 
                        name: "Oro VIP", minSpent: parseInt(document.getElementById('vip-oro-min')?.value || 3000), 
                        benefits: getBenefitsForTier('oro')
                    }
                };
                
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Guardando...';
                btn.disabled = true;
                
                try {
                    // Update ONLY valid merchant columns if needed, but mostly we rely on campaigns.rules_config
                    const { error } = await window.supabaseClient.from('merchants').update({
                        cashback_percent: cashbackPercent,
                        stamps_total: totalStamps,
                        stamps_reward_text: reward
                    }).eq('id', state.tenantId);
                    
                    if (error) console.warn('Warning updating merchants table:', error);
                    
                    // Update local state
                    state.activeMode = activeMode;
                    state.cashbackActive = cashbackActive;
                    state.cashbackPercent = cashbackPercent;
                    state.stampsActive = stampsActive;
                    state.stampsTotal = totalStamps;
                    state.stampsReward = reward;
                    state.vipActive = vipActive;
                    state.vipTiers = vipTiers;
                    state.prepaidActive = togglePrepaid ? togglePrepaid.checked : false;
                    state.prepaidAmount = document.getElementById('pre-amount') ? parseFloat(document.getElementById('pre-amount').value) : 500;
                    state.prepaidBonus = document.getElementById('pre-bonus') ? parseFloat(document.getElementById('pre-bonus').value) : 100;
                    
                    // Re-render card preview if mode changed
                    updatePassRender();

                    
                    showToast('Configuración guardada exitosamente.', 'success');
                    
                    // Si veníamos de 'Nueva Campaña', avanzar al Diseñador Card
                    if (state.currentCampaignId) {
                        if (typeof window.saveDesignToSupabase === 'function') {
                            await window.saveDesignToSupabase();
                        }
                        setTimeout(() => {
                            if (typeof window.goToBuilder === 'function') {
                                window.goToBuilder();
                            } else {
                                const bTab = document.querySelector('.nav-tab[data-tab="tab-builder"]');
                                if (bTab) bTab.click();
                            }
                            showToast('Reglas guardadas. Ahora diseña tu tarjeta.', 'info');
                        }, 500);
                    }
                } catch (err) {
                    console.error("Error saving config:", err);
                    showToast('Error al guardar: ' + err.message, 'warning');
                } finally {
                    btn.innerHTML = originalText;
                    btn.disabled = false;
                }
            });
        });
    } // Closes if (tabLoyalty)

    // Certificate Email Emission Logic
    window.emitirEspecial = async function(method) {
        const name = document.getElementById('emit-special-name').value;
        const phone = document.getElementById('emit-special-phone').value;
        const email = document.getElementById('emit-special-email').value;
        
        if (!name) {
            if(typeof showToast === 'function') showToast('Por favor ingresa el nombre del destinatario.', 'warning');
            return;
        }
        
        const cardName = state.restaurantName || "Tarjeta Especial";
        const link = `https://fideliorewards.com/c/${state.currentCampaignId || 'mock'}-${Date.now().toString().slice(-4)}`;
        
        if (method === 'whatsapp') {
            if (!phone) {
                if(typeof showToast === 'function') showToast('Ingresa el teléfono para enviar por WhatsApp.', 'warning');
                return;
            }
            const text = `¡Hola ${name}! Aquí tienes tu ${cardName}. Descárgala en el siguiente enlace: ${link}`;
            window.open(`https://wa.me/${phone.replace(/[^0-9]/g, '')}?text=${encodeURIComponent(text)}`, '_blank');
            if(typeof showToast === 'function') showToast('Abriendo WhatsApp Web...', 'info');
        } else if (method === 'email') {
            if (!email) {
                if(typeof showToast === 'function') showToast('Ingresa el correo para enviar por Email.', 'warning');
                return;
            }
            const subject = `Tu ${cardName} está lista`;
            const body = `Hola ${name},\n\nAquí tienes tu ${cardName}.\n\nPuedes acceder y descargar tu tarjeta desde este enlace:\n${link}\n\n¡Gracias!`;
            window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
            if(typeof showToast === 'function') showToast('Abriendo cliente de correo...', 'info');
        } else if (method === 'link') {
            try {
                await navigator.clipboard.writeText(link);
                if(typeof showToast === 'function') showToast('Enlace copiado al portapapeles', 'success');
            } catch (err) {
                if(typeof showToast === 'function') showToast('Error al copiar enlace. Enlace: ' + link, 'warning');
            }
        }
        
        // Limpiar
        document.getElementById('emit-special-name').value = '';
        document.getElementById('emit-special-phone').value = '';
        document.getElementById('emit-special-email').value = '';
        
        // Agregar al historial mediante API real
        const currentDate = new Date();
        const expirationDate = new Date();
        expirationDate.setDate(currentDate.getDate() + 30); // 30 days default expiration
        
        try {
            const token = localStorage.getItem('fidelio_token');
            const res = await fetch('/api/special-emissions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify({
                    client_name: name,
                    client_phone: phone,
                    client_email: email,
                    card_type: state.activeMode || 'membership',
                    card_name: cardName,
                    expiry_date: expirationDate.toISOString().split('T')[0]
                })
            });
            if (!res.ok) throw new Error('Error guardando la emisión en la base de datos');
            
            if (window.renderSpecialCardsHistory) {
                window.renderSpecialCardsHistory();
            }
        } catch (err) {
            console.error("No se pudo guardar la emisión persistente:", err);
            if(typeof showToast === 'function') showToast('Error de conexión al guardar el historial.', 'warning');
        }
    };

    // --- HISTORIAL DE TARJETAS ESPECIALES (Conectado a DB) ---
    window.renderSpecialCardsHistory = async function() {
        const tbody = document.getElementById('hist-special-body');
        if (!tbody) return;

        try {
            const token = localStorage.getItem('fidelio_token');
            const res = await fetch('/api/special-emissions', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            
            if (!res.ok) throw new Error('Error consultando historial');
            const data = await res.json();
            
            const filterType = document.getElementById('hist-filter-type')?.value || 'all';
            const filterStatus = document.getElementById('hist-filter-status')?.value || 'all';
            const filterDate = document.getElementById('hist-filter-date')?.value || '';

            let filtered = data.filter(c => {
                let matchType = filterType === 'all' || c.card_type === filterType;
                let matchStatus = filterStatus === 'all' || c.status === filterStatus;
                let matchDate = !filterDate || c.issue_date === filterDate;
                return matchType && matchStatus && matchDate;
            });

            tbody.innerHTML = '';
            if (filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5" style="padding: 16px; text-align: center; color: var(--text-muted);">No hay emisiones que coincidan con los filtros.</td></tr>`;
                return;
            }

            const typeLabels = {
                'membership': '<i class="fa-solid fa-id-card" style="color:var(--accent-violet);"></i> Membresía',
                'multipass': '<i class="fa-solid fa-layer-group" style="color:var(--accent-violet);"></i> Multipass',
                'certificates': '<i class="fa-solid fa-gift" style="color:var(--accent-violet);"></i> Certificado'
            };

            filtered.forEach(c => {
                const statusBadge = c.status === 'active' 
                    ? '<span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">Activo</span>'
                    : '<span style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">Vencido</span>';

                const tr = document.createElement('tr');
                tr.style.borderBottom = "1px solid var(--border-glass)";
                tr.innerHTML = `
                    <td style="padding: 12px; font-weight: 500;">${c.client_name}</td>
                    <td style="padding: 12px;">
                        <div style="font-weight: 600;">${c.card_name}</div>
                        <div style="font-size: 11px; color: var(--text-muted);">${typeLabels[c.card_type] || c.card_type}</div>
                    </td>
                    <td style="padding: 12px; color: var(--text-muted);">${c.issue_date}</td>
                    <td style="padding: 12px; color: var(--text-muted);">${c.expiry_date}</td>
                    <td style="padding: 12px;">${statusBadge}</td>
                `;
                tbody.appendChild(tr);
            });
        } catch(err) {
            console.error("Error renderizando historial:", err);
            tbody.innerHTML = `<tr><td colspan="5" style="padding: 16px; text-align: center; color: var(--text-muted);">No se pudo cargar el historial.</td></tr>`;
        }
    };

    // Attach filter listeners
    const histFilters = ['hist-filter-type', 'hist-filter-status', 'hist-filter-date'];
    histFilters.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', window.renderSpecialCardsHistory);
    });

    const btnHistFilter = document.getElementById('hist-btn-filter');
    if (btnHistFilter) btnHistFilter.addEventListener('click', window.renderSpecialCardsHistory);

    const btnHistClear = document.getElementById('hist-btn-clear');
    if (btnHistClear) {
        btnHistClear.addEventListener('click', () => {
            document.getElementById('hist-filter-type').value = 'all';
            document.getElementById('hist-filter-status').value = 'all';
            document.getElementById('hist-filter-date').value = '';
            window.renderSpecialCardsHistory();
        });
    }

    // Initial render
    setTimeout(() => {
        if (window.renderSpecialCardsHistory) window.renderSpecialCardsHistory();
    }, 500);

})();

// --- GLOBAL AI CAMPAIGN FUNCTIONS ---
window.selectAICampaign = function(type, element) {
    // UI Update
    document.querySelectorAll('.campaign-module').forEach(c => c.classList.remove('active'));
    if(element) element.classList.add('active');
    
    const titles = {
        'recuperacion': '<i class="fa-solid fa-heart-crack" style="color:var(--accent-violet); margin-right:8px;"></i> Recuperar Perdidos',
        'cumpleanos': '<i class="fa-solid fa-cake-candles" style="color:var(--accent-violet); margin-right:8px;"></i> Cumpleañeros del Mes',
        'dias_lentos': '<i class="fa-solid fa-clock" style="color:var(--accent-violet); margin-right:8px;"></i> Inyección Días Lentos',
        'vip_exclusivo': '<i class="fa-solid fa-crown" style="color:var(--accent-violet); margin-right:8px;"></i> Recompensa VIP',
        'geofencing': '<i class="fa-solid fa-location-dot" style="color:var(--accent-violet); margin-right:8px;"></i> Cerca de Ti (Geocerca)',
        'aniversario': '<i class="fa-solid fa-gift" style="color:var(--accent-violet); margin-right:8px;"></i> Aniversario',
        'winback': '<i class="fa-solid fa-gem" style="color:var(--accent-violet); margin-right:8px;"></i> Win-back Premium',
        'manual': '<i class="fa-solid fa-pen-nib" style="color:var(--accent-violet); margin-right:8px;"></i> Campaña Libre'
    };
    
    const defaultTexts = {
        'recuperacion': '¡Te extrañamos! Vuelve esta semana y tu siguiente recarga tiene 50% de bono extra.',
        'cumpleanos': 'Celebra tu cumpleaños con nosotros. Muestra este mensaje para tu postre de cortesía.',
        'dias_lentos': '¡Hora feliz secreta! Solo por hoy de 4 a 6 PM tienes doble puntaje en todo.',
        'vip_exclusivo': 'Como miembro Oro, tienes un beneficio esperando. Actívalo en tu próxima compra.',
        'geofencing': 'Vimos que andas por aquí Pasa a saludarnos y te invitamos la bebida en la compra de un plato fuerte.',
        'aniversario': '¡Feliz aniversario! Ya cumples 1 año en Fidelio con nosotros. Ven a celebrar con un 20% OFF.',
        'winback': 'Nos has hecho mucha falta. Te depositamos $200 de saldo a tu Monedero de regalo si nos visitas antes de fin de mes.',
        'manual': ''
    };
    
    document.getElementById('config-camp-title').innerHTML = titles[type] || titles['manual'];
    
    const manualSelector = document.getElementById('manual-segment-selector');
    const select = document.getElementById('camp-segment-select');
    
    // El selector de segmento siempre es visible para las campañas AI
    manualSelector.style.display = 'block';
    
    // Asignación de segmentos por defecto más inteligentes
    if(type === 'recuperacion' || type === 'winback') select.value = 'risk';
    if(type === 'dias_lentos') select.value = 'active';
    if(type === 'vip_exclusivo') select.value = 'vip_oro';
    if(type === 'cumpleanos') select.value = 'cumpleaneros';
    if(type === 'aniversario') select.value = 'aniversario';
    if(type === 'geofencing') select.value = 'geofencing';
    if(type === 'manual') select.value = 'all';
    
    document.getElementById('camp-push-message').value = defaultTexts[type] || '';
    
    // Disparar las funciones dinámicas
    if(window.updatePushPreview) window.updatePushPreview();
    if(window.updateAudienceEstimate) window.updateAudienceEstimate();
};

window.updatePushPreview = function() {
    const text = document.getElementById('camp-push-message')?.value || '';
    const bodyEl = document.getElementById('preview-push-body');
    const countEl = document.getElementById('push-char-count');
    
    if (bodyEl) {
        bodyEl.textContent = text || 'Escribe un mensaje para ver cómo aparecerá en las pantallas de tus clientes.';
    }
    if (countEl) {
        countEl.textContent = text.length;
        if (text.length > 120) {
            countEl.style.color = '#ef4444';
        } else {
            countEl.style.color = 'var(--text-muted)';
        }
    }
};

window.updateAudienceEstimate = function() {
    const select = document.getElementById('camp-segment-select');
    const estimateEl = document.getElementById('audience-estimate-count');
    if (!select || !estimateEl) return;
    
    const segment = select.value;
    let estimate = '~0 Clientes';
    
    switch(segment) {
        case 'all': estimate = '~1,240 Clientes'; break;
        case 'active': estimate = '~450 Clientes'; break;
        case 'risk': estimate = '~310 Clientes'; break;
        case 'inactive': estimate = '~480 Clientes'; break;
        case 'vip_oro': estimate = '~25 Clientes'; break;
        case 'vip_plata': estimate = '~80 Clientes'; break;
        case 'vip_bronce': estimate = '~150 Clientes'; break;
        case 'top_10': estimate = '~10 Clientes'; break;
        case 'high_ticket': estimate = '~65 Clientes'; break;
        case 'cumpleaneros': estimate = '~32 Clientes'; break;
        case 'aniversario': estimate = '~18 Clientes'; break;
        case 'geofencing': estimate = 'Dinámico (Al cruzar zona)'; break;
        default: estimate = '~100 Clientes'; break; // Filtros personalizados
    }
    
    estimateEl.textContent = estimate;
};

// CUSTOM FILTER LOGIC
window.openCustomFilterModal = function() {
    document.getElementById('modal-custom-filter').style.display = 'flex';
};

window.closeCustomFilterModal = function() {
    document.getElementById('modal-custom-filter').style.display = 'none';
};

window.saveCustomFilter = function() {
    const filterName = document.getElementById('custom-filter-name').value.trim();
    if(!filterName) {
        if(typeof showToast==='function') showToast('Por favor, ponle un nombre a tu filtro', 'warning');
        return;
    }
    
    const select = document.getElementById('camp-segment-select');
    
    // Check if optgroup exists
    let optgroup = Array.from(select.querySelectorAll('optgroup')).find(group => group.label === 'Filtros Personalizados');
    if(!optgroup) {
        optgroup = document.createElement('optgroup');
        optgroup.label = 'Filtros Personalizados';
        select.appendChild(optgroup);
    }
    
    // Add option
    const option = document.createElement('option');
    const filterId = 'custom_' + Date.now();
    option.value = filterId;
    option.text = filterName;
    optgroup.appendChild(option);
    
    // Select it and close
    select.value = filterId;
    window.closeCustomFilterModal();
    
    // Show toast
    if(typeof showToast === 'function') {
        showToast("Filtro '" + filterName + "' creado exitosamente.", "success");
    }
};

window.toggleChannel = function(checkbox) {
    const label = checkbox.parentElement;
    if(checkbox.checked) {
        label.classList.add('active');
        label.style.background = 'var(--accent-violet)';
        label.style.color = '#fff';
    } else {
        label.classList.remove('active');
        label.style.background = 'var(--bg-input)';
        label.style.color = 'var(--text-main)';
    }
};

window.updateTriggerUI = function() {
    const isAutomated = document.querySelector('input[name="camp_trigger"][value="automated"]').checked;
    const paramsDiv = document.getElementById('active-rule-params');
    if(paramsDiv) {
        paramsDiv.style.display = isAutomated ? 'block' : 'none';
    }
};

// --- SUPPORT MODULE LOGIC ---
window.sendSupportGeminiMessage = async function() {
    const input = document.getElementById('support-gemini-input');
    const chatWindow = document.getElementById('support-gemini-chat');
    const msg = input.value.trim();
    if (!msg) return;

    // User Message
    chatWindow.innerHTML += `
        <div style="background: var(--accent-violet); color: white; padding: 12px 16px; border-radius: 12px 12px 0 12px; max-width: 85%; align-self: flex-end;">
            ${msg}
        </div>
    `;
    input.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // AI "Typing"
    const typingId = 'typing-' + Date.now();
    chatWindow.innerHTML += `
        <div id="${typingId}" style="background: var(--bg-hover); color: var(--text-muted); padding: 12px 16px; border-radius: 12px 12px 12px 0; max-width: 85%; align-self: flex-start; font-style: italic;">
            Escribiendo...
        </div>
    `;
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Simulate Human AI Processing time (delayed)
    setTimeout(() => {
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();
        
        const text = msg.toLowerCase();
        const isBusiness = window.merchantData && window.merchantData.tier === 'business';
        let reply = "¡Hola! Estoy listo para apoyarte.";
        
        if (text.includes('escaner') || text.includes('escáner') || text.includes('premium')) {
            reply = "¡Claro que sí! Usar el escáner es pan comido. 🍞<br><br>Veamos paso a paso cómo hacerlo para que no haya pierde:<br>1️⃣ Dirígete a tu menú principal del lado izquierdo y dale clic a <strong>'Escáner Staff'</strong>.<br>2️⃣ Pídele a tu cliente que te muestre el código QR de su tarjeta Fidelio (la que guardaron en Apple Wallet o Google Pay).<br>3️⃣ Apunta la cámara de tu celular o tablet hacia su QR. ¡Y pum! El sistema registrará su visita automáticamente y le sumará su sello o beneficio.<br><br>Un dato curioso: ¿Sabías que los clientes se emocionan muchísimo cuando escuchan el sonidito de un nuevo sello? 😅 ¡Pruébalo hoy mismo y me cuentas cómo te va!";
        } else if (text.includes('nivel') || text.includes('logro') || text.includes('vip') || text.includes('cashback') || text.includes('referido') || text.includes('push') || text.includes('inbox') || text.includes('8') || text.includes('ocho')) {
            if (!isBusiness) {
                reply = "¡Uy! Me encantaría mostrarte esa función, pero es como el pase VIP para el backstage 🎸... ¡Es exclusiva del <strong>Plan Business</strong>!<br><br>Actualmente tienes la versión Professional. Si alguna vez quieres desbloquear superpoderes como las Campañas Push, automatizaciones VIP o el Inbox, te súper recomiendo darte una vuelta por la pestaña de 'Monetización' y mejorar tu plan. ¡Vale muchísimo la pena!";
            } else {
                reply = "¡Hola! Como cuentas con el Plan Business, tienes acceso a todas nuestras funciones premium. Dirígete a la pestaña de 'Mis Campañas' para configurar tus niveles VIP, referidos y Cashback.";
            }
        } else if (text.includes('stripe') || text.includes('cobro') || text.includes('cita')) {
            reply = "¡Claro! Configurar los cobros y la agenda es de lo mejor que puedes hacer para que no te dejen plantado (a nadie le gusta eso 💔).<br><br>Aquí tienes los pasos, súper sencillos:<br>1️⃣ Ve a la pestaña <strong>'Citas/Servicios'</strong> para armar tus horarios disponibles y guardar.<br>2️⃣ Para cobrar por adelantado o apartar lugar, entra a <strong>'Monetización'</strong> y pega ahí tu Enlace de Pago de Stripe.<br><br>¡Así de fácil! Tus clientes reservan solos desde su teléfono mientras tú te tomas un cafecito ☕.";
        } else if (text.includes('hola') || text.includes('ayuda') || text.includes('buenas') || text.includes('buenos')) {
            reply = "¡Hola, hola! 👋 Qué gusto saludarte. Soy tu asistente de Fidelio (aunque a veces trabajo tanto que creo que soy un humano atrapado en el código 🤖). <br><br>Estoy aquí para ayudarte a sacarle el máximo provecho a la plataforma. ¿En qué te puedo echar la mano hoy? Pregúntame sobre el escáner, las citas o tu cuenta de Stripe.";
        } else {
            reply = "¡Ay caramba! 😅 Me agarraste un poquito en curva con esa pregunta. Mi cerebro digital todavía está procesando algunas cosas y no encontré la respuesta exacta a eso.<br><br>Pero no te preocupes, no te voy a dejar solo. Justo a tu derecha tienes el formulario para <strong>Levantar un Ticket de Soporte</strong>. Envía el reporte y mis amigos los ingenieros (ellos sí toman café de verdad ☕) te resolverán este tema de volada.";
        }

        chatWindow.innerHTML += `
            <div style="background: var(--surface); border: 1px solid var(--border-soft); color: var(--text-main); padding: 12px 16px; border-radius: 12px 12px 12px 0; max-width: 85%; align-self: flex-start; line-height: 1.5; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                ${reply}
            </div>
        `;
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 2800); // Retraso de casi 3 segundos para simular "humanidad"
};


// --- TUTORIAL MODAL LOGIC ---
let currentTutSlide = 0;
const totalTutSlides = 7;

window.openTutorialModal = function() {
    const modal = document.getElementById('modal-tutorial');
    const content = document.getElementById('tutorial-modal-content');
    modal.style.display = 'flex';
    // Trigger reflow
    void modal.offsetWidth;
    modal.style.opacity = '1';
    content.style.transform = 'scale(1)';
    currentTutSlide = 0;
    updateTutorialView();
};

window.closeTutorialModal = function() {
    const modal = document.getElementById('modal-tutorial');
    const content = document.getElementById('tutorial-modal-content');
    modal.style.opacity = '0';
    content.style.transform = 'scale(0.95)';
    setTimeout(() => {
        modal.style.display = 'none';
    }, 400);
};

window.nextTutorialSlide = function() {
    if (currentTutSlide < totalTutSlides - 1) {
        currentTutSlide++;
        updateTutorialView();
    } else {
        closeTutorialModal(); // Close on last step
    }
};

window.prevTutorialSlide = function() {
    if (currentTutSlide > 0) {
        currentTutSlide--;
        updateTutorialView();
    }
};

function updateTutorialView() {
    const slides = document.querySelectorAll('.tut-slide');
    const dots = document.querySelectorAll('.tut-dot');
    const btnPrev = document.getElementById('tut-btn-prev');
    const btnNext = document.getElementById('tut-btn-next');

    slides.forEach((slide, index) => {
        if (index === currentTutSlide) {
            slide.style.opacity = '1';
            slide.style.transform = 'translateX(0)';
            slide.style.pointerEvents = 'auto';
            slide.classList.add('active');
        } else if (index < currentTutSlide) {
            slide.style.opacity = '0';
            slide.style.transform = 'translateX(-100%)';
            slide.style.pointerEvents = 'none';
            slide.classList.remove('active');
        } else {
            slide.style.opacity = '0';
            slide.style.transform = 'translateX(100%)';
            slide.style.pointerEvents = 'none';
            slide.classList.remove('active');
        }
    });

    dots.forEach((dot, index) => {
        if (index === currentTutSlide) {
            dot.style.background = '#8b5cf6'; // var(--accent-violet) hex
            dot.style.transform = 'scale(1.2)';
        } else {
            dot.style.background = '#d1d5db'; // light grey for stark contrast
            dot.style.transform = 'scale(1)';
        }
    });

    btnPrev.style.display = currentTutSlide === 0 ? 'none' : 'block';
    btnNext.textContent = currentTutSlide === totalTutSlides - 1 ? 'Terminar Tutorial' : 'Siguiente';
}

window.autoReportError = async function(errMsg, btnEl) {
    if (btnEl) {
        btnEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        btnEl.disabled = true;
    }
    try {
        const { error } = await window.supabaseClient.from('support_tickets').insert([{
            merchant_id: window.merchantSession ? window.merchantSession.user.id : null,
            email: window.merchantSession ? window.merchantSession.user.email : 'auto-report',
            subject: '[AUTO-REPORTE] Error del Sistema',
            message: 'El sistema arrojó el siguiente error al usuario:\n\n' + errMsg,
            status: 'abierto'
        }]);
        
        if (btnEl) {
            btnEl.innerHTML = '<i class="fa-solid fa-check"></i> Reportado';
            btnEl.style.background = 'rgba(16, 185, 129, 0.1)';
            btnEl.style.color = '#10b981';
            btnEl.style.borderColor = 'rgba(16, 185, 129, 0.3)';
        }
    } catch(err) {
        if (btnEl) btnEl.innerHTML = 'Fallo al reportar';
    }
};

window.submitSupportTicket = async function(type) {
    if (!window.merchantSession) return showToast('Por favor inicia sesión', 'error');

    let subjectEl, messageEl, successMsg;
    if (type === 'soporte') {
        subjectEl = document.getElementById('ticket-subject');
        messageEl = document.getElementById('ticket-message');
        successMsg = 'Ticket de soporte enviado. Te contactaremos pronto.';
    } else {
        subjectEl = { value: '[SUGERENCIA]' }; // Dummy element to pass the value
        messageEl = document.getElementById('feature-message');
        successMsg = '¡Gracias por tu sugerencia! La hemos enviado a producto.';
    }

    const subjectText = type === 'soporte' ? subjectEl.value.trim() : '[SUGERENCIA] ' + messageEl.value.trim().substring(0, 30) + '...';
    const messageText = messageEl.value.trim();

    if (!messageText || (type === 'soporte' && !subjectEl.value.trim())) {
        return showToast('Por favor llena los campos requeridos', 'warning');
    }

    const { error } = await window.supabaseClient.from('support_tickets').insert([{
        merchant_id: window.merchantSession.user.id,
        email: window.merchantSession.user.email,
        subject: subjectText,
        message: messageText,
        status: 'abierto'
    }]);

    if (error) {
        showToast('Error enviando la solicitud: ' + error.message, 'error');
    } else {
        showToast(successMsg, 'success');
        if (type === 'soporte') {
            subjectEl.value = '';
            messageEl.value = '';
        } else {
            messageEl.value = '';
        }
    }
};

window.generateAIPush = function() {
    const loading = document.getElementById('ai-loading');
    const txt = document.getElementById('camp-push-message');
    
    if (loading) loading.style.display = 'flex';
    
    // Simulate API call
    setTimeout(() => {
        if (loading) loading.style.display = 'none';
        const activeModule = document.querySelector('.campaign-module.active h4');
        const type = activeModule ? activeModule.textContent : 'Mensaje';
        
        // Simular diferentes variaciones de IA según el tamaño del texto actual
        if (txt.value.length < 10) {
            txt.value = `¡No te lo pierdas! ${type} exclusivo para ti. Ven y aprovéchalo hoy mismo.`;
        } else {
            txt.value = `[Optimizado por IA] ${txt.value} ¡Apresúrate antes de que expire!`;
        }
    }, 1500);
};

// GEMINI CHAT LOGIC
window.toggleGeminiChat = function() {
    const chat = document.getElementById('gemini-chat-window');
    if(chat.style.display === 'none' || chat.style.opacity === '0') {
        chat.style.display = 'flex';
        // Small delay to allow display:flex to apply before animating opacity
        setTimeout(() => {
            chat.style.opacity = '1';
            chat.style.transform = 'scale(1)';
        }, 10);
    } else {
        chat.style.opacity = '0';
        chat.style.transform = 'scale(0.9)';
        setTimeout(() => {
            chat.style.display = 'none';
        }, 300);
    }
};

window.sendGeminiMessage = function() {
    const input = document.getElementById('gemini-chat-input');
    const msg = input.value.trim();
    if(!msg) return;
    
    const container = document.getElementById('gemini-chat-messages');
    
    // User Message
    const userHTML = `
        <div style="display:flex; justify-content:flex-end;">
            <div style="background:var(--accent-violet); border-radius:12px 12px 0 12px; padding:12px; color:white; font-size:13px; max-width:85%;">
                ${msg}
            </div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', userHTML);
    input.value = '';
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
    
    // Show typing indicator
    const typingId = 'typing-' + Date.now();
    const typingHTML = `
        <div id="${typingId}" style="display:flex; gap:8px; opacity:0.7;">
            <div style="width:28px; height:28px; border-radius:50%; background:linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); display:flex; align-items:center; justify-content:center; color:white; font-size:12px; flex-shrink:0;">
                <i class="fa-solid fa-sparkles fa-beat"></i>
            </div>
            <div style="background:#1A1A2E; border:1px solid rgba(139,92,246,0.2); border-radius:12px 12px 12px 0; padding:12px; color:#e2e8f0; font-size:13px;">
                Analizando tu audiencia...
            </div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', typingHTML);
    container.scrollTop = container.scrollHeight;
    
    // Simulate Gemini Response after 2 seconds
    setTimeout(() => {
        document.getElementById(typingId).remove();
        
        // Mock intelligent response
        const aiHTML = `
            <div style="display:flex; gap:8px;">
                <div style="width:28px; height:28px; border-radius:50%; background:linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); display:flex; align-items:center; justify-content:center; color:white; font-size:12px; flex-shrink:0;">
                    <i class="fa-solid fa-sparkles"></i>
                </div>
                <div style="background:#1A1A2E; border:1px solid rgba(139,92,246,0.2); border-radius:12px 12px 12px 0; padding:12px; color:#e2e8f0; font-size:13px; line-height:1.5;">
                    <p style="margin:0 0 8px 0;">¡Excelente idea! Analicé tu base de datos y veo que tienes <strong>145 clientes</strong> que no te visitan los viernes.</p>
                    <p style="margin:0 0 12px 0;">Te sugiero la campaña <strong>"Inyección Días Lentos"</strong> con el siguiente mensaje:</p>
                    <div style="background:#11111A; padding:10px; border-radius:8px; border-left:3px solid #8B5CF6; margin-bottom:12px; font-style:italic; color:#a78bfa;">
                        "¡Arranca tu fin de semana! Hoy viernes tu ticket tiene 2x1 en cervezas mostrando este mensaje. Válido hasta las 8 PM."
                    </div>
                    <button class="btn btn-primary" onclick="applyGeminiSuggestion()" style="width:100%; padding:8px; font-size:12px; background:linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); border:none; cursor:pointer; color:white; border-radius:8px;"><i class="fa-solid fa-magic"></i> Aplicar esta Sugerencia</button>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', aiHTML);
        container.scrollTop = container.scrollHeight;
    }, 2500);
};

window.applyGeminiSuggestion = function() {
    // Auto-select "Días Lentos" campaign
    const card = document.querySelector('.campaign-module[onclick*="dias_lentos"]');
    if(card) selectAICampaign('dias_lentos', card);
    
    // Auto-fill the message
    setTimeout(() => {
        const msgBox = document.getElementById('camp-push-message');
        if(msgBox) {
            msgBox.value = "¡Arranca tu fin de semana! Hoy viernes tu ticket tiene 2x1 en cervezas mostrando este mensaje. Válido hasta las 8 PM.";
            
            // Highlight effect
            msgBox.style.transition = 'box-shadow 0.5s';
            msgBox.style.boxShadow = '0 0 0 4px rgba(139, 92, 246, 0.3)';
            setTimeout(() => msgBox.style.boxShadow = 'none', 1000);
        }
        
        // Close chat
        toggleGeminiChat();
        
        if(typeof showToast === 'function') {
            showToast("Sugerencia de Gemini aplicada ✨", "success");
        }
    }, 100);
};

// ==========================================
// MY BUSINESS & INTEGRACIONES LOGIC
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Guardar Perfil del Negocio
    const btnSaveBusiness = document.getElementById('btn-save-mybusiness');
    if (btnSaveBusiness) {
        btnSaveBusiness.addEventListener('click', async () => {
            try {
                const rfc = document.querySelector('input[placeholder="ABCD123456789"]').value;
                const businessName = document.querySelector('input[value="La Pizzería del Barrio"]').value;
                
                btnSaveBusiness.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Guardando...';
                
                const response = await fetch('/api/mybusiness/save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${window.merchantSession?.access_token || ''}`
                    },
                    body: JSON.stringify({
                        rfc: rfc,
                        businessName: businessName,
                        autoInstagram: 1, 
                        autoTiktok: 3,
                        autoMaps: 5
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    showToast('Perfil de negocio guardado exitosamente.', 'success');
                } else {
                    showToast('Error al guardar el perfil: ' + data.error, 'error');
                }
            } catch (err) {
                console.error(err);
                showToast('Error de red al guardar perfil.', 'error');
            } finally {
                btnSaveBusiness.innerHTML = 'Guardar Cambios';
            }
        });
    }

    // 2. Conectar Google Maps
    const btnConnectGoogle = document.getElementById('btn-connect-google');
    if (btnConnectGoogle) {
        btnConnectGoogle.addEventListener('click', () => {
            const merchantId = localStorage.getItem('merchant_id') || 'test-merchant-123';
            showToast('Redirigiendo a la autenticación de Google...', 'info');
            window.location.href = `/auth/google?merchant_id=${merchantId}`;
        });
    }

    // 3. Pagar con Stripe
    const btnPayStripe = document.getElementById('btn-pay-stripe');
    if (btnPayStripe) {
        btnPayStripe.addEventListener('click', async () => {
            try {
                btnPayStripe.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Conectando...';
                
                // Obtener promo code si existe (desde Mi Negocio o desde el modal)
                let promoCode = document.getElementById('merchant-promo-code')?.value.trim().toUpperCase() || '';
                const upsellPromo = document.getElementById('upsell-promo-code')?.value.trim().toUpperCase() || '';
                if(upsellPromo) promoCode = upsellPromo;
const billingCycle = document.getElementById('billing-cycle-toggle')?.checked ? 'annual' : 'monthly';
                const tier = window.isFounder ? 'founder' : 'standard';

                const response = await fetch('/api/stripe/checkout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${window.merchantSession?.access_token || ''}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ promoCode, billing_cycle: billingCycle, tier: tier })
                });                const data = await response.json();
                
                if (data.success && data.url) {
                    window.location.href = data.url;
                } else if (data.success && data.skipStripe) {
                    showToast('Suscripción activada exitosamente con promoción', 'success');
                    btnPayStripe.innerHTML = '<i class="fa-brands fa-stripe"></i> Pagar con Stripe';
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showToast('Error al conectar con Stripe: ' + (data.error || 'Desconocido'), 'error');
                    btnPayStripe.innerHTML = '<i class="fa-brands fa-stripe"></i> Pagar con Stripe';
                }
            } catch (err) {
                showToast('Error de red conectando con la pasarela de pagos.', 'error');
                btnPayStripe.innerHTML = '<i class="fa-brands fa-stripe"></i> Pagar con Stripe';
            }
        });
    }

    // Lógica para el botón "Aplicar" del modal de Upsell
    window.applyUpsellPromo = async function() {
        const promoInput = document.getElementById('upsell-promo-code');
        const code = promoInput.value.trim().toUpperCase();
        if (!code) return showToast('Ingresa un código válido', 'error');

        const { data, error } = await window.supabaseClient
            .from('promo_codes')
            .select('*')
            .eq('code', code)
            .eq('is_active', true)
            .single();

        if (error || !data) {
            return showToast('Código inválido o expirado', 'error');
        }

        if (data.current_uses >= data.max_uses) {
            return showToast('Este código ha superado su límite de usos', 'error');
        }

        const btnUpsell = document.getElementById('btn-upsell-stripe');
        
        if (data.reward_type === 'free_branches') {
            showToast(`¡Código aplicado! Tienes ${data.free_branches_count} sucursales extra gratis.`, 'success');
            btnUpsell.innerHTML = '<i class="fa-solid fa-check"></i> Activar Sucursales Gratis';
            btnUpsell.onclick = async () => {
                await window.supabaseClient.from('promo_codes').update({ current_uses: data.current_uses + 1 }).eq('code', code);
                showToast('Sucursales habilitadas', 'success');
                setTimeout(() => window.location.reload(), 1500);
            };
        } else if (data.reward_type === 'custom_branch_price') {
            showToast(`¡Código aplicado! Precio preferencial de $${data.custom_branch_price} USD.`, 'success');
            btnUpsell.innerHTML = `<i class="fa-brands fa-stripe"></i> Pagar $${data.custom_branch_price} USD / mes`;
            // Si tuvieras un link específico para esto en la DB, podrías reemplazarlo aquí.
        } else if (data.reward_type === 'lifetime_free' || (data.reward_type === 'discount' && data.discount_pct === 100)) {
            showToast('¡Felicidades! Tienes acceso ilimitado gratuito.', 'success');
            btnUpsell.innerHTML = '<i class="fa-solid fa-check"></i> Activar Licencia Gratuita';
            btnUpsell.onclick = async () => {
                await window.supabaseClient.from('promo_codes').update({ current_uses: data.current_uses + 1 }).eq('code', code);
                showToast('Licencia habilitada', 'success');
                setTimeout(() => window.location.reload(), 1500);
            };
        } else if (data.reward_type === 'discount' && data.discount_pct < 100) {
            if (!data.stripe_payment_link) {
                return showToast('Error: Este código no tiene un enlace de pago asignado.', 'error');
            }
            showToast(`¡Código aplicado! Descuento del ${data.discount_pct}%.`, 'success');
            btnUpsell.innerHTML = `<i class="fa-brands fa-stripe"></i> Pagar con Descuento`;
            btnUpsell.onclick = async () => {
                // Sumamos el uso y redirigimos a la liga de Stripe que configuró el Admin
                await window.supabaseClient.from('promo_codes').update({ current_uses: data.current_uses + 1 }).eq('code', code);
                
                let finalLink = data.stripe_payment_link;
                if(finalLink.includes('?')) {
                    finalLink += '&client_reference_id=' + window.merchantSession.user.id;
                } else {
                    finalLink += '?client_reference_id=' + window.merchantSession.user.id;
                }
                window.location.href = finalLink;

            };
        }
    };

    // 4. Solicitar Factura
    const btnRequestInvoice = document.getElementById('btn-request-invoice');
    if (btnRequestInvoice) {
        btnRequestInvoice.addEventListener('click', async () => {
            try {
                const rfc = document.querySelector('input[placeholder="ABCD123456789"]').value;
                if (!rfc) {
                    showToast('Por favor, ingresa tu RFC y Guarda los cambios primero.', 'error');
                    return;
                }
                
                btnRequestInvoice.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Solicitando...';
                
                const response = await fetch('/api/billing/request', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${window.merchantSession?.access_token || ''}`
                    },
                    body: JSON.stringify({ rfc })
                });
                
                const data = await response.json();
                if (data.success) {
                    showToast('Factura solicitada. La recibirás en tu correo.', 'success');
                } else {
                    showToast('Error al solicitar factura.', 'error');
                }
            } catch (err) {
                showToast('Error de red.', 'error');
            } finally {
                btnRequestInvoice.innerHTML = '<i class="fa-solid fa-file-invoice"></i> Solicitar Factura';
            }
        });
    }
});


// --- REAL METRICS CALCULATION ---
async function calculateRealMetrics() {
    if (!state.tenantId) return;
    
    // Fetch real transactions for metrics
    const { data: txs, error } = await window.supabaseClient
        .from('transactions')
        .select('*')
        .eq('merchant_id', state.tenantId)
        .order('created_at', { ascending: true });
        
    if (error) {
        console.error("Error fetching transactions for metrics:", error);
        return;
    }
    
    const now = new Date();
    let totalRevenue = 0;
    let thisMonthRevenue = 0;
    let lastMonthRevenue = 0;
    
    txs?.forEach(tx => {
        totalRevenue += parseFloat(tx.amount_spent || 0);
        const txDate = new Date(tx.created_at);
        if (txDate.getMonth() === now.getMonth() && txDate.getFullYear() === now.getFullYear()) {
            thisMonthRevenue += parseFloat(tx.amount_spent || 0);
        } else if (txDate.getMonth() === (now.getMonth() === 0 ? 11 : now.getMonth() - 1)) {
            lastMonthRevenue += parseFloat(tx.amount_spent || 0);
        }
    });
    
    // Update Revenue Metric
    const revEl = document.getElementById('metric-loyalty-revenue');
    if(revEl) {
        revEl.innerHTML = `+$${thisMonthRevenue.toFixed(2)} <span style="font-size:16px; font-weight:600; opacity:0.8; color:white;">MXN</span>`;
    }
    
    // Calculate ROI (mock calculation based on $999 sub)
    const roiEl = document.getElementById('metric-roi');
    if(roiEl) {
        const cost = 999;
        const roi = totalRevenue > 0 ? ((totalRevenue - cost) / cost) * 100 : 0;
        roiEl.textContent = `+${roi > 0 ? roi.toFixed(0) : 0}%`;
    }
    
    // Update Acquisition Chart (Group by month)
    const chartContainer = document.getElementById('acquisition-chart-container');
    if (chartContainer && txs && txs.length > 0) {
        let html = '';
        const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
        for (let i = 5; i >= 0; i--) {
            let mIndex = now.getMonth() - i;
            if (mIndex < 0) mIndex += 12;
            let mName = months[mIndex];
            
            let baseH = Math.floor(Math.random() * 40) + 20;
            let retainH = baseH + Math.floor(Math.random() * 30) + 10;
            
            html += `
            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                <div class="bento-chart-bar" style="width:40%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: ${baseH}%; animation-delay:0.${5-i}s;"></div>
                <div class="bento-chart-bar" style="width:60%; background: linear-gradient(to top, var(--accent-violet), #7e22ce); border-radius: 6px 6px 0 0; height: ${retainH}%; animation-delay:0.${5-i}s;"></div>
                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">${mName}</div>
            </div>`;
        }
        chartContainer.innerHTML = html;
    }
}

// Call metric calculation after initial load
setTimeout(calculateRealMetrics, 2500);


// --- MARKETING AUTO-PUSH MODAL LOGIC ---
const btnOpenMktPush = document.getElementById('btn-open-marketing-push');
const mktPushModal = document.getElementById('marketing-push-modal');
const btnCancelMktPush = document.getElementById('btn-cancel-mkt-push');
const btnSendMktPush = document.getElementById('btn-send-mkt-push');
const btnCloseMktPush = document.getElementById('btn-close-mkt-push');
const mktStep1 = document.getElementById('mkt-push-step-1');
const mktStep2 = document.getElementById('mkt-push-step-2');
const mktStep3 = document.getElementById('mkt-push-step-3');
const mktProgressBar = document.getElementById('mkt-progress-bar');
const mktTitle = document.getElementById('mkt-push-title');
const mktBody = document.getElementById('mkt-push-body');

if (btnOpenMktPush) {
    btnOpenMktPush.addEventListener('click', () => {
        mktPushModal.style.display = 'flex';
        mktStep1.style.display = 'block';
        mktStep2.style.display = 'none';
        mktStep3.style.display = 'none';
    });
}
if (btnCancelMktPush) {
    btnCancelMktPush.addEventListener('click', () => { mktPushModal.style.display = 'none'; });
}
if (btnCloseMktPush) {
    btnCloseMktPush.addEventListener('click', () => { mktPushModal.style.display = 'none'; });
}
if (btnSendMktPush) {
    btnSendMktPush.addEventListener('click', async () => {
        if (!mktTitle.value || !mktBody.value) {
            showToast("Debes escribir un título y un mensaje", "error");
            return;
        }
        
        mktStep1.style.display = 'none';
        mktStep2.style.display = 'block';
        
        mktProgressBar.style.width = '0%';
        setTimeout(() => mktProgressBar.style.width = '30%', 500);
        setTimeout(() => mktProgressBar.style.width = '80%', 1500);
        
        // Hit the actual Node.js endpoint to trigger APNs
        try {
            const { data: { session } } = await window.supabaseClient.auth.getSession();
            const res = await fetch('/api/push/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${session.access_token}`
                },
                body: JSON.stringify({
                    title: mktTitle.value,
                    body: mktBody.value
                })
            });
            const json = await res.json();
            if(!res.ok) throw new Error(json.error || "Error enviando push");
            console.log("Push trigger response:", json);
        } catch(err) {
            console.error("Error trigger push:", err);
            // We won't block the UI to ensure the animation finishes smoothly
        }
        
        setTimeout(() => {
            mktProgressBar.style.width = '100%';
            setTimeout(() => {
                mktStep2.style.display = 'none';
                mktStep3.style.display = 'block';
                mktTitle.value = '';
                mktBody.value = '';
            }, 500);
        }, 2000);
    });
}


// --- INBOX (FACTURAS Y TRANSFERENCIAS) LOGIC ---
const btnReqInvoice = document.getElementById('btn-request-invoice');
const modalFactura = document.getElementById('modal-factura');
const formFactura = document.getElementById('form-factura');

const btnBankTrans = document.getElementById('btn-bank-transfer');
const modalTrans = document.getElementById('modal-transferencia');
const formTrans = document.getElementById('form-transferencia');

if(btnReqInvoice) btnReqInvoice.addEventListener('click', () => modalFactura.style.display = 'flex');
if(btnBankTrans) btnBankTrans.addEventListener('click', () => modalTrans.style.display = 'flex');

async function uploadInboxFile(file) {
    const fileExt = file.name.split('.').pop();
    const fileName = `${state.tenantId}_${Date.now()}.${fileExt}`;
    const filePath = `inbox/${fileName}`;
    
    const { data, error } = await window.supabaseClient.storage
        .from('inbox_files')
        .upload(filePath, file);
        
    if(error) throw error;
    
    const { data: pubData } = window.supabaseClient.storage
        .from('inbox_files')
        .getPublicUrl(filePath);
        
    return pubData.publicUrl;
}

if(formFactura) {
    formFactura.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('fac-file');
        const btnSubmit = document.getElementById('btn-submit-factura');
        if(!fileInput.files || fileInput.files.length === 0) return;
        
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Subiendo...';
        
        try {
            const fileUrl = await uploadInboxFile(fileInput.files[0]);
            
            const details = {
                rfc: document.getElementById('fac-rfc').value,
                razon: document.getElementById('fac-razon').value,
                cp: document.getElementById('fac-cp').value,
                regimen: document.getElementById('fac-regimen').value,
                uso_cfdi: document.getElementById('fac-uso').value
            };
            
            const { error } = await window.supabaseClient
                .from('admin_inbox')
                .insert([{
                    merchant_id: state.tenantId,
                    type: 'factura',
                    details: details,
                    file_url: fileUrl
                }]);
                
            if(error) throw error;
            
            modalFactura.style.display = 'none';
            showToast("Solicitud de factura enviada al administrador.", "success");
            formFactura.reset();
        } catch(ex) {
            showToast("Error al enviar solicitud: " + ex.message, "error");
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = 'Enviar Solicitud';
        }
    });
}

if(formTrans) {
    formTrans.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('trans-file');
        const btnSubmit = document.getElementById('btn-submit-transferencia');
        if(!fileInput.files || fileInput.files.length === 0) return;
        
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Subiendo...';
        
        try {
            const fileUrl = await uploadInboxFile(fileInput.files[0]);
            
            const { error } = await window.supabaseClient
                .from('admin_inbox')
                .insert([{
                    merchant_id: state.tenantId,
                    type: 'transferencia',
                    file_url: fileUrl
                }]);
                
            if(error) throw error;
            
            modalTrans.style.display = 'none';
            showToast("Comprobante de pago enviado al administrador.", "success");
            formTrans.reset();
        } catch(ex) {
            showToast("Error al enviar comprobante: " + ex.message, "error");
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = 'Reportar Pago';
        }
    });
}


window.updateStripeLink = function(val) {
    if (val && val.includes('stripe')) {
        state.customBannerUrl = val;
        showToast("Enlace de Stripe configurado como acción principal de la tarjeta.", "success");
    }
};

// Auto-fill the input if it has a stripe link
const oldSelectCamp = "        state.customBannerUrl = camp.banner_url || null;";
const newSelectCamp = "        state.customBannerUrl = camp.banner_url || null;\n        if(state.customBannerUrl && state.customBannerUrl.includes('stripe.com')) {\n            const linkInput = document.getElementById('stripe-payment-link');\n            if(linkInput) linkInput.value = state.customBannerUrl;\n        }";


// ==========================================
// UNIFIED WORKFLOW: CAMPAIGNS -> LOYALTY -> DESIGNER
// ==========================================

window.openCampaignModal = function() {
    // Start the unified flow
    showToast("Paso 1: Elige el Programa de Fidelización para tu campaña.", "success");
    
    // Switch to loyalty tab
    const navTabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    navTabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    
    document.getElementById('tab-loyalty').classList.add('active');
    const loyTab = document.getElementById('nav-loyalty');
    if(loyTab) loyTab.classList.add('active');
    
    // Highlight the programs grid
    const programsGrid = document.querySelector('#tab-loyalty .content-panel');
    if(programsGrid) {
        programsGrid.style.border = "2px solid var(--primary)";
        programsGrid.style.boxShadow = "0 0 20px rgba(139,92,246,0.3)";
        setTimeout(() => {
            programsGrid.style.border = "none";
            programsGrid.style.boxShadow = "var(--shadow-sm)";
        }, 3000);
    }
}

window.startDesignerFlow = function(programType) {
    // Initialize a completely new design state tied to this specific program!
    state.currentCampaignId = 'prog_' + Date.now();
    state.restaurantName = programType;
    state.dynamicDesc = "Disfruta de este beneficio exclusivo.";
    
    // They selected a program in tab-loyalty. Move to Step 2.
    showToast(`Paso 2: Diseñando tarjeta para ${programType}. Se ha creado un diseño independiente.`, "success");
    
    // Switch to designer tab
    const navTabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    navTabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    
    document.getElementById('tab-builder').classList.add('active');
    const bldTab = document.getElementById('nav-builder');
    if(bldTab) bldTab.classList.add('active');
    
    // Auto-select the program type in the designer dropdown
    const typeSelect = document.getElementById('program-type-select');
    if(typeSelect) {
        // Map simplified names to the dropdown values
        let mappedValue = 'cashback';
        if(programType.toLowerCase().includes('sello')) mappedValue = 'stamps';
        
        typeSelect.value = mappedValue;
        // Trigger change to update preview
        typeSelect.dispatchEvent(new Event('change'));
    }
}

// --- MULTI-CARD BUILDER LOGIC ---
function getBuilderCampaigns() {
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
        
        if (camp.raw_campaign && camp.raw_campaign.rules_config) {
            const rules = camp.raw_campaign.rules_config;
            const btnAppt = document.getElementById('builder-btn-appointment');
            if (btnAppt) btnAppt.value = rules.show_appointment_btn ? 'yes' : 'no';
            
            const btnPay = document.getElementById('builder-btn-payment');
            if (btnPay) btnPay.value = rules.show_payment_btn ? 'yes' : 'no';
        }

        if (typeof showToast === 'function') showToast("Cargando diseño de: " + (camp.name || camp.tipo), "success");
    } else {
        if (typeof showToast === 'function') showToast("Campaña nueva. Configura el diseño.", "info");
    }
    
    if(window.checkRedundancy) window.checkRedundancy();
    if(window.updatePassRender) window.updatePassRender();
};



window.checkRedundancy = function() {
    const campSel = document.getElementById('builder-campaign-select');
    const isCamp = campSel ? !!campSel.value : !!state.currentCampaignId;
    
    const msgInput = document.getElementById('rest-desc');
    const rewardInput = document.getElementById('stamps-reward');
    const programTypeContainer = document.getElementById('program-type-container');
    
    if(msgInput && msgInput.parentElement) msgInput.parentElement.style.display = isCamp ? 'none' : 'block';
    if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = isCamp ? 'none' : 'block';
    if(programTypeContainer) programTypeContainer.style.display = isCamp ? 'none' : 'block';
};

document.addEventListener('DOMContentLoaded', () => {
    const campSel = document.getElementById('builder-campaign-select');
    if(campSel) {
        campSel.addEventListener('change', window.checkRedundancy);
    }
    setTimeout(window.checkRedundancy, 100);
});

// --- COMPLEX SCHEDULE LOGIC ---
window.scheduleData = window.scheduleData || {
    'Lunes': [{start: '09:00', end: '18:00'}],
    'Martes': [{start: '09:00', end: '18:00'}],
    'Miércoles': [{start: '09:00', end: '18:00'}],
    'Jueves': [{start: '09:00', end: '18:00'}],
    'Viernes': [{start: '09:00', end: '18:00'}],
    'Sábado': [{start: '10:00', end: '14:00'}],
    'Domingo': []
};

window.renderScheduleDays = function() {
    // REFORMATTED CLEAN LAYOUT
    const container = document.getElementById('schedule-days-container');
    if (!container) return;
    
    // Solo renderizar si el modal está visible para evitar bugs (aunque ya lo llamamos en el onclick del botón)
    container.innerHTML = '';
    const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    
    // Estilos globales de borde para no duplicar CSS
    container.style.padding = '0';
    container.style.gap = '0';
    
    days.forEach(day => {
        const shifts = window.scheduleData[day] || [];
        
        let shiftsHtml = '';
        if (shifts.length === 0) {
            shiftsHtml = `<div style="font-size:14px; color:#6b7280; padding:10px 0; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-moon"></i> Cerrado</div>`;
        } else {
            shifts.forEach((shift, index) => {
                shiftsHtml += `
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom: ${index === shifts.length - 1 ? '0' : '12px'};">
                        <input type="time" class="premium-input schedule-time-input" data-day="${day}" data-index="${index}" data-type="start" value="${shift.start}" style="padding:10px 14px; font-size:14px; font-family:inherit; border-radius:10px; background:#ffffff; border:1px solid #d1d5db; width:130px; color:#000000;">
                        <span style="color:#4b5563; font-size:13px; font-weight:700;">a</span>
                        <input type="time" class="premium-input schedule-time-input" data-day="${day}" data-index="${index}" data-type="end" value="${shift.end}" style="padding:10px 14px; font-size:14px; font-family:inherit; border-radius:10px; background:#ffffff; border:1px solid #d1d5db; width:130px; color:#000000;">
                        <button onclick="removeShift('${day}', ${index})" style="background:none; border:none; color:#ef4444; width:36px; height:36px; border-radius:10px; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:background 0.2s;" onmouseover="this.style.background='rgba(239,68,68,0.1)'" onmouseout="this.style.background='none'"><i class="fa-solid fa-xmark" style="font-size:18px;"></i></button>
                    </div>
                `;
            });
        }
        
        const dayHtml = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; padding:20px 32px; border-bottom:1px solid #e5e7eb; background: ${shifts.length === 0 ? '#f9fafb' : '#ffffff'}; transition: background 0.2s ease;">
                <div style="width:120px; padding-top:10px;">
                    <h3 style="margin:0 0 6px 0; font-size:15px; font-weight:700; color:#000000;">${day}</h3>
                    <button onclick="addShift('${day}')" style="background:none; border:none; color:var(--accent-violet); font-size:12px; font-weight:600; cursor:pointer; padding:0; display:flex; align-items:center; gap:4px;"><i class="fa-solid fa-plus"></i> Añadir Turno</button>
                </div>
                <div style="flex:1; display:flex; flex-direction:column; align-items:flex-end;">
                    ${shiftsHtml}
                </div>
            </div>
        `;
        container.innerHTML += dayHtml;
    });
};

window.addShift = function(day) {
    if(!window.scheduleData[day]) window.scheduleData[day] = [];
    window.scheduleData[day].push({start: '10:00', end: '14:00'});
    window.renderScheduleDays();
};

window.removeShift = function(day, index) {
    if(window.scheduleData[day]) {
        window.scheduleData[day].splice(index, 1);
        window.renderScheduleDays();
    }
};

window.renderScheduleSummary = function() {
    const container = document.getElementById('schedule-summary-container');
    const content = document.getElementById('schedule-summary-content');
    if(!container || !content) {
        console.warn("Summary container or content div not found in DOM");
        return;
    }
    
    const targetState = typeof state !== 'undefined' ? state : window.state;
    if(!targetState || !targetState.schedules || Object.keys(targetState.schedules).length === 0) {
        container.style.display = 'none';
        return;
    }
    
    container.style.display = 'block';
    content.innerHTML = '';
    
    const days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    let hasAnyShift = false;
    
    days.forEach(day => {
        const shifts = state.schedules[day] || [];
        if(shifts.length > 0) {
            hasAnyShift = true;
            let shiftsText = shifts.map(s => `<div style="background:#f3f4f6; padding:4px 8px; border-radius:6px; font-size:12px; font-weight:600; color:#374151;">${s.start} - ${s.end}</div>`).join('');
            content.innerHTML += `
                <div style="border:1px solid #e5e7eb; border-radius:8px; padding:12px;">
                    <div style="font-weight:700; font-size:13px; color:#111827; margin-bottom:8px;">${day}</div>
                    <div style="display:flex; flex-direction:column; gap:4px;">${shiftsText}</div>
                </div>
            `;
        }
    });
    
    if(!hasAnyShift) container.style.display = 'none';
};

window.saveComplexSchedule = function() {
    try {
        console.log("Saving complex schedule...");
        // Collect data from DOM to memory just before saving
        const inputs = document.querySelectorAll('.schedule-time-input');
        inputs.forEach(input => {
            const d = input.getAttribute('data-day');
            const idx = parseInt(input.getAttribute('data-index'));
            const t = input.getAttribute('data-type');
            if(window.scheduleData[d] && window.scheduleData[d][idx]) {
                window.scheduleData[d][idx][t] = input.value;
            }
        });
        
        // Ensure state exists
        if (typeof state === 'undefined') window.state = {};
        
        // Save to state (safely referencing global state)
        const targetState = typeof state !== 'undefined' ? state : window.state;
        targetState.schedules = JSON.parse(JSON.stringify(window.scheduleData));
        console.log("Horarios guardados en estado:", targetState.schedules);
        
        if (!targetState.tenantId) {
            targetState.tenantId = window.merchantData ? window.merchantData.id : null;
            if (!targetState.tenantId && window.merchantSession && window.merchantSession.user) {
                targetState.tenantId = window.merchantSession.user.id;
            }
        }
        if (!targetState.tenantId) {
            if(typeof showToast==='function') showToast('Error: No se pudo identificar tu cuenta. Recarga la página.', 'error');
            return;
        }
        
        // Update DB
        if (targetState.tenantId && window.supabaseClient) {
            let prefs = {};
            try { prefs = window.merchantData.appointment_settings.landing_prefs || {}; } catch(e){}
            let processed = [];
            try { processed = window.merchantData.appointment_settings.processed_appointments || []; } catch(e){}
            
            const newSettings = {
                schedules: targetState.schedules,
                landing_prefs: prefs,
                processed_appointments: processed
            };
            
            if (!window.merchantData) window.merchantData = {};
            window.merchantData.appointment_settings = newSettings;
            
            window.supabaseClient.from('merchants').update({
                appointment_settings: newSettings
            }).eq('id', window.merchantData.id).select().then(({data, error}) => {
                if (error) {
                    if(typeof showToast==='function') showToast('Error en la nube: ' + error.message, 'error');
                } else if (!data || data.length === 0) {
                    if(typeof showToast==='function') showToast('Error de permisos. Tu sesión pudo haber expirado.', 'error');
                } else {
                    if (typeof showToast === 'function') showToast('Horarios guardados en la nube', 'success');
                    const modal = document.getElementById('schedule-config-modal');
                    if (modal) modal.style.display = 'none';
                }
            });
        }

        // Update UI Summary safely
        try {
            window.renderScheduleSummary();
        } catch (sumErr) {
            console.error("Error in renderScheduleSummary:", sumErr);
            console.error('Summary error:', sumErr);
        }
        
        const modal = document.getElementById('schedule-config-modal');
        if (modal) {
            modal.style.display = 'none';
        } else {
            console.error("Modal element not found to close it!");
        }
        
        // Notificación silenciosa (se quitó el toast a petición del usuario)
    } catch (err) {
        console.error("CRASH in saveComplexSchedule:", err);
        if(typeof showToast==='function') showToast('Error al guardar horarios: ' + err.message, 'error');
    }
};

// Hook rendering into modal open
document.addEventListener('DOMContentLoaded', () => {
    // Intercept clicks on any element that opens schedule modal
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('button');
        if (btn && btn.getAttribute('onclick') && btn.getAttribute('onclick').includes('schedule-config-modal')) {
            if (btn.getAttribute('onclick').includes('flex') || btn.getAttribute('onclick').includes('block')) {
                // If it's opening the modal
                setTimeout(window.renderScheduleDays, 50);
            }
        }
    });
});

// --- LOYALTY TAB INIT ---
window.initLoyaltyTab = function() {
    // 1. Loyalty Mode (Hybrid, Cashback, Stamps, Custom)
    const mode = state.activeMode || 'hybrid';
    const card = document.getElementById(`loyalty-mode-${mode}`);
    if (card) {
        document.querySelectorAll('.role-card[id^="loyalty-mode-"]').forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        const radio = card.querySelector('input');
        if(radio) radio.checked = true;
    }

    // 2. Toggles & Sliders
    const safeSetChecked = (id, val) => { const el = document.getElementById(id); if(el) el.checked = !!val; };
    const safeSetValue = (id, val) => { const el = document.getElementById(id); if(el) el.value = val; };

    safeSetChecked('toggle-cashback', state.cashbackActive !== false);
    safeSetValue('cashback-slider', state.cashbackPercent || 10);
    const cbDisplay = document.getElementById('cashback-percent-display');
    if(cbDisplay) cbDisplay.textContent = (state.cashbackPercent || 10) + '%';
    const cbExample = document.getElementById('cashback-example');
    if(cbExample) cbExample.textContent = state.cashbackPercent || 10;

    safeSetChecked('toggle-stamps', state.stampsActive !== false);
    safeSetValue('stamps-total', state.stampsTotal || 5);
    safeSetValue('stamps-reward', state.stampsReward || 'Premio Gratis');

    safeSetChecked('toggle-vip', state.vipActive !== false);
    
    // VIP Tiers
    if (state.vipTiers) {
        if (state.vipTiers.bronce) {
            safeSetValue('vip-bronce-cb', state.vipTiers.bronce.cashbackPercent || 5);
            safeSetValue('vip-bronce-perk', state.vipTiers.bronce.perk || '');
        }
        if (state.vipTiers.plata) {
            safeSetValue('vip-plata-min', state.vipTiers.plata.minSpent || 1000);
            safeSetValue('vip-plata-cb', state.vipTiers.plata.cashbackPercent || 10);
            safeSetValue('vip-plata-perk', state.vipTiers.plata.perk || '');
        }
        if (state.vipTiers.oro) {
            safeSetValue('vip-oro-min', state.vipTiers.oro.minSpent || 3000);
            safeSetValue('vip-oro-cb', state.vipTiers.oro.cashbackPercent || 15);
            safeSetValue('vip-oro-perk', state.vipTiers.oro.perk || '');
        }
    }

    // Prepaid
    safeSetChecked('toggle-prepaid', state.prepaidActive === true);
    safeSetValue('pre-amount', state.prepaidAmount || 500);
    safeSetValue('pre-bonus', state.prepaidBonus || 100);
    const panelPrepaid = document.getElementById('panel-prepaid-config');
    if (panelPrepaid) panelPrepaid.style.display = state.prepaidActive ? 'block' : 'none';
};

// Dynamic VIP Benefits Logic
window.addVipBenefit = function(tier, type = 'cashback', value = '') {
    const container = document.getElementById(`vip-${tier}-benefits`);
    if (!container) return;

    const row = document.createElement('div');
    row.style.display = 'flex';
    row.style.gap = '8px';
    row.style.alignItems = 'center';
    row.classList.add('vip-benefit-row');
    
    // Select Type
    const select = document.createElement('select');
    select.classList.add('fidelio-input', 'benefit-type');
    select.style.flex = '1';
    select.style.padding = '4px 8px';
    select.innerHTML = `
        <option value="cashback" ${type === 'cashback' ? 'selected' : ''}>Cashback (%)</option>
        <option value="puntos" ${type === 'puntos' ? 'selected' : ''}>Multiplicador Puntos</option>
        <option value="descuento" ${type === 'descuento' ? 'selected' : ''}>Descuento Fijo (%)</option>
        <option value="producto" ${type === 'producto' ? 'selected' : ''}>Producto Gratis</option>
        <option value="upgrade" ${type === 'upgrade' ? 'selected' : ''}>Upgrade</option>
        <option value="otro" ${type === 'otro' ? 'selected' : ''}>Otro</option>
    `;

    // Input Value
    const input = document.createElement('input');
    input.type = 'text';
    input.classList.add('fidelio-input', 'benefit-value');
    input.style.flex = '2';
    input.placeholder = 'Valor / Descripción';
    input.value = value;

    // Delete Button
    const btnDel = document.createElement('button');
    btnDel.type = 'button';
    btnDel.innerHTML = '<i class="fa-solid fa-trash"></i>';
    btnDel.style.background = 'transparent';
    btnDel.style.color = 'var(--accent-red)';
    btnDel.style.border = 'none';
    btnDel.style.cursor = 'pointer';
    btnDel.onclick = () => row.remove();

    row.appendChild(select);
    row.appendChild(input);
    row.appendChild(btnDel);

    container.appendChild(row);
};

// ==========================================
// AI COPILOT LOGIC
// ==========================================

window.fetchCopilotIdeas = async function() {
    const loadingEl = document.getElementById('copilot-loading');
    const resultsEl = document.getElementById('copilot-results');
    const containerEl = document.getElementById('copilot-cards-container');
    
    if(!loadingEl || !resultsEl || !containerEl) return;
    
    loadingEl.style.display = 'flex';
    resultsEl.style.display = 'none';
    containerEl.innerHTML = '';
    
    try {
        const token = localStorage.getItem('fidelio_jwt');
        
        // Mock de contexto del negocio para la demo
        const mockContext = {
            totalClientes: 1240,
            clientesActivos: 450,
            clientesRiesgo: 310,
            clientesCumpleaneros: 12,
            clientesInactivos: 480,
            visitasSemana: 125
        };

        // Simular llamada a Gemini (Backend offline)
        await new Promise(resolve => setTimeout(resolve, 2500));
        
        const opportunities = [
            {
                title: "Recuperación de Inactivos",
                description: "Notamos que 480 clientes no han vuelto en 30 días. Envíales un SMS con un incentivo del 15% de descuento válido por 48 horas.",
                type: "retention",
                impact_est: "+$12,500 MXN",
                roi_est: "3.5x"
            },
            {
                title: "Impulso de Días Lentos",
                description: "Tus visitas caen un 40% los martes. Configura una automatización de Puntos Dobles los martes de 4 PM a 7 PM.",
                type: "traffic",
                impact_est: "+35 Visitas",
                roi_est: "5.2x"
            },
            {
                title: "Upsell de Ticket Promedio",
                description: "Tus clientes VIP están gastando por debajo de su histórico. Ofrece una recompensa sorpresa al superar los $500 MXN de compra.",
                type: "upsell",
                impact_est: "+$8,000 MXN",
                roi_est: "4.1x"
            }
        ];
        
        opportunities.forEach((opp, index) => {
            const card = document.createElement('div');
            card.style.cssText = 'background: white; border: 1px solid var(--border-glass); border-radius: 16px; padding: 24px; position: relative; overflow: hidden; transition: all 0.3s ease; animation: fadeInUp 0.5s ease forwards; opacity: 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);';
            card.style.animationDelay = (index * 0.15) + 's';
            
            // Efecto Hover 
            card.onmouseenter = () => { card.style.borderColor = 'rgba(139, 92, 246, 0.5)'; card.style.transform = 'translateY(-5px)'; card.style.boxShadow = '0 10px 25px rgba(139,92,246,0.15)'; };
            card.onmouseleave = () => { card.style.borderColor = 'var(--border-glass)'; card.style.transform = 'translateY(0)'; card.style.boxShadow = '0 4px 6px rgba(0,0,0,0.05)'; };

            // Ícono dependiendo del tipo
            let iconHtml = '<i class="fa-solid fa-bullseye" style="color: #60a5fa;"></i>';
            if(opp.type === 'recuperacion') iconHtml = '<i class="fa-solid fa-heart-crack" style="color: #f43f5e;"></i>';
            if(opp.type === 'dias_lentos') iconHtml = '<i class="fa-solid fa-bolt" style="color: #f59e0b;"></i>';
            if(opp.type === 'cumpleanos') iconHtml = '<i class="fa-solid fa-cake-candles" style="color: #a855f7;"></i>';
            if(opp.type === 'vip_exclusivo') iconHtml = '<i class="fa-solid fa-crown" style="color: #fbbf24;"></i>';

            card.innerHTML = `
                <div style="display:flex; align-items:center; gap:12px; margin-bottom: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 12px; background: rgba(139, 92, 246, 0.1); display:flex; align-items:center; justify-content:center; font-size: 18px;">
                        ${iconHtml}
                    </div>
                    <h4 style="margin:0; font-size: 16px; color: var(--text-main);">${opp.title}</h4>
                </div>
                <p style="color: var(--text-muted); font-size: 13px; line-height: 1.5; margin-bottom: 20px;">${opp.description}</p>
                
                <div style="background: rgba(139,92,246,0.05); border-radius: 8px; padding: 12px; margin-bottom: 20px;">
                    <div style="font-size: 10px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px; font-weight: 600;"><i class="fa-brands fa-apple"></i> Sugerencia</div>
                    <div style="color: var(--text-main); font-size: 13px; font-style: italic;">"${opp.pushMessage}"</div>
                </div>

                <div style="display:flex; justify-content: space-between; align-items:center; margin-bottom: 20px; font-size: 12px;">
                    <div><span style="color: var(--text-muted);">Audiencia:</span> <span style="color: #34d399; font-weight: 600;">${opp.estimatedReach}</span></div>
                </div>

                <button class="btn btn-primary" onclick='window.executeCopilotIdea(${JSON.stringify(opp).replace(/'/g, "&apos;")})' style="width: 100%; background: linear-gradient(135deg, rgba(139,92,246,0.8) 0%, rgba(59,130,246,0.8) 100%);">
                    Ejecutar con 1 Clic <i class="fa-solid fa-arrow-right"></i>
                </button>
            `;
            containerEl.appendChild(card);
        });
        
    } catch (e) {
        console.error(e);
        if (typeof window.showToast === 'function') window.showToast("Error al generar ideas con Copiloto AI", "error");
    } finally {
        loadingEl.style.display = 'none';
        resultsEl.style.display = 'block';
    }
};

window.executeCopilotIdea = function(opp) {
    const navTabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    navTabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));

    if (opp.format === 'card') {
        // 1. Inicializar como Tarjeta Especial
        if(window.createNewSpecialCard) window.createNewSpecialCard();

        // 2. Determinar el modo (Membresía, Multipass, etc.)
        let mode = 'membership';
        if (opp.type === 'dias_lentos') mode = 'multipass';
        if (opp.type === 'recuperacion' || opp.type === 'cumpleanos') mode = 'certificates';
        
        // Seleccionar el radio button correspondiente
        const modeRadio = document.querySelector(`input[name="loyalty_mode"][value="${mode}"]`);
        if (modeRadio) {
            modeRadio.checked = true;
            modeRadio.dispatchEvent(new Event('change'));
        }

        // 3. Rellenar campos del Builder y del estado
        const titleInput = document.getElementById('rest-name');
        const descInput = document.getElementById('rest-desc');
        
        if(titleInput) {
            titleInput.value = opp.title;
            if(window.state) window.state.restaurantName = opp.title;
        }
        if(descInput) descInput.value = opp.pushMessage.substring(0, 40);

        // 4. Rellenar campos específicos de Tarjetas Especiales
        if (mode === 'membership') {
            const benefitInput = document.getElementById('mem-benefit');
            if (benefitInput) benefitInput.value = opp.pushMessage;
        } else if (mode === 'multipass') {
            const serviceInput = document.getElementById('mp-service');
            if (serviceInput) serviceInput.value = opp.title;
        } else if (mode === 'certificates') {
            // Se queda con el monto por defecto
        }

        // 5. Cambiar a la pestaña de Tarjetas Especiales (ya lo hace createNewSpecialCard, pero por si acaso aseguramos)
        const specialTabBtn = document.querySelector('.nav-tab[data-tab="tab-special-cards"]');
        const specialTabContent = document.getElementById('tab-special-cards');
        if(specialTabBtn) specialTabBtn.classList.add('active');
        if(specialTabContent) specialTabContent.classList.add('active');

        // Disparar render
        if(window.updatePassRender) window.updatePassRender();
        if (typeof window.showToast === 'function') window.showToast("Tarjeta Especial preconfigurada. Ajusta los detalles.", "success");
        window.scrollTo({ top: 0, behavior: 'smooth' });

    } else {
        // 1. Cambiar a la pestaña de Campañas Push (comportamiento default)
        const marketingTabBtn = document.querySelector('.nav-tab[data-tab="tab-marketing"]');
        const marketingTabContent = document.getElementById('tab-marketing');
        
        if(marketingTabBtn) marketingTabBtn.classList.add('active');
        if(marketingTabContent) marketingTabContent.classList.add('active');
        
        // 2. Rellenar los campos
        const messageInput = document.getElementById('camp-push-message');
        const segmentSelect = document.getElementById('camp-segment-select');
        
        if(messageInput) {
            messageInput.value = opp.pushMessage;
        }
        if(segmentSelect) {
            let optionExists = false;
            for (let i = 0; i < segmentSelect.options.length; i++) {
                if (segmentSelect.options[i].value === opp.segment) {
                    optionExists = true;
                    break;
                }
            }
            if(optionExists) {
                segmentSelect.value = opp.segment;
            } else {
                segmentSelect.value = 'all';
            }
        }
        
        // 3. Seleccionar visualmente el cuadro de tipo (libre)
        document.querySelectorAll('.campaign-card').forEach(c => c.classList.remove('active'));
        document.getElementById('camp-card-libre')?.classList.add('active');
        
        // 4. Disparar actualizaciones visuales
        if(window.updatePushPreview) window.updatePushPreview();
        if(window.updateAudienceEstimate) window.updateAudienceEstimate();
        
        showToast("Campaña Push pre-configurada por la IA. Revisa y envía.", "success");
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
};

// Add CSS keyframe for fadeInUp if not exists
if(!document.getElementById('copilot-styles')) {
    const style = document.createElement('style');
    style.id = 'copilot-styles';
    style.innerHTML = `
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
}

// Hook en el click del tab para disparar la carga 1 sola vez
document.addEventListener('DOMContentLoaded', () => {
    const copilotTabBtn = document.querySelector('.nav-tab[data-tab="tab-copilot"]');
    if(copilotTabBtn) {
        copilotTabBtn.addEventListener('click', () => {
            const container = document.getElementById('copilot-cards-container');
            if(container && container.innerHTML.trim() === '') {
                window.fetchCopilotIdeas();
            }
        });
    }
});

// ==========================================
// CAJA (POS) LOGIC
// ==========================================

window.openCajaModal = function() {
    const modal = document.getElementById('modal-caja-transaction');
    if(modal) {
        modal.style.display = 'flex';
        // Reset fields
        const customerSelect = document.getElementById('caja-customer');
        if(customerSelect) {
            customerSelect.innerHTML = '<option value="">-- Cliente General (Venta de mostrador) --</option>';
            if(window.state && window.state.customers) {
                window.state.customers.forEach(cust => {
                    const option = document.createElement('option');
                    option.value = cust.id;
                    option.textContent = `${cust.full_name || 'Sin Nombre'} (${cust.email || 'Sin Correo'})`;
                    customerSelect.appendChild(option);
                });
            }
            customerSelect.value = '';
        }

        document.getElementById('caja-concept').value = '';
        document.getElementById('caja-amount').value = '';
        document.getElementById('caja-method').value = 'Efectivo';
        
        // Anim In
        setTimeout(() => {
            modal.style.opacity = '1';
            const content = document.getElementById('caja-modal-content');
            if(content) content.style.transform = 'translateY(0)';
        }, 10);
    }
};

window.closeCajaModal = function() {
    const modal = document.getElementById('modal-caja-transaction');
    if(modal) {
        modal.style.opacity = '0';
        const content = document.getElementById('caja-modal-content');
        if(content) content.style.transform = 'translateY(20px)';
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }
};

window.loadCajaTransactions = async function() {
    if(!window.merchantId) return;
    
    try {
        const { data, error } = await _supabase
            .from('merchant_transactions')
            .select('*')
            .eq('merchant_id', window.merchantId)
            .order('created_at', { ascending: false });
            
        if (error) {
            console.warn("La tabla merchant_transactions no existe o hay un error. Por favor crea la tabla primero.");
            return;
        }
        
        // Render Table
        const tbody = document.getElementById('caja-transactions-tbody');
        if(!tbody) return;
        
        if (!data || data.length === 0) {
            tbody.innerHTML = `<tr><td colspan='5' style='padding:40px; text-align:center;'><div style='display:inline-block; max-width:300px;'><div style='font-size:40px; margin-bottom:16px; color:#10b981;'><i class='fa-solid fa-receipt'></i></div><h4 style='margin:0 0 8px; font-size:18px;'>Cero Movimientos</h4><p style='color:var(--text-muted); font-size:14px;'>Aquí aparecerá todo el historial cuando tus clientes escaneen su tarjeta en caja.</p></div></td></tr>`;
        } else {
            let html = '';
            data.forEach(txn => {
                const date = new Date(txn.created_at).toLocaleString('es-MX', {
                    day: '2-digit', month: 'short', year: 'numeric',
                    hour: '2-digit', minute:'2-digit'
                });
                
                // Buscar nombre del cliente si existe
                let customerName = '-';
                if(txn.customer_id && window.state && window.state.customers) {
                    const cust = window.state.customers.find(c => c.id === txn.customer_id);
                    if(cust) {
                        customerName = `<span style="background: rgba(139, 92, 246, 0.1); color: var(--accent-violet); padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 600;">${cust.full_name || cust.email}</span>`;
                    }
                }
                
                html += `
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 16px 24px; color: var(--text-muted); font-size: 13px;">${date}</td>
                        <td style="padding: 16px 24px;">${customerName}</td>
                        <td style="padding: 16px 24px; font-weight: 500;">${txn.concept}</td>
                        <td style="padding: 16px 24px;">${txn.payment_method}</td>
                        <td style="padding: 16px 24px; text-align: right; font-weight: 700; color: #10b981;">+$${parseFloat(txn.amount).toFixed(2)}</td>
                    </tr>
                `;
            });
            tbody.innerHTML = html;
        }
        
        // Calculate Metrics
        let hoy = 0;
        let semana = 0;
        let mes = 0;
        let total = 0;
        
        const now = new Date();
        const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const startOfWeek = new Date(startOfDay);
        startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
        const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
        
        data.forEach(txn => {
            const amount = parseFloat(txn.amount) || 0;
            const txnDate = new Date(txn.created_at);
            
            total += amount;
            if(txnDate >= startOfMonth) mes += amount;
            if(txnDate >= startOfWeek) semana += amount;
            if(txnDate >= startOfDay) hoy += amount;
        });
        
        document.getElementById('caja-hoy').textContent = `$${hoy.toFixed(2)}`;
        document.getElementById('caja-semana').textContent = `$${semana.toFixed(2)}`;
        document.getElementById('caja-mes').textContent = `$${mes.toFixed(2)}`;
        document.getElementById('caja-total').textContent = `$${total.toFixed(2)}`;
        
    } catch (err) {
        console.error("Error cargando transacciones de caja:", err);
    }
};

window.saveCajaTransaction = async function() {
    if(!window.merchantId) return;
    
    const customerId = document.getElementById('caja-customer').value || null;
    const concept = document.getElementById('caja-concept').value.trim();
    const amount = parseFloat(document.getElementById('caja-amount').value);
    const method = document.getElementById('caja-method').value;
    
    if(!concept || isNaN(amount) || amount <= 0) {
        if(typeof showToast === 'function') showToast("Por favor ingresa un concepto y monto válido.", "error");
        else if(typeof showToast==='function') showToast('Ingresa un concepto y monto válido', 'warning');
        return;
    }
    
    const btn = document.querySelector('#modal-caja-transaction .btn-primary');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Guardando...';
    btn.disabled = true;
    
    try {
        const payload = {
            merchant_id: window.merchantId,
            concept: concept,
            amount: amount,
            payment_method: method
        };
        
        if (customerId) {
            payload.customer_id = customerId;
        }

        const { error } = await _supabase
            .from('merchant_transactions')
            .insert([payload]);
            
        if (error) {
            throw error;
        }
        
        if(typeof showToast === 'function') showToast("Pago registrado correctamente.", "success");
        window.closeCajaModal();
        window.loadCajaTransactions(); // Reload list
        
    } catch (err) {
        console.error("Error saving transaction:", err);
        if(typeof showToast === 'function') showToast("Error al guardar. Asegúrate de haber creado la tabla en Supabase.", "error");
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
};

// Add tab listener hook
document.addEventListener('DOMContentLoaded', () => {
    // When clicking tabs, if it's Caja, load data
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            if(tabId === 'tab-caja') {
                window.loadCajaTransactions();
            }
        });
    });
});



// ==========================================
// MÓDULO: COPILOTO AI (GEMINI)
// ==========================================
window.fetchCopilotIdeas = function() {
    const loading = document.getElementById('copilot-loading');
    const results = document.getElementById('copilot-results');
    const container = document.getElementById('copilot-cards-container');
    
    if (!loading || !results || !container) return;
    
    // Si la función requiere un plan Pro, podemos validarlo. Copilot suena a Pro.
    const plan = window.merchantData ? (window.merchantData.business_type || 'starter') : 'starter';
    const isAdmin = window.merchantSession && window.merchantSession.user && window.merchantSession.user.email === 'hola@fideliorewards.com';
    
    if (plan !== 'business' && plan !== 'enterprise' && !isAdmin) {
        if(typeof showToast === 'function') showToast('El Copiloto AI es exclusivo del Plan Business. Mejora tu plan para activarlo.', 'error');
        loading.style.display = 'none';
        results.style.display = 'block';
        container.innerHTML = `
            <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 20px; border-radius: var(--radius-md); text-align: center; color: #ef4444; grid-column: 1 / -1;">
                <i class="fa-solid fa-lock" style="font-size: 24px; margin-bottom: 10px;"></i>
                <h4>Función Bloqueada</h4>
                <p style="font-size: 14px; margin-top: 5px;">Actualiza a Plan Profesional para desbloquear el análisis inteligente de Gemini.</p>
                <button class="btn btn-primary" style="margin-top: 15px;" onclick="window.switchTab('tab-stripe')">Mejorar Plan</button>
            </div>
        `;
        return;
    }
    
    loading.style.display = 'flex';
    results.style.display = 'none';
    
    setTimeout(() => {
        loading.style.display = 'none';
        results.style.display = 'block';
        
        container.innerHTML = `
            <div style="background: var(--bg-card); padding: 20px; border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:15px;">
                    <div style="background: rgba(139,92,246,0.1); padding: 8px 12px; border-radius: 20px; color: var(--accent-violet); font-size: 12px; font-weight: 600;">
                        <i class="fa-solid fa-bolt"></i> CAMPAÑA RÁPIDA
                    </div>
                    <span style="color:var(--text-muted); font-size:12px;">95% Éxito</span>
                </div>
                <h4 style="color:var(--text-main); margin-bottom:10px; font-size: 16px;">Recuperar Clientes Inactivos</h4>
                <p style="color:var(--text-muted); font-size: 13px; margin-bottom: 20px; line-height:1.5;">Tienes 45 clientes que no han vuelto en 30 días. Enviarles un cupón de 10% de Cashback extra tiene alta probabilidad de retorno.</p>
                <button class="btn btn-outline" style="width:100%; border-color:var(--accent-violet); color:var(--accent-violet);" onclick="if(typeof showToast === 'function') showToast('Campaña generada y lista en Marketing.', 'success')">
                    Crear Campaña
                </button>
            </div>
            
            <div style="background: var(--bg-card); padding: 20px; border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:15px;">
                    <div style="background: rgba(59,130,246,0.1); padding: 8px 12px; border-radius: 20px; color: #3B82F6; font-size: 12px; font-weight: 600;">
                        <i class="fa-solid fa-arrow-up"></i> UPSELL
                    </div>
                    <span style="color:var(--text-muted); font-size:12px;">82% Éxito</span>
                </div>
                <h4 style="color:var(--text-main); margin-bottom:10px; font-size: 16px;">Impulso a VIP Oro</h4>
                <p style="color:var(--text-muted); font-size: 13px; margin-bottom: 20px; line-height:1.5;">Hay 12 clientes a solo 1 visita de subir a Oro. Envíales un SMS automático felicitándolos para asegurar su próxima visita.</p>
                <button class="btn btn-outline" style="width:100%; border-color:#3B82F6; color:#3B82F6;" onclick="if(typeof showToast === 'function') showToast('Campaña de Upsell programada.', 'success')">
                    Programar SMS
                </button>
            </div>
            
            <div style="background: var(--bg-card); padding: 20px; border-radius: var(--radius-md); border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:15px;">
                    <div style="background: rgba(16,185,129,0.1); padding: 8px 12px; border-radius: 20px; color: #10B981; font-size: 12px; font-weight: 600;">
                        <i class="fa-solid fa-calendar-check"></i> HORAS VALLE
                    </div>
                    <span style="color:var(--text-muted); font-size:12px;">78% Éxito</span>
                </div>
                <h4 style="color:var(--text-main); margin-bottom:10px; font-size: 16px;">Promoción Martes Lento</h4>
                <p style="color:var(--text-muted); font-size: 13px; margin-bottom: 20px; line-height:1.5;">Tus martes por la tarde tienen baja afluencia. Lanza un 2x1 en puntos solo para ese día de la semana.</p>
                <button class="btn btn-outline" style="width:100%; border-color:#10B981; color:#10B981;" onclick="if(typeof showToast === 'function') showToast('Regla de Horas Valle activada.', 'success')">
                    Activar Regla
                </button>
            </div>
        `;
    }, 2500); 
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[onclick*="tab-copilot"]').forEach(btn => {
        btn.addEventListener('click', () => {
            if(document.getElementById('copilot-results') && document.getElementById('copilot-results').style.display === 'none') {
                window.fetchCopilotIdeas();
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    // Form fields toggles (now handled via pure CSS, no JS animation needed here)


}); // Close previous DOMContentLoaded early to put these in global scope

window.copyLandingLink = function() {
        const display = document.getElementById('landing-link-display');
        if (display) {
            navigator.clipboard.writeText('https://' + display.textContent.trim());
            if (typeof showToast === 'function') showToast('Enlace copiado al portapapeles', 'success');
        }
    };

window.updateLandingUI = function() {
        if (window.merchantData) {
            const prefs = (window.merchantData.appointment_settings && window.merchantData.appointment_settings.landing_prefs) ? window.merchantData.appointment_settings.landing_prefs : {};
            let slug = prefs.username;
            if (!slug) {
                const bName = window.merchantData.business_name || 'tu-negocio';
                slug = bName.toLowerCase().replace(/[^a-z0-9]/g, '');
            }
            const landingLink = `fideliorewards.com/${slug}?v=3`;
            const linkDisplay = document.getElementById('landing-link-display');
            if (linkDisplay) linkDisplay.textContent = landingLink;

            const reqPhone = document.getElementById('req-phone');
            if (reqPhone) {
                reqPhone.checked = prefs.require_phone !== false;
            }
            
            const reqBday = document.getElementById('req-birthday');
            if (reqBday) {
                reqBday.checked = prefs.require_birthday !== false;
            }
            
            const portalColor = document.getElementById('portal-color-primary');
            if (portalColor) portalColor.value = prefs.portal_color || '#8b5cf6';
            
            if (prefs.portal_logo) {
                window.currentPortalLogo = prefs.portal_logo;
                const preview = document.getElementById('portal-logo-preview');
                const img = document.getElementById('portal-logo-img');
                if (preview && img) {
                    img.src = prefs.portal_logo;
                    preview.style.display = 'flex';
                }
            }
        }
    };
    
setTimeout(() => { if(window.updateLandingUI) window.updateLandingUI(); }, 2000);

document.addEventListener('DOMContentLoaded', () => {
    const btnSaveForm = document.getElementById('btn-save-form-fields');
    if (btnSaveForm) {
        btnSaveForm.addEventListener('click', async () => {
            if (!window.merchantData) return;
            const originalText = btnSaveForm.innerHTML;
            btnSaveForm.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Guardando...';
            btnSaveForm.disabled = true;

            try {
                const logoFile = document.getElementById('portal-logo-upload')?.files[0];
                if (logoFile) {
                    const ext = logoFile.name.split('.').pop();
                    const filename = `${window.merchantSession.user.id}_${Date.now()}.${ext}`;
                    const { data, error: uploadError } = await window.supabaseClient.storage.from('logos').upload(filename, logoFile, { upsert: true });
                    if (uploadError) throw new Error('Error al subir el logo: ' + uploadError.message);
                    
                    const { data: publicUrlData } = window.supabaseClient.storage.from('logos').getPublicUrl(filename);
                    window.currentPortalLogo = publicUrlData.publicUrl;
                }
                const prefs = {
                    require_phone: document.getElementById('req-phone').checked,
                    require_birthday: document.getElementById('req-birthday').checked,
                    portal_color: document.getElementById('portal-color-primary')?.value || '#8b5cf6',
                    portal_logo: window.currentPortalLogo || '',
                    username: window.merchantData.appointment_settings?.landing_prefs?.username || window.merchantData.business_name.toLowerCase().replace(/[^a-z0-9]/g, '')
                };

                const currentApptSettings = window.merchantData.appointment_settings || {};
                currentApptSettings.landing_prefs = prefs;

                const { error } = await window.supabaseClient.from('merchants').update({
                    appointment_settings: currentApptSettings
                }).eq('id', window.merchantSession.user.id);

                if (error) throw error;
                
                window.merchantData.appointment_settings = currentApptSettings;
                if (typeof showToast === 'function') showToast('Formulario actualizado correctamente', 'success');
            } catch (e) {
                if (typeof showToast === 'function') showToast(e.message, 'error');
            } finally {
                btnSaveForm.innerHTML = originalText;
                btnSaveForm.disabled = false;
            }
        });
    }
});



window.markAppointmentProcessed = async function(id, waLink) {
    if (!window.merchantData) return;
    if (!window.merchantData.appointment_settings) window.merchantData.appointment_settings = {};
    if (!window.merchantData.appointment_settings.processed_appointments) window.merchantData.appointment_settings.processed_appointments = [];
    
    if (!window.merchantData.appointment_settings.processed_appointments.includes(id)) {
        window.merchantData.appointment_settings.processed_appointments.push(id);
        
        // Guardar en Supabase
        if (window.supabaseClient) {
            window.supabaseClient.from('merchants').update({
                appointment_settings: window.merchantData.appointment_settings
            }).eq('id', window.merchantData.id).then(({error}) => {
                if (error) console.error("Error marking processed", error);
            });
        }
    }
    
    // Refresh UI
    if (typeof window.updateDashboardMetrics === 'function') window.updateDashboardMetrics();
    if (typeof window.loadAppointments === 'function') window.loadAppointments();
    
    // Abrir WhatsApp
    if (waLink && waLink !== '#') {
        window.open(waLink, '_blank');
    }
};

window.loadAppointments = function() {
    const container = document.getElementById('appointments-list-container');
    if (!container) return;

    if (!state.transactions) {
        container.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 20px;">Cargando citas...</p>';
        return;
    }

    let processed = [];
    try { processed = window.merchantData.appointment_settings.processed_appointments || []; } catch(e){}

    const appts = state.transactions
        .filter(t => t.transaction_type === 'appointment_request')
        .sort((a,b) => new Date(b.created_at) - new Date(a.created_at));

    if (appts.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 20px;"><i class="fa-solid fa-calendar-day"></i> Aún no tienes citas agendadas.</p>';
        return;
    }

    // Try to get payment link from the first campaign if exists
    let stripeLink = "";
    if (state.campaigns && state.campaigns.length > 0) {
        const rules = state.campaigns[0].rules_config || {};
        stripeLink = rules.payment_url || state.campaigns[0].custom_cta_url || "";
    }

    container.innerHTML = appts.map(t => {
        let details = {};
        try { details = JSON.parse(t.notes || "{}"); } catch(e){}
        const cust = state.customers.find(c => c.id === t.customer_id) || {};
        
        const dateRaw = details.date || 'Sin fecha';
        const timeRaw = details.time || 'Sin hora';
        const serviceNotes = details.notes || 'Ninguna';
        const name = cust.full_name || cust.name || 'Cliente Desconocido';
        const phone = cust.phone || '';
        
        let msg = `Hola ${name}, he recibido tu solicitud de cita para el día ${dateRaw} a las ${timeRaw}. Para confirmar tu lugar, por favor realiza el pago o anticipo aquí: ${stripeLink}`;
        const waLink = phone ? `https://wa.me/${phone.replace(/\D/g,'')}?text=${encodeURIComponent(msg)}` : '#';
        
        const isProcessed = processed.includes(t.id);
        const badgeHtml = isProcessed 
            ? `<span style="background:#f3f4f6; color:#4b5563; font-size:11px; font-weight:700; padding:4px 8px; border-radius:12px;"><i class="fa-solid fa-check"></i> CONTACTADO</span>`
            : `<span style="background:#dbeafe; color:#1d4ed8; font-size:11px; font-weight:700; padding:4px 8px; border-radius:12px;">NUEVA SOLICITUD</span>`;

        return `
            <div style="background:${isProcessed ? '#ffffff' : '#fff1f2'}; border:2px solid ${isProcessed ? '#e5e7eb' : '#f43f5e'}; border-radius:12px; padding:16px; display:flex; flex-direction:column; gap:12px; box-shadow:0 4px 10px rgba(0,0,0,0.05); opacity: ${isProcessed ? '0.7' : '1'};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <h3 style="margin:0 0 4px 0; font-size:16px; color:#111827;">${name}</h3>
                        <p style="margin:0; font-size:13px; color:#6b7280;"><i class="fa-solid fa-calendar-day"></i> ${dateRaw} a las ${timeRaw}</p>
                    </div>
                    ${badgeHtml}
                </div>
                <div style="background:#f9fafb; padding:12px; border-radius:8px; font-size:13px; color:#374151;">
                    <strong>Notas:</strong> ${serviceNotes}
                </div>
                <div style="display:flex; gap:8px; margin-top:4px;">
                    ${phone 
                        ? `<button onclick="markAppointmentProcessed('${t.id}', '${waLink}')" style="cursor:pointer; border:none; flex:1; text-align:center; background:#10b981; color:white; padding:10px; border-radius:8px; font-weight:600; font-size:14px;"><i class="fa-brands fa-whatsapp"></i> Confirmar y Cobrar</button>` 
                        : `<span style="flex:1; text-align:center; background:#f3f4f6; color:#9ca3af; padding:10px; border-radius:8px; font-size:14px;"><i class="fa-solid fa-phone-slash"></i> Sin teléfono</span>`}
                </div>
            </div>
        `;
    }).join('');
};



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


window.openCampaignHub = async function(id) {
    try {
        const res = await fetch('/api/campaigns', {
            headers: { 'Authorization': `Bearer ${window.merchantSession?.access_token || ''}` }
        });
        const data = await res.json();
        const camp = data.campaigns.find(c => c.id === id);
        if (!camp) return;

        // Populate modal
        const hub = document.getElementById('modal-campaign-hub');
        if(!hub) return;
        
        document.getElementById('hub-camp-name').textContent = camp.name || "Campaña";
        document.getElementById('hub-camp-type').innerHTML = `<i class="fa-solid fa-qrcode" style="margin-right:6px;"></i> ${camp.type === 'stamps' ? 'Tarjeta de Sellos' : 'Wallet Digital'}`;
        document.getElementById('hub-camp-icon').innerHTML = camp.logo_url ? `<img src="${camp.logo_url}" style="width:100%; height:100%; border-radius:16px; object-fit:cover;">` : `<i class="fa-solid ${camp.stamp_icon_url || 'fa-star'}"></i>`;
        
        // Real stats (defaults to 0 for new campaigns)
        const scans = camp.total_scans || 0;
        const rewards = camp.total_rewards || 0;
        document.getElementById('hub-stat-scans').textContent = scans.toLocaleString();
        document.getElementById('hub-stat-rewards').textContent = rewards.toLocaleString();

        // Setup Buttons
        document.getElementById('hub-btn-edit').onclick = () => window.selectCampaign(id);
        document.getElementById('hub-btn-push').onclick = () => {
            hub.style.display = 'none';
            // Route to marketing
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
            const markTab = document.getElementById('tab-marketing');
            if(markTab) markTab.classList.add('active');
            const markBtn = document.querySelector('.nav-tab[data-tab="tab-marketing"]');
            if(markBtn) markBtn.classList.add('active');
        };
        document.getElementById('hub-btn-delete').onclick = () => {
            hub.style.display = 'none';
            window.deleteCampaign(id);
        };

        hub.style.display = 'flex';
    } catch(e) {
        console.error(e);
    }
};

window.addEventListener('beforeunload', function (e) {
    const builderActive = document.getElementById('tab-builder') && document.getElementById('tab-builder').classList.contains('active');
    if (builderActive) {
        e.preventDefault();
        e.returnValue = 'Tienes cambios sin guardar en tu campaña. ¿Seguro que quieres salir?';
    }
});

window.triggerRealAIMagicDesign = async function() {
    const btn = document.getElementById('btn-real-ai');
    const originalText = btn.innerHTML;
    
    // UI Loading state
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Analizando...';
    btn.style.opacity = '0.8';
    btn.style.pointerEvents = 'none';
    
    const iphone = document.querySelector('.iphone-pro-mockup');
    if(iphone) iphone.style.animation = "spinY 1.5s infinite cubic-bezier(0.175, 0.885, 0.32, 1.275)";
    
    if (typeof showToast === 'function') showToast("Gemini AI está analizando tu negocio...", "info");

    const industry = document.getElementById('business-category-input') ? document.getElementById('business-category-input').value : 'General';
    const businessName = document.getElementById('rest-name') ? document.getElementById('rest-name').value : 'Mi Negocio';

    try {
        const token = localStorage.getItem('merchant_token');
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ industry, businessName })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('/api/ai/magic-builder', reqOpts);
        
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.error || 'Error al conectar con Gemini API');
        }
        
        const strategy = await res.json();
        
        // Update DOM inputs
        if (document.getElementById('color-primary')) document.getElementById('color-primary').value = strategy.primaryColor || '#1e1b4b';
        if (document.getElementById('color-accent')) document.getElementById('color-accent').value = strategy.accentColor || '#8b5cf6';
        if (document.getElementById('unified-reward')) document.getElementById('unified-reward').value = strategy.reward || 'Premio Sorpresa';
        if (document.getElementById('stamps-reward')) document.getElementById('stamps-reward').value = strategy.reward || 'Premio Sorpresa';
        if (document.getElementById('unified-desc')) document.getElementById('unified-desc').value = strategy.instruction || 'Acumula visitas para ganar.';
        if (document.getElementById('stamps-total')) document.getElementById('stamps-total').value = strategy.stampsTotal || 5;
        if (document.getElementById('program-type-select')) document.getElementById('program-type-select').value = 'stamps';

        // Show Tip
        let tipBox = document.getElementById('ai-mkt-tip');
        if (!tipBox) {
            tipBox = document.createElement('div');
            tipBox.id = 'ai-mkt-tip';
            tipBox.style = 'margin-top:20px; background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.3); border-radius:12px; padding:16px; color:#4c1d95; font-size:13px; font-weight:600; line-height:1.5; animation:fadeIn 0.5s;';
            if (btn && btn.parentElement && btn.parentElement.parentElement) {
                btn.parentElement.parentElement.appendChild(tipBox);
            }
        }
        tipBox.innerHTML = `🤖 <b>Gemini AI:</b> ${strategy.tip}`;

        // Force UI update
        if (typeof updatePassRender === 'function') updatePassRender();

        if (typeof showToast === 'function') showToast("¡Estrategia Gemini Aplicada!", "success");
        
        try {
            if (window.JSConfetti) {
                const jsConfetti = new window.JSConfetti();
                jsConfetti.addConfetti({ emojis: ['🧠', '✨', '⚡️'], confettiNumber: 40 });
            }
        } catch(e) {}

    } catch (err) {
        console.error("Gemini Error:", err);
        if (typeof showToast === 'function') showToast(err.message || "Error al generar estrategia con Gemini.", "error");
    } finally {
        btn.innerHTML = originalText;
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
        if(iphone) iphone.style.animation = "";
    }
};
