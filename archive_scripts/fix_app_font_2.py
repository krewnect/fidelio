import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

target_client = """                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" },
                        { key: "status", label: "ESTADO", value: "Activo" }
                    ],
                    auxiliaryFields: [
                        { key: "type", label: "PROGRAMA", value: campaign.type === 'stamps' ? 'Tarjetas de Sellos' : 'Cashback VIP' }
                    ],"""

replacement_client = """                    secondaryFields: [
                        { key: "name", label: "SU TARJETA VIRTUAL", value: customer.name || "Invitado" },
                        { key: "type", label: "TIPO", value: campaign.type === 'stamps' ? 'Sellos' : 'Cashback' }
                    ],
                    auxiliaryFields: [],"""

app_js = app_js.replace(target_client, replacement_client)

target_demo = """                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" }
                    ],"""

replacement_demo = """                    secondaryFields: [
                        { key: "name", label: "SU TARJETA VIRTUAL", value: customer.name || "Invitado" },
                        { key: "type", label: "TIPO", value: campaign.type === 'stamps' ? 'Sellos' : 'Cashback' }
                    ],"""

app_js = app_js.replace(target_demo, replacement_demo)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
