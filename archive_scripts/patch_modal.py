import re
with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_modal = """        const bld = document.getElementById('tab-builder');
        if(bld) {
            bld.classList.add('active');
            bld.style.display = 'block'; // Force visibility
            console.log("Set tab-builder to active and block");
        } else {
            alert("ERROR: tab-builder NO EXISTE EN EL DOM");
        }
        
        const bldNav = document.getElementById('nav-builder');
        if(bldNav) bldNav.classList.add('active');
        
        if (typeof window.showToast === 'function') {
            window.showToast("Cargando Fidelio Card Studio...", "success");
        }"""

new_modal = """        const restId = window.merchantData ? window.merchantData.id : '123';
        const studioIframe = document.getElementById('wallet-studio-iframe');
        if(studioIframe) {
            studioIframe.src = `/studio/index.html?rest_id=${restId}`;
            document.getElementById('wallet-studio-container').style.display = 'block';
            console.log("Launched FullScreen Studio Iframe");
        } else {
            alert("ERROR: wallet-studio-container NO EXISTE EN EL DOM");
        }
        
        if (typeof window.showToast === 'function') {
            window.showToast("Cargando Fidelio Card Studio (Micro-Frontend)...", "success");
        }"""

js = js.replace(old_modal, new_modal)

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Patched openCampaignModal.")
