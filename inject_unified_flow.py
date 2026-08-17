import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

unified_flow = """
// ==========================================
// UNIFIED WORKFLOW: CAMPAIGNS -> LOYALTY -> DESIGNER
// ==========================================

window.openCampaignModal = function() {
    // Start the unified flow
    showToast("Paso 1: Elige el Programa de Fidelización para tu campaña.", "success");
    
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
            programsGrid.style.boxShadow = "var(--shadow-sm)";
        }, 3000);
    }
}

window.startDesignerFlow = function(programType) {
    // They selected a program in tab-loyalty. Move to Step 2.
    showToast(`Paso 2: Diseñando tarjeta para ${programType}. Personaliza los colores.`, "success");
    
    // Switch to designer tab
    const navTabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    navTabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    
    document.getElementById('tab-builder').classList.add('active');
    const bldTab = document.getElementById('nav-builder');
    if(bldTab) bldTab.classList.add('active');
    
    // Auto-select the program type in the designer dropdown
    const typeSelect = document.getElementById('card-pass-type');
    if(typeSelect) {
        // Map simplified names to the dropdown values
        let mappedValue = 'storeCard';
        if(programType.toLowerCase().includes('sello')) mappedValue = 'stampCard';
        if(programType.toLowerCase().includes('membresía')) mappedValue = 'membershipCard';
        if(programType.toLowerCase().includes('cupón')) mappedValue = 'coupon';
        
        typeSelect.value = mappedValue;
        // Trigger change to update preview
        typeSelect.dispatchEvent(new Event('change'));
    }
}
"""

if "window.openCampaignModal" not in js:
    # Inject it near the end, before the last closing tags or just at the end.
    js = js + "\n" + unified_flow
    with open('dashboard.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Unified flow JS injected.")
else:
    print("Unified flow already exists.")
