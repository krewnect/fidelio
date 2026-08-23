with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_flow = """            // 3. Show loyalty tab
            const loy = document.getElementById('tab-loyalty');
            if (loy) {
                loy.classList.add('active');
                loy.style.display = 'block';
            } else {
                alert("DOM ERROR: tab-loyalty is missing!");
            }
            
            // 4. Toast
            if (typeof window.showToast === 'function') {
                window.showToast("Paso 1: Elige el Programa de Fidelización.", "success");
            }"""

new_flow = """            // 3. Show Builder directly
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

html = html.replace(old_flow, new_flow)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Bypassed tab-loyalty in forceNewCampaignFlow.")
