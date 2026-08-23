import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                storeCard: {
                    primaryFields: [
                        { key: "balance", label: labelVal, value: balanceVal }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" }
                    ],
                    backFields: [
                        { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` },
                        { key: "terms", label: "TÉRMINOS", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes." }
                    ]
                },
                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: `${customerId}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Código Cliente"
                }"""

replacement = """                storeCard: {
                    headerFields: [
                        { key: "balance", label: labelVal, value: balanceVal }
                    ],
                    primaryFields: [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || (campaign.type === 'stamps' ? "Recompensa" : "Saldo VIP") }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Invitado" },
                        { key: "status", label: "ESTADO", value: "Activo" }
                    ],
                    auxiliaryFields: [
                        { key: "type", label: "PROGRAMA", value: campaign.type === 'stamps' ? 'Tarjetas de Sellos' : 'Cashback VIP' }
                    ],
                    backFields: [
                        { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` },
                        { key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." },
                        { key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" }
                    ]
                },
                barcodes: [{
                    format: "PKBarcodeFormatQR",
                    message: `${customerId}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Mostrar para escanear"
                }]"""

text = text.replace(target, replacement)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
