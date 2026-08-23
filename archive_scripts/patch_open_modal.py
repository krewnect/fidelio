with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_modal = """        const loy = document.getElementById('tab-loyalty');
        if(loy) {
            loy.classList.add('active');
            loy.style.display = 'block'; // Force visibility
            console.log("Set tab-loyalty to active and block");
        } else {
            alert("ERROR: tab-loyalty NO EXISTE EN EL DOM");
        }
        
        if (typeof window.showToast === 'function') {
            window.showToast("Paso 1: Elige el Programa de Fidelización para tu campaña.", "success");
        }"""

new_modal = """        const bld = document.getElementById('tab-builder');
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

js = js.replace(old_modal, new_modal)

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Patched openCampaignModal.")
