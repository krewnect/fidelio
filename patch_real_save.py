import re

# 1. Inject saveCampaignFromStudio into dashboard_v3.js
with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

inject_func = """
// --- FIDELIO STUDIO BRIDGE ---
window.saveCampaignFromStudio = async function(studioPayload) {
    const payload = {
        id: crypto.randomUUID(),
        type: studioPayload.loyalty.type || "hybrid",
        name: studioPayload.branding.name || "Campaña de Studio",
        description: studioPayload.branding.desc || "Generada desde Fidelio Studio",
        color_primary: studioPayload.branding.colors.primary || "#000000",
        color_accent: studioPayload.branding.colors.accent || "#ffffff",
        custom_cta_label: studioPayload.loyalty.stampsReward || 'Recompensa Exclusiva',
        rules_config: {
            stamps_total: studioPayload.loyalty.stampsTotal || 5
        }
    };
    try {
        const res = await fetch('/api/campaigns', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.merchantSession?.access_token || ''}`
            },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            if (typeof window.loadCampaigns === 'function') {
                await window.loadCampaigns();
            }
            return true;
        } else {
            console.error("Save Error:", await res.text());
            if (typeof window.showToast === 'function') window.showToast("Error al guardar campaña en BD", "error");
            return false;
        }
    } catch(e) {
        console.error(e);
        if (typeof window.showToast === 'function') window.showToast("Error de conexión al guardar", "error");
        return false;
    }
};
// -----------------------------
"""

js = inject_func + js

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Update publishPass in studio/index.html to call it
with open('studio/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_publish = """                        // Simulando guardado en el Engine
                        await new Promise(r => setTimeout(r, 1500));
                        this.isSuccess = true;"""

new_publish = """                        // Guardado real en la base de datos a través de la ventana padre
                        if (window.parent && typeof window.parent.saveCampaignFromStudio === 'function') {
                            const success = await window.parent.saveCampaignFromStudio(payload);
                            if (success) {
                                this.isSuccess = true;
                            } else {
                                alert("No se pudo guardar la campaña. Revisa tu conexión.");
                            }
                        } else {
                            // Fallback
                            await new Promise(r => setTimeout(r, 1500));
                            this.isSuccess = true;
                        }"""

html = html.replace(old_publish, new_publish)

# 3. Fix the "Volver al Dashboard" button in the success overlay so it just closes the iframe instead of reloading
old_success_btn = """<button @click="if(window.parent) { window.parent.document.getElementById('wallet-studio-container').style.display = 'none'; window.parent.document.getElementById('wallet-studio-iframe').src = ''; window.parent.showToast('Campaña creada con éxito.', 'success'); window.parent.location.reload(); }" class="px-8 py-3 rounded-xl bg-[#8b5cf6] hover:bg-[#7c3aed] text-white font-bold shadow-lg transition-transform hover:scale-105 flex items-center">"""
new_success_btn = """<button @click="if(window.parent) { window.parent.document.getElementById('wallet-studio-container').style.display = 'none'; window.parent.document.getElementById('wallet-studio-iframe').src = ''; window.parent.showToast('Campaña lista.', 'success'); }" class="px-8 py-3 rounded-xl bg-[#8b5cf6] hover:bg-[#7c3aed] text-white font-bold shadow-lg transition-transform hover:scale-105 flex items-center">"""

html = html.replace(old_success_btn, new_success_btn)

with open('studio/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Linked Studio to real database.")
