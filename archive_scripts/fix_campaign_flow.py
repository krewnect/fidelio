import re

with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix 1: Make openCampaignModal clear the currentCampaignId so it creates a NEW one
old_open_modal = """window.openCampaignModal = function() {
    // Start the unified flow
    window.showToast("Paso 1: Elige el Programa de Fidelización para tu campaña.", "success");"""
new_open_modal = """window.openCampaignModal = function() {
    // Force a new campaign context
    if(window.state) window.state.currentCampaignId = null;
    window.showToast("Paso 1: Elige el Programa de Fidelización para tu campaña.", "success");"""

if old_open_modal in js:
    js = js.replace(old_open_modal, new_open_modal)
    print("Patched openCampaignModal")

# Fix 2: Fix btn-save-loyalty so it ALWAYS transitions to the builder, even if currentCampaignId was null
old_save_logic = """                    // Si veníamos de 'Nueva Campaña', avanzar al Diseñador Card
                    if (state.currentCampaignId) {
                        if (typeof window.saveDesignToSupabase === 'function') {
                            await window.saveDesignToSupabase();
                        }
                        setTimeout(() => {
                            if (typeof window.goToBuilder === 'function') {
                                window.goToBuilder();
                            } else {
                                const bTab = document.querySelector('.nav-tab[data-tab="tab-builder"]');
                                if (bTab) bTab.click();
                            }
                            window.showToast('Reglas guardadas. Ahora diseña tu tarjeta.', 'info');
                        }, 500);
                    }"""

new_save_logic = """                    // Avanzar siempre al Diseñador Card (ya sea campaña existente o nueva)
                    if (typeof window.saveDesignToSupabase === 'function') {
                        await window.saveDesignToSupabase(); // Esto auto-generará el currentCampaignId si es null
                    }
                    setTimeout(() => {
                        // Navegar forzosamente al tab-builder
                        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                        const builderTab = document.getElementById('tab-builder');
                        if (builderTab) builderTab.classList.add('active');
                        window.showToast('Reglas guardadas. Paso 2: Diseña tu tarjeta.', 'info');
                        
                        // Actualizar la lista en el builder si es necesario
                        if (typeof window.populateBuilderCampaignSelect === 'function') {
                            window.populateBuilderCampaignSelect();
                        }
                    }, 500);"""

if old_save_logic in js:
    js = js.replace(old_save_logic, new_save_logic)
    print("Patched btn-save-loyalty")

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)

