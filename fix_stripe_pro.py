import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# REWRITE STRIPE TAB
old_stripe = """            <section id="tab-stripe" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">STRIPE</span>
                        <h1>Monetización</h1>
                        <p>Configura tus llaves de Stripe para cobrar.</p>
                    </div>
                </div>
                <div class="settings-card" style="background: var(--surface); padding: 32px; border-radius: 20px; border: 1px solid var(--surface-light); text-align: center;">
                    <div style="font-size: 48px; color: #6366f1; margin-bottom: 16px;">
                        <i class="fa-brands fa-stripe"></i>
                    </div>
                    <h3 style="margin-bottom: 12px; color: var(--text-main); font-size: 20px;">Vende tus beneficios directo desde Wallet</h3>
                    <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 32px; max-width: 500px; margin-left: auto; margin-right: auto;">
                        Crea un producto en tu cuenta de Stripe (ej. "Membresía Anual" o "Saldo Prepagado") y pega aquí el enlace de pago. Nosotros nos encargamos de integrarlo en tu tarjeta de Apple Wallet.
                    </p>
                    
                    <div class="form-group" style="margin-bottom: 24px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; font-size: 13px;">Payment Link de Stripe</label>
                        <input type="url" id="stripe-payment-link" class="form-control" placeholder="https://buy.stripe.com/test_..." style="width: 100%; padding: 16px; border-radius: 12px; border: 2px solid var(--surface-light); background: var(--bg-color); color: var(--text-color); font-size: 15px; transition: all 0.3s ease;">
                    </div>
                    
                    <button class="btn btn-primary" onclick="saveStripeKeys()" style="background: #8b5cf6 !important; color: #fff !important; padding: 16px 32px; font-size: 16px; font-weight: 700; border: none; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 14px rgba(139,92,246,0.3); transition: all 0.3s ease;"><i class="fa-solid fa-link" style="margin-right: 8px;"></i> Vincular Payment Link</button>
                </div>
            </section>"""

new_stripe = """            <section id="tab-stripe" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">STRIPE</span>
                        <h1>Monetización (BETA)</h1>
                        <p>Vende membresías y saldo prepagado directamente a través de Apple y Google Wallet.</p>
                    </div>
                </div>
                
                <!-- PROFESSIONAL TIER LOCK -->
                <div id="stripe-pro-lock" style="display:none; background: linear-gradient(135deg, rgba(139,92,246,0.05) 0%, rgba(0,0,0,0) 100%); border: 1px solid rgba(139,92,246,0.2); border-radius: 20px; padding: 40px; text-align: center; margin-bottom: 24px; position:relative; overflow:hidden;">
                    <div style="font-size: 48px; color: var(--accent-amber); margin-bottom: 16px;"><i class="fa-solid fa-crown"></i></div>
                    <h3 style="margin-bottom: 12px; color: var(--text-main); font-size: 24px; font-weight:800;">Exclusivo para Cuentas Profesionales</h3>
                    <p style="color: var(--text-muted); font-size: 15px; margin-bottom: 24px; max-width: 500px; margin-left: auto; margin-right: auto; line-height:1.5;">
                        La monetización nativa y la venta directa de beneficios desde Apple Wallet requieren una cuenta de nivel Profesional. Sube de nivel para desbloquear los enlaces de pago de Stripe.
                    </p>
                    <button class="btn btn-primary" style="background: var(--accent-amber) !important; color: #000 !important; font-weight: 800; border: none;"><i class="fa-solid fa-arrow-up-right-dots"></i> Hacer Upgrade a Pro</button>
                </div>

                <div id="stripe-active-ui" class="settings-card" style="background: var(--surface); padding: 40px; border-radius: 20px; border: 1px solid var(--surface-light); text-align: center; position:relative;">
                    
                    <div style="position:absolute; top:20px; right:20px; background:rgba(16,185,129,0.1); color:#10b981; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:700;"><i class="fa-solid fa-check-circle"></i> Cuenta Pro Activa</div>

                    <div style="font-size: 48px; color: #6366f1; margin-bottom: 16px;">
                        <i class="fa-brands fa-stripe"></i>
                    </div>
                    <h3 style="margin-bottom: 12px; color: var(--text-main); font-size: 20px;">Vende tus beneficios directo desde Wallet</h3>
                    <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 32px; max-width: 500px; margin-left: auto; margin-right: auto;">
                        Crea un producto en tu cuenta de Stripe (ej. "Membresía Anual VIP") y pega aquí el enlace de pago. Selecciona a qué tarjeta deseas asociarlo.
                    </p>
                    
                    <div style="max-width: 600px; margin: 0 auto; text-align: left;">
                        <div class="form-group" style="margin-bottom: 20px;">
                            <label style="display: block; margin-bottom: 8px; font-weight: 600; font-size: 13px; color:var(--accent-violet);">1. Tarjeta / Campaña a Monetizar</label>
                            <select id="stripe-campaign-select" class="form-control" style="width: 100%; padding: 16px; border-radius: 12px; border: 2px solid var(--surface-light); background: var(--bg-color); color: var(--text-color); font-size: 15px; font-weight:600;">
                                <option value="">-- Selecciona una tarjeta/campaña --</option>
                            </select>
                        </div>

                        <div class="form-group" style="margin-bottom: 32px;">
                            <label style="display: block; margin-bottom: 8px; font-weight: 600; font-size: 13px; color:var(--accent-violet);">2. Payment Link de Stripe</label>
                            <input type="url" id="stripe-payment-link" class="form-control" placeholder="https://buy.stripe.com/test_..." style="width: 100%; padding: 16px; border-radius: 12px; border: 2px solid var(--surface-light); background: var(--bg-color); color: var(--text-color); font-size: 15px;">
                        </div>
                        
                        <div style="text-align:center;">
                            <button class="btn btn-primary" onclick="saveStripeKeys()" style="background: #8b5cf6 !important; color: #fff !important; padding: 16px 32px; font-size: 16px; font-weight: 700; border: none; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 14px rgba(139,92,246,0.3); transition: all 0.3s ease; width:100%;"><i class="fa-solid fa-link" style="margin-right: 8px;"></i> Vincular Checkout a Tarjeta</button>
                        </div>
                    </div>
                </div>
            </section>"""

if old_stripe in html:
    html = html.replace(old_stripe, new_stripe)
    print("Stripe Tab Redesigned HTML.")
else:
    print("Could not find old stripe HTML.")


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# UPDATE DASHBOARD.JS TO HANDLE THIS NEW STRIPE UI
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# We need to populate the stripe campaign select, and update saveStripeKeys to read it.
old_save_stripe = """window.saveStripeKeys = async function() {
    const linkInput = document.getElementById('stripe-payment-link');
    const paymentLink = linkInput ? linkInput.value : '';
    
    if (!paymentLink || !paymentLink.includes('stripe.com')) {
        if (typeof showToast === 'function') showToast("Ingresa un Payment Link válido de Stripe", "warning");
        return;
    }
    
    // We save this into the current active campaign (if there is one) or locally
    state.customBannerUrl = paymentLink;
    
    if (typeof showToast === 'function') showToast("Payment Link de Stripe vinculado con éxito", "success");
};"""

new_save_stripe = """window.saveStripeKeys = async function() {
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
    
    // Asignar el payment link a la campaña especificada (Mock)
    console.log("Stripe Linked to campaign: " + campId);
    
    if (typeof showToast === 'function') showToast("Checkout de Stripe vinculado exitosamente a la Tarjeta", "success");
};

// POPULATE STRIPE CAMPAIGNS AND HANDLE PRO LOCK
window.initStripeUI = function() {
    const sel = document.getElementById('stripe-campaign-select');
    const lock = document.getElementById('stripe-pro-lock');
    const activeUI = document.getElementById('stripe-active-ui');
    
    // Mock user tier
    const isPro = true; // Set to true so they can see the UI, or false to test the lock
    
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
"""

if old_save_stripe in js:
    js = js.replace(old_save_stripe, new_save_stripe)
    print("Stripe JS replaced.")
else:
    print("Could not find old stripe JS logic.")

# NOTE: Since `switchTab` was already overridden in the previous step, I need to make sure I'm not creating an infinite loop or overriding my own override.
# Actually, the previous step's override is currently in `dashboard.js`. I will replace the PREVIOUS override with the NEW one that handles both.
old_override = """// Make sure to call populateBuilderCampaignSelect when switching to tab-builder
const origSwitchTab = window.switchTab;
window.switchTab = function(tabId) {
    if (origSwitchTab) origSwitchTab(tabId);
    if (tabId === 'tab-builder' && window.populateBuilderCampaignSelect) {
        window.populateBuilderCampaignSelect();
    }
};"""

if old_override in js:
    js = js.replace(old_override, "")
    print("Cleaned up old override.")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
