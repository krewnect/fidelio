with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_flow = """            // 3. Show Builder directly
            const bld = document.getElementById('tab-builder');
            if (bld) {
                bld.classList.add('active');
                bld.style.display = 'block';
            } else {
                alert("DOM ERROR: tab-builder is missing!");
            }
            
            const bldNav = document.getElementById('nav-builder');
            if (bldNav) bldNav.classList.add('active');
            
            // 4. Toast
            if (typeof window.showToast === 'function') {
                window.showToast("Cargando Fidelio Card Studio...", "success");
            }"""

new_flow = """            // 3. Show FullScreen Studio Iframe
            const restId = window.merchantData ? window.merchantData.id : '123';
            const studioIframe = document.getElementById('wallet-studio-iframe');
            if(studioIframe) {
                studioIframe.src = `/studio/index.html?rest_id=${restId}`;
                document.getElementById('wallet-studio-container').style.display = 'block';
            }
            
            // 4. Toast
            if (typeof window.showToast === 'function') {
                window.showToast("Cargando Fidelio Card Studio (Micro-Frontend)...", "success");
            }"""

html = html.replace(old_flow, new_flow)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Patched forceNewCampaignFlow.")
