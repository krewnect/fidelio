with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """    // Populate account info
    document.getElementById('acc-email').value = state.user.email || '';
    if (state.merchant) {
        document.getElementById('acc-business-name').value = state.merchant.business_name || '';
        document.getElementById('acc-business-category').value = state.merchant.category || '';
        
        // Portal Settings
        if(state.merchant.portal_color) document.getElementById('portal-color-primary').value = state.merchant.portal_color;
        if(state.merchant.portal_logo) {
            const preview = document.getElementById('portal-logo-preview');
            const img = document.getElementById('portal-logo-img');
            img.src = state.merchant.portal_logo;
            preview.style.display = 'flex';
        }
        
        // Settings json
        const settings = state.merchant.settings || {};
        const reqFields = settings.required_fields || ['name', 'email', 'phone'];
        document.getElementById('req-phone').checked = reqFields.includes('phone');
        document.getElementById('req-birthday').checked = reqFields.includes('birthday');
    }"""

replacement = target + """
    
    // Premium Sidebar Info
    if (state.merchant) {
        const bName = state.merchant.business_name || 'Tu Negocio';
        const sNameEl = document.getElementById('acc-summary-name');
        if (sNameEl) sNameEl.textContent = bName;
        
        const avatarEl = document.getElementById('acc-avatar-letter');
        if (avatarEl) avatarEl.textContent = bName.charAt(0).toUpperCase();
        
        const tierEl = document.getElementById('acc-summary-tier');
        if (tierEl) tierEl.textContent = 'PLAN ' + (state.merchant.tier || 'PROFESSIONAL').toUpperCase();
    }
"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

