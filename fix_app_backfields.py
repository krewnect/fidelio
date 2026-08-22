import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

target1 = """                    backFields: (() => {
                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: "Abrir mi tarjeta web", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}">Haz clic aquí para abrir</a>` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {"""

replacement1 = """                    backFields: (() => {
                        const arr = [];
                        if (campaign.custom_cta_url) {
                            arr.push({ key: "website", label: "SITIO WEB O REDES SOCIALES", value: "Visitar el perfil del negocio", attributedValue: `<a href="${campaign.custom_cta_url}">Haz clic aquí para abrir</a>` });
                        }
                        if (campaign.rules_config?.show_appointment_btn) {"""

app_js = app_js.replace(target1, replacement1)

target2 = """                    backFields: (() => {
                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: "Abrir mi tarjeta web", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}">Haz clic aquí para abrir</a>` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {"""

replacement2 = """                    backFields: (() => {
                        const arr = [];
                        if (campaign.custom_cta_url) {
                            arr.push({ key: "website", label: "SITIO WEB O REDES SOCIALES", value: "Visitar el perfil del negocio", attributedValue: `<a href="${campaign.custom_cta_url}">Haz clic aquí para abrir</a>` });
                        }
                        if (campaign.rules_config?.show_appointment_btn) {"""

app_js = app_js.replace(target2, replacement2)

app_js = re.sub(r'serialNumber: `\$\{customerId\}\|\$\{campaignId\}\|v4_\$\{Date\.now\(\)\}`', r'serialNumber: `${customerId}|${campaignId}|v5_${Date.now()}`', app_js)
app_js = re.sub(r'serialNumber: `\$\{customer\.id\}\|v4_\$\{Date\.now\(\)\}`', r'serialNumber: `${customer.id}|v5_${Date.now()}`', app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
