import re

with open('app.js', 'r') as f:
    content = f.read()

old_backfields = """                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: "Realizar pago", attributedValue: `<a href="https://fideliorewards.com/card.html?c=${customer.id}&camp=${campaignId}&action=payment">Haz clic aquí para pagar</a>` });
                        }"""
                        
new_backfields = """                        if (campaign.rules_config?.show_payment_btn) {
                            arr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: "Realizar pago", attributedValue: `<a href="https://fideliorewards.com/card.html?c=${customer.id}&camp=${campaignId}&action=payment">Haz clic aquí para pagar</a>` });
                        }
                        if (campaign.rules_config?.booking_link) {
                            arr.push({ key: "booking", label: "RESERVAR MESA / CITA", value: "Reserva en línea", attributedValue: `<a href="${campaign.rules_config.booking_link}">Haz clic aquí para reservar</a>` });
                        }"""
                        
content = content.replace(old_backfields, new_backfields)

with open('app.js', 'w') as f:
    f.write(content)
print("Backfields patched successfully")
