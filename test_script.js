        let supabase;
        let merchantData;
        let selectedCampaignId = null;

        document.addEventListener('DOMContentLoaded', async () => {
            try {
                // 1. Fetch config to init Supabase
                const configRes = await fetch('/api/config');
                const config = await configRes.json();
                supabase = window.supabase.createClient(config.supabaseUrl, config.supabaseAnonKey);
                
                // 2. Get slug from URL or Subdomain
                const hostname = window.location.hostname;
                const parts = hostname.split('.');
                const ignoredSubdomains = ['www', 'app', 'panel', 'api', 'localhost', 'fideliorewards', '127'];
                let slug = '';

                if (parts.length >= 2 && !ignoredSubdomains.includes(parts[0])) {
                    slug = parts[0];
                } else {
                    slug = window.location.pathname.replace('/', '').toLowerCase();
                }
                
                if (!slug) {
                    Swal.fire('Error', 'Restaurante no especificado', 'error');
                    return;
                }

                // 3. Fetch Merchant by Username
                let { data, error } = await supabase
                    .from('merchants')
                    .select('*')
                    .filter('appointment_settings->landing_prefs->>username', 'eq', slug)
                    .limit(1)
                    .single();
                    
                if (error || !data) {
                    // Try by business name fallback just in case
                    let { data: fallbackData } = await supabase
                        .from('merchants')
                        .select('*')
                        .ilike('business_name', '%' + slug + '%')
                        .limit(1)
                        .single();
                        
                    if (fallbackData) {
                        data = fallbackData;
                    } else {
                        throw new Error('Merchant not found');
                    }
                }

                if (error || !data) {
                    throw new Error('Restaurante no encontrado');
                }

                merchantData = data;
                
                // Override con landing_prefs si existen
                const prefs = merchantData.appointment_settings?.landing_prefs || {};
                if (prefs.portal_color) merchantData.color_primary = prefs.portal_color;
                if (prefs.portal_logo) merchantData.logo_url = prefs.portal_logo;

                // 4. Apply Visual Branding
                document.getElementById('merchant_id').value = merchantData.id;
                document.getElementById('merchant-name').textContent = merchantData.business_name;
                document.title = `${merchantData.business_name} - Registro de Lealtad`;
                
                if (merchantData.color_primary) {
                    document.documentElement.style.setProperty('--primary', merchantData.color_primary);
                }
                
                if (merchantData.banner_url) {
                    document.getElementById('banner').style.backgroundImage = `url('${merchantData.banner_url}')`;
                }
                
                const logoEl = document.getElementById('logo');
                if (merchantData.logo_url) {
                    logoEl.src = merchantData.logo_url;
                } else {
                    logoEl.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(merchantData.business_name)}&background=${(merchantData.color_primary||'8b5cf6').replace('#','')}&color=fff&size=128`;
                }

                // 5. Fetch Campaigns
                const { data: campaigns, error: campError } = await supabase
                    .from('campaigns')
                    .select('*')
                    .eq('merchant_id', merchantData.id)
                    .eq('is_active', true);
                    
                if (campError) throw campError;
                
                let visibleCampaigns = campaigns || [];
                if (merchantData.business_type === 'professional') {
                    visibleCampaigns = visibleCampaigns.filter(c => c.type === 'stamps');
                    document.getElementById('merchant-subtitle').textContent = "Selecciona tu programa y regístrate para obtener tu tarjeta.";
                }

                const grid = document.getElementById('campaign-grid');
                if (visibleCampaigns.length === 0) {
                    grid.innerHTML = '<p style="text-align:center; color:var(--text-muted);">No hay campañas activas en este momento.</p>';
                } else {
                    visibleCampaigns.forEach(camp => {
                        const card = document.createElement('div');
                        card.className = 'campaign-card';
                        if (camp.color_primary) {
                            card.style.setProperty('--card-primary', camp.color_primary);
                        }
                        
                        let typeLabel = 'Campaña';
                        let purposeHtml = '';
                        let termsHtml = '';

                        if (camp.type === 'stamps') typeLabel = 'Sellos';
                        else if (camp.type === 'cashback') typeLabel = 'Cashback';
                        else if (camp.type === 'discount') {
                            typeLabel = 'Descuento';
                            if (camp.rules_config?.discount?.purpose) purposeHtml = `<p style="font-size:13px; margin:8px 0; color:var(--text-muted);">${camp.rules_config.discount.purpose}</p>`;
                            if (camp.rules_config?.discount?.conditions) termsHtml = `<p style="font-size:11px; margin-top:8px; color:rgba(0,0,0,0.5);">* ${camp.rules_config.discount.conditions}</p>`;
                        }
                        else if (camp.type === 'coupons') {
                            typeLabel = 'Cupón Promocional';
                            if (camp.rules_config?.coupons?.desc) purposeHtml = `<p style="font-size:13px; margin:8px 0; color:var(--text-muted);">${camp.rules_config.coupons.desc}</p>`;
                            if (camp.rules_config?.coupons?.terms) termsHtml = `<p style="font-size:11px; margin-top:8px; color:rgba(0,0,0,0.5);">* ${camp.rules_config.coupons.terms}</p>`;
                        }
                        else if (camp.type === 'multipass') {
                            typeLabel = 'Multipass';
                            if (camp.rules_config?.multipass?.service) purposeHtml = `<p style="font-size:13px; margin:8px 0; color:var(--text-muted);">${camp.rules_config.multipass.count} Pases para ${camp.rules_config.multipass.service}</p>`;
                        }
                        
                        card.innerHTML = `
                            <div class="campaign-type-badge">${typeLabel}</div>
                            <h3 class="campaign-name">${camp.name}</h3>
                            ${purposeHtml}
                            ${termsHtml}
                        `;
                        
                        card.addEventListener('click', () => {
                            selectedCampaignId = camp.id;
                            document.getElementById('selected-campaign-badge').textContent = `Campaña: ${camp.name}`;
                            if (camp.color_primary) {
                                document.getElementById('selected-campaign-badge').style.backgroundColor = camp.color_primary;
                                document.documentElement.style.setProperty('--primary', camp.color_primary);
                            }
                            
                            document.getElementById('campaigns-container').style.display = 'none';
                            document.getElementById('registration-form-container').style.display = 'block';
                        });
                        
                        grid.appendChild(card);
                    });
                }
                
                document.getElementById('campaigns-container').style.display = 'block';
                document.getElementById('loading-screen').style.display = 'none';

            } catch (err) {
                console.error(err);
                document.getElementById('loading-screen').style.display = 'none';
                document.getElementById('registration-form-container').innerHTML = `
                    <div style="text-align:center; padding: 40px 0;">
                        <i class="fa-solid fa-store-slash" style="font-size:48px; color:var(--text-muted); margin-bottom:16px;"></i>
                        <h2>Restaurante/Negocio no encontrado</h2>
                        <p style="color:var(--text-muted); margin-top:8px;">Verifica que la dirección web sea correcta.</p>
                    </div>
                `;
                document.getElementById('registration-form-container').style.display = 'block';
            }
        });
        
        document.getElementById('btn-back').addEventListener('click', () => {
            document.getElementById('registration-form-container').style.display = 'none';
            document.getElementById('campaigns-container').style.display = 'block';
            // Reset primary color to merchant default
            if (merchantData && merchantData.color_primary) {
                document.documentElement.style.setProperty('--primary', merchantData.color_primary);
            }
        });

        // 6. Handle Registration
        document.getElementById('public-register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!selectedCampaignId) {
                Swal.fire('Error', 'Por favor selecciona una campaña primero.', 'warning');
                return;
            }
            
            const btn = document.getElementById('btn-submit');
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Creando Tarjeta...';
            btn.disabled = true;

            const fullName = document.getElementById('full_name').value.trim();
            const email = document.getElementById('email').value.trim().toLowerCase();
            const phone = document.getElementById('phone').value.trim();
            const birthdayInput = document.getElementById('birthday');
            const birthday = birthdayInput ? birthdayInput.value : null;
            const merchantId = document.getElementById('merchant_id').value;

            try {
                // Check if user already exists
                const { data: existing } = await supabase
                    .from('customers')
                    .select('id')
                    .eq('merchant_id', merchantId)
                    .eq('email', email)
                    .single();

                let customerId;
                
                if (existing) {
                    customerId = existing.id;
                } else {
                    // Insert new customer
                    const { data: newCustomer, error } = await supabase
                        .from('customers')
                        .insert([{
                            merchant_id: merchantId,
                            full_name: fullName,
                            email: email,
                            phone: phone || null,
                            birthday: birthday || null,
                            balance_cashback: 0,
                            stamps_count: 0,
                            vip_tier: 'Bronce'
                        }])
                        .select()
                        .single();

                    if (error) throw error;
                    customerId = newCustomer.id;
                }
                
                // Link customer to campaign
                const { data: existingLink } = await supabase
                    .from('customer_campaigns')
                    .select('id')
                    .eq('customer_id', customerId)
                    .eq('campaign_id', selectedCampaignId)
                    .single();
                    
                if (!existingLink) {
                    await supabase.from('customer_campaigns').insert([{
                        customer_id: customerId,
                        campaign_id: selectedCampaignId
                    }]);
                }

                // Success! Redirect to digital pass
                window.location.href = `/pass.html?id=${customerId}&campaign=${selectedCampaignId}`;

            } catch (err) {
                Swal.fire('Error', 'Hubo un problema al crear tu tarjeta. Intenta de nuevo.', 'error');
                console.error(err);
                btn.innerHTML = 'Generar Mi Tarjeta Digital';
                btn.disabled = false;
            }
        });
