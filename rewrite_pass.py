import re

with open('pass.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """        <div class="digital-card" id="digital-card">
            <div class="digital-card-banner" id="ui-card-banner"></div>
            
            <div class="card-header">
                <img src="" id="ui-merchant-logo" class="merchant-logo" alt="Logo">
                <div class="vip-badge" id="ui-vip">BRONCE</div>
            </div>
            
            <div class="campaign-title" id="ui-campaign-title"></div>

            <div class="balance-section" id="ui-balance-section" style="display:none;">
                <div class="balance-label">Cashback Disponible</div>
                <div class="balance-amount" id="ui-balance">$0.00</div>
            </div>
            
            <div class="stamps-section" id="ui-stamps-section" style="display:none;">
                <div class="stamps-label">Sellos Acumulados</div>
                <div class="stamps-grid" id="ui-stamps-grid"></div>
            </div>

            <div class="qr-container" id="qrcode"></div>
            
            <div class="customer-name" id="ui-customer-name">Cargando...</div>
        </div>"""

replacement = """        <div id="digital-card" style="background: #ffffff; border-radius: 20px; padding: 24px; position: relative; overflow: hidden; box-shadow: 0 16px 40px rgba(0,0,0,0.12); display: flex; flex-direction: column; min-height: 250px; border: 1px solid var(--primary);">
            
            <!-- Top row: Logo and "10 SELLOS" -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <div style="flex: 1; max-width: 160px; display: flex; align-items: center;">
                    <img id="ui-merchant-logo" src="" style="width: 100%; max-height: 45px; object-fit: contain; object-position: left center; display: none;" alt="Logo" />
                    <div id="ui-default-logo" style="display: flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-crown" style="color: var(--primary); font-size: 24px;"></i>
                        <span id="ui-campaign-title" style="font-weight: 800; font-size: 20px; color: #111827; letter-spacing: -0.5px;">Mi Negocio</span>
                    </div>
                </div>
                <div id="ui-top-right-stamps" style="display: none; text-align: right; align-items: center; gap: 8px;">
                    <span id="ui-stamps-top-label" style="font-size: 11px; font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: 0.5px;">SELLOS</span>
                    <i class="fa-solid fa-wifi" style="transform: rotate(90deg); color: var(--primary); opacity: 0.8; font-size: 14px;"></i>
                </div>
            </div>

            <!-- Middle Body (Dynamic: Stamps vs Cashback) -->
            <div id="ui-stamps-section" style="display: none; flex-direction: column; flex-grow: 1;">
                <div style="font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.5px; line-height: 1.4;">ACUMULA SELLOS<br>Y OBTÉN TU RECOMPENSA</div>
                <div id="ui-stamps-grid" style="display: flex; flex-wrap: wrap; gap: 14px; position: relative; margin-bottom: 20px;"></div>
            </div>

            <div id="ui-balance-section" style="display: none; flex-direction: column; flex-grow: 1;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
                    <div>
                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 1px;">NIVEL</div>
                        <div id="ui-vip" style="font-size: 28px; font-weight: 800; color: var(--primary); letter-spacing: -1px; display: flex; align-items: center; gap: 8px;">ÉLITE</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 1px;">CASHBACK</div>
                        <div id="ui-balance" style="font-size: 24px; font-weight: 800; color: #111827;">$0.00</div>
                        <div style="font-size: 10px; font-weight: 600; color: var(--primary); text-transform: uppercase; margin-top: 2px;">Disponible</div>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: auto;">
                    <div>
                        <div style="font-size: 10px; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 1px;">CLIENTE</div>
                        <div id="ui-customer-name" style="font-size: 16px; font-weight: 800; color: #111827;">Cargando...</div>
                    </div>
                </div>
            </div>

            <!-- Bottom row: Instructions and QR -->
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: auto; padding-top: 16px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="color: var(--primary); font-size: 24px;"><i class="fa-solid fa-expand"></i></div>
                    <div style="font-size: 10px; font-weight: 600; color: #4b5563; text-transform: uppercase; line-height: 1.4; letter-spacing: 0.5px;">ESCANEA TU TARJETA<br>EN CAJA</div>
                </div>
                <div style="width: 70px; height: 70px; background: white; padding: 4px; border-radius: 8px; border: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: center;" id="qrcode">
                    <!-- QR goes here -->
                </div>
            </div>
        </div>"""

text = html.replace(target, replacement)

# We need to fix the render logic inside pass.html because we changed IDs and structure.
target_js = """                if (campaign.type === 'stamps') {
                    document.getElementById('ui-stamps-section').style.display = 'block';
                    document.getElementById('ui-stamps-stat').textContent = customer.stamps_count;
                    
                    const grid = document.getElementById('ui-stamps-grid');
                    grid.innerHTML = '';
                    const totalStamps = campaign.rules_config.stamps_total || 5;
                    const earnedStamps = customer.stamps_count;
                    for (let i = 0; i < totalStamps; i++) {
                        const stamp = document.createElement('div');
                        stamp.className = 'stamp-circle ' + (i < earnedStamps ? 'earned' : '');
                        stamp.innerHTML = i < earnedStamps ? `<i class="fa-solid fa-check"></i>` : i + 1;
                        grid.appendChild(stamp);
                    }
                } else {
                    document.getElementById('ui-balance-section').style.display = 'block';
                    document.getElementById('ui-balance').textContent = `$${customer.current_balance}`;
                }"""

replacement_js = """                if (campaign.type === 'stamps') {
                    document.getElementById('ui-stamps-section').style.display = 'flex';
                    document.getElementById('ui-top-right-stamps').style.display = 'flex';
                    document.getElementById('ui-stamps-top-label').textContent = `${campaign.rules_config.stamps_total || 5} SELLOS`;
                    document.getElementById('ui-stamps-stat').textContent = customer.stamps_count;
                    
                    const grid = document.getElementById('ui-stamps-grid');
                    grid.innerHTML = '<div style="position:absolute; top:50%; left:5%; right:5%; height:2px; background:#f3f4f6; z-index:0; transform:translateY(-50%);"></div>';
                    
                    const totalStamps = campaign.rules_config.stamps_total || 5;
                    const earnedStamps = customer.stamps_count;
                    for (let i = 0; i < totalStamps; i++) {
                        if (i < earnedStamps) {
                            grid.innerHTML += `<div style="width:36px; height:36px; border-radius:50%; background:var(--primary); color:white; display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:bold; z-index:1; box-shadow:0 0 0 4px #ffffff;">
                                <i class="fa-solid fa-check"></i>
                            </div>`;
                        } else {
                            grid.innerHTML += `<div style="width:36px; height:36px; border-radius:50%; background:white; border:2px solid #e5e7eb; color:#9ca3af; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600; z-index:1; box-shadow:0 0 0 4px #ffffff;">
                                ${i + 1}
                            </div>`;
                        }
                    }
                } else {
                    document.getElementById('ui-balance-section').style.display = 'flex';
                    document.getElementById('ui-balance').textContent = `$${customer.current_balance}`;
                }"""

text = text.replace(target_js, replacement_js)

# Fix logo
target_logo = """                if (campaign.logo_url) {
                    const img = document.getElementById('ui-merchant-logo');
                    img.src = campaign.logo_url;
                    img.style.display = 'block';
                }"""

replacement_logo = """                if (campaign.logo_url) {
                    const img = document.getElementById('ui-merchant-logo');
                    img.src = campaign.logo_url;
                    img.style.display = 'block';
                    document.getElementById('ui-default-logo').style.display = 'none';
                }"""
text = text.replace(target_logo, replacement_logo)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(text)
