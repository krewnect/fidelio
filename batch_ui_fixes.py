import re

# --- FIX INDEX.HTML ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Metric Cards: Delete Mock Data
# Replace 1,248 with 0
html = html.replace('<div class="metric-value">1,248</div>', '<div class="metric-value" id="ui-metric-users">0</div>')
# Replace $485 with $0
html = html.replace('<div class="metric-value">$485</div>', '<div class="metric-value" id="ui-metric-ticket">$0</div>')
# Replace 43.5% with 0%
html = html.replace('<div class="metric-value">43.5%</div>', '<div class="metric-value" id="ui-metric-redemption">0%</div>')
# Replace 2.8x with 0x
html = html.replace('<div class="metric-value">2.8x<span style="font-size:14px; color:var(--text-muted)">/mes</span></div>', '<div class="metric-value" id="ui-metric-frequency">0x<span style="font-size:14px; color:var(--text-muted)">/mes</span></div>')

# 2. Buttons to Purple
html = html.replace('class="btn btn-outline"', 'class="btn btn-primary"')
html = html.replace('class="btn btn-secondary"', 'class="btn btn-primary"')
html = html.replace('class="btn-wallet"', 'class="btn-wallet btn-primary"')
# Make 'Nueva Campaña' button purple
html = html.replace('class="btn btn-primary" onclick="openCampaignModal()" style="background:var(--surface-light); color:var(--text-color); border:1px solid var(--border-color);"', 'class="btn btn-primary" onclick="openCampaignModal()" style="background:var(--primary); color:#ffffff; border:none;"')
html = html.replace('onclick="openCampaignModal()" style="background: var(--surface-light); color: var(--text-color); border: 1px solid var(--border-color);"', 'onclick="openCampaignModal()" style="background: var(--primary); color: #ffffff; border: none;"')

# 3. Monetization Stripe for Professionals
# Hide Public and Secret keys in index.html, leave only Payment Link
old_keys = """                        <div style="margin-top: 15px;">
                            <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">Stripe Public Key</label>
                            <input type="text" id="stripe-pub-key" class="form-control" placeholder="pk_test_..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--bg-color); color: var(--text-color);">
                        </div>
                        <div style="margin-top: 15px;">
                            <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">Stripe Secret Key</label>
                            <input type="text" id="stripe-secret-key" class="form-control" placeholder="sk_test_..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--bg-color); color: var(--text-color);">
                        </div>"""
new_keys = """                        <!-- Public and Secret Keys hidden to simplify for professionals -->
                        <div style="display:none; margin-top: 15px;">
                            <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">Stripe Public Key</label>
                            <input type="text" id="stripe-pub-key" class="form-control" placeholder="pk_test_..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--bg-color); color: var(--text-color);">
                        </div>
                        <div style="display:none; margin-top: 15px;">
                            <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">Stripe Secret Key</label>
                            <input type="text" id="stripe-secret-key" class="form-control" placeholder="sk_test_..." style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--bg-color); color: var(--text-color);">
                        </div>"""
html = html.replace(old_keys, new_keys)

# 4. Redesign "The Bank"
old_bank = """                            <div style="display: flex; flex-direction: column; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <i class="fa-solid fa-wallet" style="color: var(--primary);"></i>
                                    <span>Total Prepagado (Histórico)</span>
                                </div>
                                <div id="bank-total-historical" style="font-weight: bold; font-size: 1.1rem;">$0.00</div>
                                <div style="font-size: 0.9rem; color: var(--text-muted);">Dinero total que han metido tus clientes al monedero.</div>
                            </div>
                            <div style="display: flex; flex-direction: column; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <i class="fa-solid fa-money-bill-wave" style="color: #10b981;"></i>
                                    <span>Bolsa de Dinero No Gastado</span>
                                </div>
                                <div id="bank-total-liability" style="font-weight: bold; font-size: 1.1rem; color: #10b981;">$0.00</div>
                                <div style="font-size: 0.9rem; color: var(--text-muted);">Pasivo actual: Dinero que tienen a favor para gastar.</div>
                            </div>"""

new_bank = """                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; width:100%;">
                                <div class="metric-card" style="border: 1px solid var(--primary); background: linear-gradient(145deg, rgba(139,92,246,0.1) 0%, rgba(0,0,0,0) 100%);">
                                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                                        <div style="background:var(--primary); width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                                            <i class="fa-solid fa-wallet" style="color: white; font-size: 18px;"></i>
                                        </div>
                                        <span style="font-weight:bold; color:var(--text-muted);">Total Prepagado (Histórico)</span>
                                    </div>
                                    <div id="bank-total-historical" style="font-weight: bold; font-size: 2rem; color: white;">$0.00</div>
                                    <div style="font-size: 0.85rem; color: var(--text-muted); margin-top:5px;">Dinero total ingresado a lo largo del tiempo.</div>
                                </div>
                                
                                <div class="metric-card" style="border: 1px solid #10b981; background: linear-gradient(145deg, rgba(16,185,129,0.1) 0%, rgba(0,0,0,0) 100%);">
                                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                                        <div style="background:#10b981; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                                            <i class="fa-solid fa-money-bill-wave" style="color: white; font-size: 18px;"></i>
                                        </div>
                                        <span style="font-weight:bold; color:var(--text-muted);">Bolsa de Dinero (Pasivo Actual)</span>
                                    </div>
                                    <div id="bank-total-liability" style="font-weight: bold; font-size: 2rem; color: #10b981;">$0.00</div>
                                    <div style="font-size: 0.85rem; color: var(--text-muted); margin-top:5px;">Saldo a favor vivo actualmente en los wallets.</div>
                                </div>
                            </div>"""

if "Total Prepagado (Histórico)" in html and "metric-card" not in old_bank:
    html = html.replace(old_bank, new_bank)

# 5. Redesign My Business (Pricing Table Feel)
old_business = """                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="color: var(--text-muted); font-size: 12px;">Suscripción Actual</div>
                                    <div style="font-weight: bold; font-size: 16px; color: #10b981;">
                                        <i class="fa-solid fa-clock"></i> Pruebas / Inactivo
                                    </div>
                                </div>
                                <div>
                                    <div style="color: var(--text-muted); font-size: 12px;">Lugares Founder Restantes</div>
                                    <div style="font-weight: bold; font-size: 16px; color: var(--primary);">
                                        <i class="fa-solid fa-fire"></i> 22 / 25 Disponibles
                                    </div>
                                </div>
                                <div>
                                    <div style="color: var(--text-muted); font-size: 12px;">Tarjetas Emitidas</div>
                                    <div style="font-weight: bold; font-size: 16px;">
                                        <i class="fa-solid fa-wallet" style="color: var(--primary);"></i> <span id="issued-cards-count">--</span>
                                    </div>
                                </div>
                                <div style="display:flex; gap:10px;">
                                    <button class="btn btn-outline" style="font-size: 12px; padding: 6px 12px;"><i class="fa-solid fa-file-invoice"></i> Factura</button>
                                    <button class="btn btn-outline" style="font-size: 12px; padding: 6px 12px;"><i class="fa-solid fa-building-columns"></i> Transferencia</button>
                                </div>
                            </div>
                            
                            <div style="margin-top: 30px; text-align: center; max-width: 500px; margin-left: auto; margin-right: auto;">
                                <div style="display: inline-flex; background: var(--surface-light); padding: 4px; border-radius: 20px; margin-bottom: 20px;">
                                    <div style="padding: 6px 16px; border-radius: 16px; font-size: 12px; cursor:pointer;">Mensual</div>
                                    <div style="background: var(--primary); color: white; padding: 6px 16px; border-radius: 16px; font-size: 12px; font-weight: bold; cursor:pointer;">Anual <span style="font-size: 10px; background: #10b981; padding: 2px 6px; border-radius: 10px; margin-left: 4px;">2 MESES GRATIS</span></div>
                                </div>
                                
                                <div style="font-size: 14px; font-weight: bold; color: var(--bg-color); background: #fbbf24; display: inline-block; padding: 4px 12px; border-radius: 20px; margin-bottom: 10px;">LICENCIA FOUNDER (DE POR VIDA)</div>
                                <div style="font-size: 48px; font-weight: 800; margin-bottom: 10px;">$9,999 <span style="font-size: 14px; font-weight: normal; color: var(--text-muted);">MXN / año + IVA (16%)</span></div>
                                <div style="font-size: 14px; color: var(--text-muted); margin-bottom: 20px;">Sucursales ilimitadas. Soporte VIP.</div>
                                
                                <div style="display: flex; gap: 10px; justify-content: center;">
                                    <input type="text" placeholder="Código Promo" style="padding: 10px 15px; border-radius: 8px; border: 1px solid var(--surface-light); background: var(--surface-color); color: white; width: 150px;">
                                    <button class="btn btn-primary" style="padding: 10px 30px; font-weight: bold;"><i class="fa-brands fa-stripe"></i> Procesar Pago</button>
                                </div>
                                <div style="margin-top: 15px; font-size: 10px; color: var(--text-muted);">Al procesar el pago o utilizar Fidelio, aceptas nuestro Aviso de Privacidad y los Términos y Condiciones.</div>
                            </div>"""

new_business = """                            <div class="metric-card" style="display: flex; flex-direction:column; gap:20px; align-items: center; justify-content: center; background: linear-gradient(135deg, rgba(30,27,75,1) 0%, rgba(0,0,0,1) 100%); border: 1px solid var(--primary); box-shadow: 0 10px 30px rgba(139,92,246,0.2);">
                                
                                <div style="display:flex; width:100%; justify-content:space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom:15px;">
                                    <div>
                                        <div style="color: var(--text-muted); font-size: 12px; text-transform:uppercase; letter-spacing:1px;">Plan Actual</div>
                                        <div style="font-weight: bold; font-size: 18px; color: #10b981; display:flex; align-items:center; gap:5px;">
                                            <i class="fa-solid fa-circle-check"></i> Pruebas / Inactivo
                                        </div>
                                    </div>
                                    <div>
                                        <div style="color: var(--text-muted); font-size: 12px; text-transform:uppercase; letter-spacing:1px;">Lugares Founder</div>
                                        <div style="font-weight: bold; font-size: 18px; color: #fbbf24; display:flex; align-items:center; gap:5px;">
                                            <i class="fa-solid fa-fire"></i> 22 / 25 Disponibles
                                        </div>
                                    </div>
                                </div>
                            
                                <div style="text-align: center; max-width: 500px; margin: 10px auto;">
                                    <div style="font-size: 14px; font-weight: bold; color: var(--bg-color); background: #fbbf24; display: inline-block; padding: 4px 12px; border-radius: 20px; margin-bottom: 10px;">LICENCIA FOUNDER (DE POR VIDA)</div>
                                    <div style="font-size: 56px; font-weight: 800; margin-bottom: 5px; color:white;">$9,999 <span style="font-size: 16px; font-weight: normal; color: var(--text-muted);">MXN / año</span></div>
                                    <div style="font-size: 14px; color: var(--text-muted); margin-bottom: 25px;">Sucursales ilimitadas • Soporte VIP 24/7 • Nuevos módulos incluidos</div>
                                    
                                    <div style="display: flex; gap: 10px; justify-content: center; margin-bottom:15px;">
                                        <input type="text" placeholder="Cupón de Descuento" style="padding: 12px 15px; border-radius: 8px; border: 1px solid var(--surface-light); background: rgba(255,255,255,0.05); color: white; width: 200px;">
                                        <button class="btn btn-primary" style="padding: 12px 30px; font-weight: bold; font-size:16px; box-shadow: 0 4px 15px rgba(139,92,246,0.4);"><i class="fa-brands fa-stripe"></i> Pagar con Stripe</button>
                                    </div>
                                    
                                    <div style="display:flex; gap:10px; justify-content:center; margin-top:20px;">
                                        <button class="btn btn-outline" style="font-size: 12px; padding: 6px 12px; border-color:rgba(255,255,255,0.2);"><i class="fa-solid fa-file-invoice"></i> Solicitar Factura</button>
                                        <button class="btn btn-outline" style="font-size: 12px; padding: 6px 12px; border-color:rgba(255,255,255,0.2);"><i class="fa-solid fa-building-columns"></i> Pago por SPEI</button>
                                    </div>
                                </div>
                            </div>"""

if "LICENCIA FOUNDER" in html and "metric-card" not in old_business:
    html = html.replace(old_business, new_business)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# --- FIX DASHBOARD.JS ---
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix DB Error (Remove country and state from merchants select)
js = js.replace('merchants(business_name, country, state, industry)', 'merchants(business_name, industry)')
js = js.replace('const mCountry = (m.country || \'\').toLowerCase();', 'const mCountry = \'\';')
js = js.replace('const mState = (m.state || \'\').toLowerCase();', 'const mState = \'\';')

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Batch UI fixes completed.")
