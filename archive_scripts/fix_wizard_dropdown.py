import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the unified flow dropdown selection logic
old_select_logic = """    const typeSelect = document.getElementById('card-pass-type');
    if(typeSelect) {
        // Map simplified names to the dropdown values
        let mappedValue = 'storeCard';
        if(programType.toLowerCase().includes('sello')) mappedValue = 'stampCard';
        if(programType.toLowerCase().includes('membresía')) mappedValue = 'membershipCard';
        if(programType.toLowerCase().includes('cupón')) mappedValue = 'coupon';"""

new_select_logic = """    const typeSelect = document.getElementById('program-type-select');
    if(typeSelect) {
        // Map simplified names to the dropdown values
        let mappedValue = 'cashback';
        if(programType.toLowerCase().includes('sello')) mappedValue = 'stamps';"""

if old_select_logic in js:
    js = js.replace(old_select_logic, new_select_logic)
    print("Fixed unified flow dropdown logic.")
else:
    print("Could not find old select logic.")

# Also add the "Invitar a un amigo" feature that was missing in the preview
old_render_end = """        } else {
            if (qrView) qrView.style.display = 'flex';
            if (stampsView) stampsView.style.display = 'none';
            if (configStamps) configStamps.style.display = 'none';
        }
    }"""

new_render_end = """        } else {
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
    }"""

if old_render_end in js:
    js = js.replace(old_render_end, new_render_end)
    print("Added Invitar a un Amigo to preview.")
else:
    print("Could not find render end.")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
