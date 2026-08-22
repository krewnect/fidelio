import re

with open('studio/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the generic alert with one that shows exactly what happened
old_alert = """                            if (success) {
                                this.isSuccess = true;
                            } else {
                                alert("No se pudo guardar la campaña. Revisa tu conexión.");
                            }"""

new_alert = """                            if (success) {
                                this.isSuccess = true;
                            } else {
                                alert("DEBUG: saveCampaignFromStudio devolvió false. El Dashboard rechazó el payload.");
                            }"""
html = html.replace(old_alert, new_alert)

old_catch = """                        if (window.parent && typeof window.parent.saveCampaignFromStudio === 'function') {
                            const success = await window.parent.saveCampaignFromStudio(payload);"""
new_catch = """                        if (window.parent && typeof window.parent.saveCampaignFromStudio === 'function') {
                            let success = false;
                            try {
                                success = await window.parent.saveCampaignFromStudio(payload);
                            } catch(err) {
                                alert("DEBUG: Error al llamar a saveCampaignFromStudio: " + err.message);
                            }"""
html = html.replace(old_catch, new_catch)

with open('studio/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_err = """        } else {
            console.error("Save Error:", await res.text());
            if (typeof window.showToast === 'function') window.showToast("Error al guardar campaña en BD", "error");
            return false;
        }"""
new_err = """        } else {
            const text = await res.text();
            console.error("Save Error:", text);
            alert("DEBUG API ERROR: " + res.status + " - " + text);
            if (typeof window.showToast === 'function') window.showToast("Error al guardar campaña en BD", "error");
            return false;
        }"""
js = js.replace(old_err, new_err)

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Injected detailed debug alerts.")
