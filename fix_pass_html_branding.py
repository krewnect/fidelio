import re

with open('pass.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the plain action overlay with a branded one
old_overlay = """    <!-- FULL SCREEN ACTION OVERLAY -->
    <div id="action-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; padding:24px; overflow-y:auto; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="max-width:400px; margin:0 auto; padding-top:40px;">
            <button onclick="window.history.back()" style="background:none; border:none; font-size:24px; margin-bottom:20px; cursor:pointer;"><i class="fa-solid fa-arrow-left"></i></button>
            <h1 id="action-title" style="font-size:24px; font-weight:800; margin-bottom:8px; color:#111827;">Agendar Cita</h1>
            <p id="action-subtitle" style="font-size:14px; color:#6b7280; margin-bottom:24px;">Selecciona la fecha y hora para tu cita.</p>
            
            <div id="action-content">
                <!-- content injected by JS -->
            </div>
        </div>
    </div>"""

new_overlay = """    <!-- FULL SCREEN ACTION OVERLAY -->
    <div id="action-overlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:#f9fafb; z-index:9999; overflow-y:auto; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        
        <!-- Branded Header -->
        <div id="action-header" style="background:var(--primary, #111827); color:white; padding: 24px 20px; padding-top: 48px; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px; text-align:center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="position:relative;">
                <button onclick="window.history.back()" style="position:absolute; left:0; top:0; background:rgba(255,255,255,0.2); border:none; border-radius:50%; width:36px; height:36px; color:white; font-size:16px; cursor:pointer; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-arrow-left"></i></button>
                <img id="action-merchant-logo" src="" alt="Logo" style="width:64px; height:64px; border-radius:50%; border:3px solid white; object-fit:cover; margin:0 auto 12px auto; display:none; background:white;">
            </div>
            <h2 id="action-merchant-name" style="font-size:18px; font-weight:700; margin:0; opacity:0.9;">Mi Negocio</h2>
        </div>

        <div style="max-width:400px; margin:0 auto; padding: 32px 24px;">
            <h1 id="action-title" style="font-size:26px; font-weight:800; margin-bottom:8px; color:#111827;">Agendar Cita</h1>
            <p id="action-subtitle" style="font-size:15px; color:#4b5563; margin-bottom:32px;">Selecciona la fecha y hora para tu cita.</p>
            
            <div id="action-content" style="background:white; border-radius:16px; padding:24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #f3f4f6;">
                <!-- content injected by JS -->
            </div>
        </div>
    </div>"""

html = html.replace(old_overlay, new_overlay)

# Make the submit button use the primary color
html = html.replace('background:#111827;', 'background:var(--primary, #111827);')

# Inject logic to populate the action-header when campaign is loaded
target_js = """                if (campaign.color_primary) {
                    document.documentElement.style.setProperty('--primary', campaign.color_primary);
                }"""

replacement_js = """                if (campaign.color_primary) {
                    document.documentElement.style.setProperty('--primary', campaign.color_primary);
                }
                
                // Populate Action Overlay Branding
                if (merchant && merchant.business_name) {
                    document.getElementById('action-merchant-name').textContent = merchant.business_name;
                }
                const overlayLogo = document.getElementById('action-merchant-logo');
                if (campaign.logo_url) {
                    overlayLogo.src = campaign.logo_url;
                    overlayLogo.style.display = 'block';
                } else if (merchant) {
                    overlayLogo.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(merchant.business_name)}&background=fff&color=000`;
                    overlayLogo.style.display = 'block';
                }"""

if "// Populate Action Overlay Branding" not in html:
    html = html.replace(target_js, replacement_js)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(html)
