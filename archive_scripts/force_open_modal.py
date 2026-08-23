import re

with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_func = """window.openCampaignModal = function() {
    // Force a new campaign context
    if(window.state) window.state.currentCampaignId = null;
    window.showToast("Paso 1: Elige el Programa de Fidelización para tu campaña.", "success");
    
    // Switch to loyalty tab
    const navTabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    navTabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    
    document.getElementById('tab-loyalty').classList.add('active');
    const loyTab = document.getElementById('nav-loyalty');
    if(loyTab) loyTab.classList.add('active');
    
    // Highlight the programs grid
    const programsGrid = document.querySelector('#tab-loyalty .content-panel');
    if(programsGrid) {
        programsGrid.style.border = "2px solid var(--primary)";
        programsGrid.style.boxShadow = "0 0 20px rgba(139,92,246,0.3)";
        setTimeout(() => {
            programsGrid.style.border = "none";
            programsGrid.style.boxShadow = "0 10px 30px rgba(0,0,0,0.05)";
        }, 3000);
    }
}"""

new_func = """window.openCampaignModal = function() {
    try {
        console.log("EXECUTING openCampaignModal()");
        if(typeof window !== 'undefined' && window.state) window.state.currentCampaignId = null;
        
        document.querySelectorAll('.tab-content').forEach(t => {
            t.classList.remove('active');
            t.style.display = 'none';
        });
        
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        
        const loy = document.getElementById('tab-loyalty');
        if(loy) {
            loy.classList.add('active');
            loy.style.display = 'block'; // Force visibility
            console.log("Set tab-loyalty to active and block");
        } else {
            alert("ERROR: tab-loyalty NO EXISTE EN EL DOM");
        }
        
        if (typeof window.showToast === 'function') {
            window.showToast("Paso 1: Elige el Programa de Fidelización para tu campaña.", "success");
        }
    } catch(err) {
        alert("CRITICAL ERROR IN openCampaignModal: " + err.message);
    }
}"""

if old_func in js:
    js = js.replace(old_func, new_func)
    print("Patched successfully")
else:
    print("Could not find old_func")

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)

