import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# We look for the exact JSON string block for the client pass
target_client = """                    backFields: [
                        { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` },
                        { key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." },
                        { key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" }
                    ]"""

replacement_client = """                    backFields: (() => {
                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {
                            arr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=appointment` });
                        }
                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=payment` });
                        }
                        arr.push({ key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." });
                        arr.push({ key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" });
                        return arr;
                    })()"""

app_js = app_js.replace(target_client, replacement_client)

target_demo = """                    backFields: [
                        { key: "portal", label: "PORTAL WEB", value: `https://fidelio.com/portal.html?id=${customer.id}` }
                    ]"""

replacement_demo = """                    backFields: (() => {
                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {
                            arr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=appointment` });
                        }
                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=payment` });
                        }
                        arr.push({ key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." });
                        arr.push({ key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" });
                        return arr;
                    })()"""

app_js = app_js.replace(target_demo, replacement_demo)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
