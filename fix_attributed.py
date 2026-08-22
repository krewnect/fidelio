import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

target_client = """                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {
                            arr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=appointment` });
                        }
                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=payment` });
                        }"""

replacement_client = """                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: "Abrir mi tarjeta web", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}">Haz clic aquí para abrir</a>` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {
                            arr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: "Agendar ahora", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=appointment">Haz clic aquí para agendar</a>` });
                        }
                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: "Realizar pago", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=payment">Haz clic aquí para pagar</a>` });
                        }"""

app_js = app_js.replace(target_client, replacement_client)

target_demo = """                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {
                            arr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=appointment` });
                        }
                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=payment` });
                        }"""

replacement_demo = """                        const arr = [
                            { key: "portal", label: "MI TARJETA VIRTUAL", value: "Abrir mi tarjeta web", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}">Haz clic aquí para abrir</a>` }
                        ];
                        if (campaign.rules_config?.show_appointment_btn) {
                            arr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: "Agendar ahora", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=appointment">Haz clic aquí para agendar</a>` });
                        }
                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: "Realizar pago", attributedValue: `<a href="https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=payment">Haz clic aquí para pagar</a>` });
                        }"""

app_js = app_js.replace(target_demo, replacement_demo)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
