import re

with open('pass.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for stamps grid
css_to_add = """
        .stamps-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            margin-top: 15px;
            margin-bottom: 20px;
            justify-items: center;
        }
        .stamp-circle {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            border: 2px dashed rgba(255,255,255,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(255,255,255,0.05);
            transition: all 0.3s ease;
            position: relative;
        }
        .stamp-circle.earned {
            border: 2px solid var(--primary);
            background-color: rgba(255,255,255,0.9);
            box-shadow: 0 0 10px var(--primary);
            animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .stamp-image {
            width: 70%;
            height: 70%;
            object-fit: contain;
            border-radius: 50%;
        }
        .stamp-icon {
            font-size: 20px;
            color: var(--primary);
        }
        @keyframes popIn {
            0% { transform: scale(0); }
            80% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
"""
if '.stamps-grid {' not in content:
    content = content.replace('</style>', f'{css_to_add}\n    </style>')

# 2. Replace the old stamps amount with the new grid container
old_stamps_html = """                <div class="stamps-amount" id="ui-stamps-main">0</div>"""
new_stamps_html = """                <div class="stamps-grid" id="ui-stamps-grid"></div>"""
content = content.replace(old_stamps_html, new_stamps_html)

# 3. Update the JS logic to render the grid
js_logic_old = "document.getElementById('ui-stamps-main').textContent = customer.stamps_count || 0;"
js_logic_new = """
                // Generar Cuadrícula de Sellos Visual
                const gridContainer = document.getElementById('ui-stamps-grid');
                if (gridContainer) {
                    const totalStampsReq = (campaign.rules_config && campaign.rules_config.stamps_total) ? campaign.rules_config.stamps_total : 10;
                    const earnedStamps = customer.stamps_count || 0;
                    gridContainer.innerHTML = '';
                    
                    // Ajustar columnas dinámicamente si hay muchos sellos
                    if (totalStampsReq > 10) gridContainer.style.gridTemplateColumns = 'repeat(6, 1fr)';
                    if (totalStampsReq <= 5) gridContainer.style.gridTemplateColumns = `repeat(${totalStampsReq}, 1fr)`;

                    const iconSrc = campaign.stamp_icon_url || 'fa-star';
                    const isImage = iconSrc.startsWith('data:image') || iconSrc.startsWith('http');
                    
                    for (let i = 0; i < totalStampsReq; i++) {
                        const circle = document.createElement('div');
                        circle.className = 'stamp-circle' + (i < earnedStamps ? ' earned' : '');
                        
                        if (i < earnedStamps) {
                            if (isImage) {
                                circle.innerHTML = `<img src="${iconSrc}" class="stamp-image">`;
                            } else {
                                circle.innerHTML = `<i class="fa-solid ${iconSrc} stamp-icon"></i>`;
                            }
                        }
                        
                        gridContainer.appendChild(circle);
                    }
                }
"""
content = content.replace(js_logic_old, js_logic_new)

# 4. Add Stripe CTA Customization
# Old button: <button class="btn-wallet" id="btn-schedule-appointment"...
btn_html_old = """<button class="btn-wallet" id="btn-schedule-appointment" style="display:none; background: var(--primary); margin-bottom: 12px; color: white;" onclick="openAppointmentModal()">
            <i class="fa-solid fa-calendar-check"></i> Agendar Cita o Servicio
        </button>"""
btn_html_new = """<button class="btn-wallet" id="btn-schedule-appointment" style="display:none; background: var(--primary); margin-bottom: 12px; color: white;" onclick="openAppointmentModal()">
            <i class="fa-solid fa-calendar-check"></i> <span id="ui-cta-text">Agendar Cita o Servicio</span>
        </button>"""
content = content.replace(btn_html_old, btn_html_new)

js_cta_injection = """
                if (merchant && merchant.business_type === 'professional') {
                    document.getElementById('ui-vip').style.display = 'none';
                    const btnAppt = document.getElementById('btn-schedule-appointment');
                    btnAppt.style.display = 'block';
                    
                    // Update label if custom
                    if (campaign.custom_cta_label) {
                        document.getElementById('ui-cta-text').textContent = campaign.custom_cta_label;
                    }
                    
                    // Check if Stripe is configured
                    if (merchant.stripe_keys && merchant.stripe_keys.stripe_pub_key) {
                        // Change action to Stripe if they provided a payment link in custom_cta_url or default
                        btnAppt.onclick = () => {
                            if (campaign.banner_url && campaign.banner_url.includes('stripe.com')) {
                                window.location.href = campaign.banner_url; // We'll hijack banner_url for stripe link as hack for now
                            } else {
                                alert('El profesional tiene Stripe activo pero no configuró su Payment Link.');
                            }
                        };
                        document.getElementById('ui-cta-text').innerHTML += " (Pagar vía Stripe)";
                    }
                }
"""
content = content.replace("""if (merchant && merchant.business_type === 'professional') {
                    document.getElementById('ui-vip').style.display = 'none';
                    document.getElementById('btn-schedule-appointment').style.display = 'block';
                }""", js_cta_injection)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("pass.html updated successfully.")
