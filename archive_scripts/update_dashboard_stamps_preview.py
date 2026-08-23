import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the inner loop of stamp generation in updatePassRender
old_stamp_loop = """                for (let i = 1; i <= sTotal; i++) {
                    const node = document.createElement('div');
                    if (i <= userStamps) {
                        node.className = 'stamp-coin filled';
                        node.style.backgroundColor = cAcc;
                        node.innerHTML = '<i class="fa-solid fa-check"></i>';
                    } else {
                        node.className = 'stamp-coin empty';
                        node.textContent = i;
                    }
                    stampsGrid.appendChild(node);
                }"""

new_stamp_loop = """                // Use custom icon/image for stamps
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
                }"""

content = content.replace(old_stamp_loop, new_stamp_loop)

# Also update the preview button text for professionals
old_preview_cta = """        // --- BUTTON CTA PREVIEW ---
        const rCtaBtn = document.getElementById('render-cta-btn');
        if (state.activeMode === 'hybrid') {
            if (rCtaBtn) rCtaBtn.innerHTML = '<i class="fa-solid fa-wallet"></i> Añadir a Apple Wallet';
        } else if (state.activeMode === 'stamps') {
            if (rCtaBtn) rCtaBtn.innerHTML = `<i class="fa-solid fa-gift"></i> ${pReward}`;
        }"""

new_preview_cta = """        // --- BUTTON CTA PREVIEW ---
        const rCtaBtn = document.getElementById('render-cta-btn');
        if (state.activeMode === 'hybrid') {
            if (rCtaBtn) rCtaBtn.innerHTML = '<i class="fa-solid fa-wallet"></i> Añadir a Apple Wallet';
        } else if (state.activeMode === 'stamps') {
            if (rCtaBtn) rCtaBtn.innerHTML = `<i class="fa-solid fa-gift"></i> ${pReward}`;
        }
        
        // Professional Override
        const businessType = window.merchantData && window.merchantData.business_type ? window.merchantData.business_type : 'restaurant';
        if (businessType === 'professional') {
            if (rCtaBtn) rCtaBtn.innerHTML = `<i class="fa-solid fa-calendar-check"></i> ${state.stampsReward || 'Agendar Cita o Servicio'}`;
            if (window.merchantData && window.merchantData.stripe_keys && window.merchantData.stripe_keys.stripe_pub_key) {
                rCtaBtn.innerHTML += " (Pagar vía Stripe)";
            }
        }"""

if '// Professional Override' not in content:
    content = content.replace(old_preview_cta, new_preview_cta)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("dashboard.js stamps preview updated.")
