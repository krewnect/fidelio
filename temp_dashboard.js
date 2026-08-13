// --- FIDELIO UNIVERSAL BUSINESS ENGINE (FIDELITO SUPPORT ASSISTANT) --- //

let state = {};
let saveTimeout = null;

(async function initFidelio() {
    try {
        // Cargar datos reales
        await loadDataFromSupabase();
    } catch (err) {
        console.error("Dashboard DB init error:", err);
        alert("CRASH LOG DB (por favor muéstrale esto a tu asistente):\n" + err.stack);
    }

    // PRESETS DICTIONARY FOR MULTI-INDUSTRY GIROS
    const categoryPresets = {
        restaurant: {
            label: "Restaurantes & Gastronomía",
            name: "Don Pedro Gourmet",
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

    // --- DATABASE SYNC ---

    async function loadDataFromSupabase() {
        if (!window.supabaseClient || !window.merchantSession) return false;
        const merchantId = window.merchantSession.user.id;

        const { data: merchantData, error } = await window.supabaseClient
            .from('merchants')
            .select('*')
            .eq('id', merchantId)
            .single();

        if (error) {
            console.error("Error cargando perfil:", error);
            showToast("Error al cargar configuración", "warning");
            return false;
        }

        const { data: custData } = await window.supabaseClient
            .from('customers')
            .select('*')
            .eq('merchant_id', merchantId);

        const { data: transData } = await window.supabaseClient
            .from('transactions')
            .select('*')
            .eq('merchant_id', merchantId);

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
            branches: [],
            customers: custData || [],
            transactions: transData || [],
            activeWallet: "apple"
        };

        // --- INJECT MERCHANT QR ---
        const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=1000x1000&data=${encodeURIComponent(window.location.origin + '/pass.html?m=' + merchantId)}`;
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
    }

    async function saveDesignToSupabase() {
        if (!window.supabaseClient || !state.tenantId) return;
        
        const updates = {
            business_name: state.restaurantName,
            industry: state.category,
            color_primary: state.colorPrimary,
            color_accent: state.colorAccent,
            cashback_percent: state.cashbackPercent,
            stamps_total: state.stampsTotal,
            stamps_reward_text: state.stampsReward,
            logo_url: state.customLogoUrl,
            banner_url: state.customBannerUrl
        };

        const { error } = await window.supabaseClient
            .from('merchants')
            .update(updates)
            .eq('id', state.tenantId);
            
        if (!error) {
            showToast("Guardado automático en la nube ☁️", "success");
        }
    }

    function scheduleAutoSave() {
        if (saveTimeout) clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            saveDesignToSupabase();
        }, 1500);
    }

    // --- TOAST NOTIFICATIONS ---
    function showToast(message, type = "info") {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = 'toast-msg';
        
        let iconClass = 'fa-circle-info';
        if (type === 'success') iconClass = 'fa-circle-check text-emerald';
        if (type === 'warning') iconClass = 'fa-triangle-exclamation';

        toast.innerHTML = `<i class="fa-solid ${iconClass}"></i> <span>${message}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // --- 1-CLICK INTUITIVE PRESET LOAD FUNCTION ---
    window.loadDemoPreset = function(presetKey) {
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
        document.getElementById('tier-bronce-name').addEventListener('input', (e) => {
            state.vipTiers.bronce.name = e.target.value;
            updatePassRender();
        });
        document.getElementById('tier-bronce-cb').addEventListener('input', (e) => {
            state.vipTiers.bronce.cashbackPercent = parseFloat(e.target.value) || 5;
            updatePassRender();
        });

        document.getElementById('tier-plata-name').addEventListener('input', (e) => {
            state.vipTiers.plata.name = e.target.value;
            updatePassRender();
        });
        document.getElementById('tier-plata-cb').addEventListener('input', (e) => {
            state.vipTiers.plata.cashbackPercent = parseFloat(e.target.value) || 10;
            updatePassRender();
        });

        document.getElementById('tier-oro-name').addEventListener('input', (e) => {
            state.vipTiers.oro.name = e.target.value;
            updatePassRender();
        });
        document.getElementById('tier-oro-cb').addEventListener('input', (e) => {
            state.vipTiers.oro.cashbackPercent = parseFloat(e.target.value) || 15;
            updatePassRender();
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
            tenantDatabase[currentTenantId].activeMode = mode;

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

    // --- 20 SUCURSALES MANAGER RENDERING ---
    const branchesList = document.getElementById('branches-list');
    const branchCount = document.getElementById('branch-count');

    function renderBranches() {
        if (!branchesList) return;
        branchCount.textContent = state.branches.length;
        branchesList.innerHTML = '';

        state.branches.forEach((b, idx) => {
            const div = document.createElement('div');
            div.className = 'branch-item';
            div.innerHTML = `
                <div class="branch-info">
                    <strong>Sucursal ${idx + 1}: ${b.name}</strong>
                    <p>${b.address}</p>
                    <span class="branch-gps"><i class="fa-solid fa-location-crosshairs"></i> GPS: ${b.lat.toFixed(4)}, ${b.lng.toFixed(4)} (Geofence 100m Activo)</span>
                </div>
                <button class="btn btn-outline" style="padding:6px 12px; font-size:12px; color:var(--pink);" onclick="removeBranch(${b.id})">
                    <i class="fa-solid fa-trash"></i>
                </button>
            `;
            branchesList.appendChild(div);
        });
    }

    const btnAddBranch = document.getElementById('btn-add-branch');
    if (btnAddBranch) {
        btnAddBranch.addEventListener('click', () => {
            if (state.branches.length >= 20) {
                showToast("Límite máximo de 20 sucursales alcanzado.", "warning");
                return;
            }

            const newId = Date.now();
            const branchNames = ["Sucursal Pedregal", "Sucursal Interlomas", "Sucursal Satélite", "Sucursal Coapa"];
            const randomName = branchNames[Math.floor(Math.random() * branchNames.length)] + ` #${state.branches.length + 1}`;

            state.branches.push({
                id: newId,
                name: randomName,
                address: "Av. Principal " + (100 + state.branches.length * 20) + ", CDMX",
                lat: 19.4000 + (Math.random() * 0.05),
                lng: -99.1500 - (Math.random() * 0.05)
            });

            renderBranches();
            showToast(`Sucursal agregada con éxito (${randomName}). Geofencing configurado.`, "success");
        });
    }

    window.removeBranch = function(id) {
        state.branches = state.branches.filter(b => b.id !== id);
        tenantDatabase[currentTenantId].branches = state.branches;
        renderBranches();
        showToast("Sucursal eliminada.", "info");
    };

    // --- CUSTOMER ONBOARDING FORM MODAL ---
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
                alert('Nombre y teléfono son obligatorios.');
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
                alert('Error registrando cliente: ' + err.message);
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
                alert("Error: " + err.message);
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
                alert("Error: " + err.message);
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

    function renderCRMTable() {
        if (!crmTableBody) return;
        const searchTerm = crmSearchInput.value.toLowerCase();
        const tierFilter = crmFilterTier.value;
        const statusFilter = crmFilterStatus.value;

        const filtered = state.customers.filter(c => {
            const matchesSearch = c.name.toLowerCase().includes(searchTerm) || 
                                  c.phone.includes(searchTerm) || 
                                  c.email.toLowerCase().includes(searchTerm) ||
                                  (c.birthday && c.birthday.toLowerCase().includes(searchTerm)) ||
                                  c.id.toLowerCase().includes(searchTerm);
            
            const matchesTier = tierFilter === 'all' || c.tier === tierFilter;
            const matchesStatus = statusFilter === 'all' || c.status === statusFilter;

            return matchesSearch && matchesTier && matchesStatus;
        });

        crmCountBadge.textContent = state.customers.length;
        crmTableBody.innerHTML = '';

        if (filtered.length === 0) {
            crmTableBody.innerHTML = `<tr><td colspan="10" style="text-align:center; color: var(--text-muted); padding: 30px;">No se encontraron registros de clientes.</td></tr>`;
            return;
        }

        filtered.forEach(c => {
            const tr = document.createElement('tr');
            
            // Map Supabase variables
            const balance = c.current_balance || 0;
            const spent = c.lifetime_value || 0;
            const tier = spent > 3000 ? 'Oro VIP' : (spent > 1000 ? 'Plata VIP' : 'Bronce VIP');
            const tierClass = tier.includes('Oro') ? 'oro' : tier.includes('Plata') ? 'plata' : 'bronce';
            const statusClass = c.visits > 0 ? 'activo' : 'riesgo';
            const walletIcon = 'fa-apple';
            const lastVisit = c.created_at ? new Date(c.created_at).toISOString().split('T')[0] : 'N/A';

            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${c.name.charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${c.name}</strong>
                            <small style="display:block; color:var(--text-muted);">${c.id.substring(0,8)}...</small>
                        </div>
                    </div>
                </td>
                <td>
                    <strong>${c.phone}</strong>
                    <small style="display:block; color:var(--text-muted);">${c.email || 'Sin correo'}</small>
                </td>
                <td><strong style="color:var(--cyan);"><i class="fa-solid fa-cake-candles"></i> N/A</strong></td>
                <td><span class="tier-pill ${tierClass}">${tier}</span></td>
                <td><i class="fa-brands ${walletIcon}"></i> Apple Wallet</td>
                <td><strong class="text-emerald">$${balance.toFixed(2)} MXN</strong></td>
                <td><strong>${c.visits}/${state.stampsTotal}</strong></td>
                <td>$${spent.toFixed(2)} MXN</td>
                <td>${lastVisit}</td>
                <td><span class="badge-status ${statusClass}">${c.visits > 0 ? 'Activo' : 'Nuevo'}</span></td>
                <td>
                    <button class="btn btn-outline" style="padding:6px 12px; font-size:12px; margin-right: 4px;" title="Ver QR del Cliente" onclick="window.showCustomerQR('${c.id}', '${c.name.replace(/'/g, "\\'")}')">
                        <i class="fa-solid fa-qrcode"></i> QR
                    </button>
                    <button class="btn btn-outline" style="padding:6px 12px; font-size:12px;" title="Enviar Correo" onclick="alert('Iniciando envío de correo directo a ${c.email}')">
                        <i class="fa-solid fa-envelope"></i>
                    </button>
                </td>
            `;
            crmTableBody.appendChild(tr);
        });
    }

    // --- PASS RENDER FUNCTION WITH METALLIC BORDERS & DYNAMIC CONFIGURABLE TIERS ---
    const passRender = document.getElementById('pass-render');

    function updatePassRender() {
        if (!passRender) return;
        scheduleAutoSave(); // Trigger auto-save debouncer
        passRender.style.backgroundColor = state.colorPrimary;
        document.getElementById('render-name').textContent = state.restaurantName;
        
        const logoContainer = document.getElementById('render-logo-container');
        if (state.customLogoUrl) {
            logoContainer.innerHTML = `<img src="${state.customLogoUrl}" style="width:28px; height:28px; border-radius:6px; object-fit:cover;"> <span id="render-name">${state.restaurantName}</span>`;
        } else {
            logoContainer.innerHTML = `<i class="fa-solid ${state.iconClass}" id="render-icon" style="color:${state.colorAccent}"></i> <span id="render-name">${state.restaurantName}</span>`;
        }

        const bannerContainer = document.getElementById('render-banner-container');
        const bannerImg = document.getElementById('render-banner-img');
        if (state.customBannerUrl) {
            bannerContainer.classList.remove('hidden');
            bannerImg.src = state.customBannerUrl;
        } else {
            bannerContainer.classList.add('hidden');
            bannerImg.src = '';
        }

        const sampleClient = state.customers[0] || { tier: "Oro VIP", balance: 0, stamps: 0 };

        passRender.classList.remove('tier-border-bronce', 'tier-border-plata', 'tier-border-oro');
        
        let currentTierConfig = state.vipTiers.oro;
        
        const clientTier = sampleClient.vip_tier || sampleClient.tier || 'Bronce';

        if (clientTier.toLowerCase().includes('oro')) {
            passRender.classList.add('tier-border-oro');
            currentTierConfig = state.vipTiers.oro;
        } else if (clientTier.toLowerCase().includes('plata')) {
            passRender.classList.add('tier-border-plata');
            currentTierConfig = state.vipTiers.plata;
        } else {
            passRender.classList.add('tier-border-bronce');
            currentTierConfig = state.vipTiers.bronce;
        }

        const vipCaption = document.getElementById('render-vip-caption');
        if (state.vipActive) {
            vipCaption.style.display = 'block';
            vipCaption.textContent = currentTierConfig.name.toUpperCase();
        } else {
            vipCaption.style.display = 'none';
        }

        const cashbackContainer = document.getElementById('render-cashback-container');
        if (state.cashbackActive) {
            cashbackContainer.style.display = 'block';
            const bal = sampleClient.current_balance !== undefined ? sampleClient.current_balance : (sampleClient.balance || 0);
            document.getElementById('render-balance').textContent = `$${bal.toFixed(2)} MXN`;
            document.getElementById('render-cashback-rate').textContent = `${currentTierConfig.cashbackPercent}% acumulable (${currentTierConfig.name})`;
        } else {
            cashbackContainer.style.display = 'none';
        }

        const stampsContainer = document.getElementById('render-stamps-container');
        if (state.stampsActive) {
            stampsContainer.style.display = 'block';
            const stampsGrid = document.getElementById('render-stamps-grid');
            stampsGrid.innerHTML = '';

            for (let i = 1; i <= state.stampsTotal; i++) {
                const node = document.createElement('div');
                if (i <= sampleClient.stamps) {
                    node.className = 'stamp-coin filled';
                    node.style.backgroundColor = state.colorAccent;
                    node.innerHTML = '<i class="fa-solid fa-check"></i>';
                } else {
                    node.className = 'stamp-coin empty';
                    node.textContent = i;
                }
                stampsGrid.appendChild(node);
            }
            document.getElementById('render-reward-text').textContent = `Premio: ${state.stampsReward}`;
        } else {
            stampsContainer.style.display = 'none';
        }

        const promoStrip = document.getElementById('render-promo-strip');
        if (state.dynamicActive && state.dynamicDesc.trim() !== '') {
            promoStrip.style.display = 'flex';
            document.getElementById('render-promo-text').textContent = state.dynamicDesc;
        } else {
            promoStrip.style.display = 'none';
        }
    }

    // --- UPLOAD HANDLERS ---
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
                    tenantDatabase[currentTenantId].customLogoUrl = evt.target.result;
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
            tenantDatabase[currentTenantId].customLogoUrl = null;
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
                    tenantDatabase[currentTenantId].customBannerUrl = evt.target.result;
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
            tenantDatabase[currentTenantId].customBannerUrl = null;
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
            navTabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const targetTab = tab.getAttribute('data-tab');
            document.getElementById(targetTab).classList.add('active');
        });
    });

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
    if (document.getElementById('rest-name')) {
        document.getElementById('rest-name').addEventListener('input', (e) => {
            state.restaurantName = e.target.value || "Comercio";
            updatePassRender();
        });
        document.getElementById('color-primary').addEventListener('input', (e) => {
            state.colorPrimary = e.target.value;
            updatePassRender();
        });
        document.getElementById('color-accent').addEventListener('input', (e) => {
            state.colorAccent = e.target.value;
            updatePassRender();
        });
        document.getElementById('rest-icon').addEventListener('change', (e) => {
            state.iconClass = e.target.value;
            updatePassRender();
        });

        document.getElementById('mech-cashback-check').addEventListener('change', (e) => {
            state.cashbackActive = e.target.checked;
            updatePassRender();
        });
        document.getElementById('cashback-percent').addEventListener('input', (e) => {
            state.cashbackPercent = parseFloat(e.target.value) || 0;
            updatePassRender();
        });

        document.getElementById('mech-stamps-check').addEventListener('change', (e) => {
            state.stampsActive = e.target.checked;
            updatePassRender();
        });
        document.getElementById('stamps-total').addEventListener('input', (e) => {
            state.stampsTotal = parseInt(e.target.value) || 5;
            updatePassRender();
        });
        document.getElementById('stamps-reward').addEventListener('input', (e) => {
            state.stampsReward = e.target.value || "Premio";
            updatePassRender();
        });

        document.getElementById('mech-dynamic-check').addEventListener('change', (e) => {
            state.dynamicActive = e.target.checked;
            updatePassRender();
        });
        document.getElementById('dynamic-desc').addEventListener('input', (e) => {
            state.dynamicDesc = e.target.value;
            updatePassRender();
        });

        document.getElementById('mech-vip-check').addEventListener('change', (e) => {
            state.vipActive = e.target.checked;
            updatePassRender();
        });
    }

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

    // --- LEADS MANAGEMENT (ADMIN ONLY) ---
    window.loadLeads = async function() {
        if (!window.merchantSession || window.merchantSession.user.email !== 'admin@fidelio.com') return;
        
        const tbody = document.getElementById('leads-table-body');
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Cargando prospectos...</td></tr>';
        
        const { data, error } = await window.supabaseClient
            .from('demo_requests')
            .select('*')
            .order('created_at', { ascending: false });
            
        if (error) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:#ef4444;">Error cargando prospectos: ${error.message}</td></tr>`;
            return;
        }
        
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">No hay solicitudes pendientes.</td></tr>';
            return;
        }
        
        tbody.innerHTML = '';
        data.forEach(lead => {
            const date = new Date(lead.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
            tbody.innerHTML += `
                <tr>
                    <td>${date}</td>
                    <td><strong style="color:#fff;">${lead.name}</strong></td>
                    <td>${lead.email}</td>
                    <td>${lead.phone}</td>
                </tr>
            `;
        });
    };

    // Initial Render Calls
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
        
        // ADMIN CHECK FOR LEADS TAB
        if (window.merchantSession.user.email === 'admin@fidelio.com') {
            document.getElementById('admin-leads-menu').style.display = 'block';
            document.getElementById('admin-leads-tab').style.display = 'block';
            
            // Re-attach listeners explicitly just in case for new tab
            document.getElementById('admin-leads-tab').addEventListener('click', (e) => {
                document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
                e.currentTarget.classList.add('active');
                document.getElementById('tab-leads').classList.add('active');
                window.loadLeads();
            });
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
    }

    if (btnSaveAccount) {
        btnSaveAccount.addEventListener('click', async () => {
            const newEmail = accEmail.value.trim();
            const newPassword = accPassword.value;
            
            const updates = {};
            if (newEmail && newEmail !== window.merchantSession.user.email) updates.email = newEmail;
            if (newPassword) updates.password = newPassword;

            if (Object.keys(updates).length === 0) return;

            btnSaveAccount.textContent = 'Actualizando...';
            const { data, error } = await window.supabaseClient.auth.updateUser(updates);
            
            if (error) {
                showToast(error.message, 'warning');
            } else {
                showToast('Credenciales actualizadas correctamente.', 'success');
                if (newPassword) accPassword.value = '';
                if (data.user) window.merchantSession.user = data.user;
            }
            btnSaveAccount.textContent = 'Actualizar Credenciales';
        });
    }

    if (btnLogout) {
        btnLogout.addEventListener('click', async () => {
            await window.supabaseClient.auth.signOut();
            window.location.href = '/';
        });
    }

    try {
        // Actualizar métricas del dashboard principal
        updateDashboardMetrics();

        // Actualizar encabezados
        if (state && state.restaurantName) {
            document.getElementById('header-restaurant-name').textContent = state.restaurantName;
            document.getElementById('header-business-category').textContent = state.category || "Restaurante";
        }

        // Inicializar UI
        updatePassRender();
        renderBranches();
        renderCRMTable();
    } catch (err) {
        console.error("Dashboard UI init error:", err);
        alert("CRASH LOG UI (por favor muéstrale esto a tu asistente):\n" + err.stack);
    }
})();
