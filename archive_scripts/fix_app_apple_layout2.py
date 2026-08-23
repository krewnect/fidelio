import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                storeCard: {
                    primaryFields: [
                        { key: "balance", label: "SALDO DISPONIBLE", value: `$${customer.current_balance}` }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Miembro" }
                    ],
                    backFields: [
                        { key: "portal", label: "PORTAL WEB", value: `https://fidelio.com/portal.html?id=${customer.id}` }
                    ]
                },
                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: customer.id
                }"""

replacement = """                storeCard: {
                    headerFields: [
                        { key: "balance", label: "SALDO DISPONIBLE", value: `$${customer.current_balance}` }
                    ],
                    primaryFields: [
                        { key: "status", label: "MEMBRESÍA", value: "Activa" }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || "Miembro" }
                    ],
                    auxiliaryFields: [
                        { key: "phone", label: "TELÉFONO", value: customer.phone || "No registrado" }
                    ],
                    backFields: [
                        { key: "portal", label: "PORTAL WEB", value: `https://fidelio.com/portal.html?id=${customer.id}` },
                        { key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes." }
                    ]
                },
                barcodes: [{
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: "Mostrar para escanear"
                }]"""

text = text.replace(target, replacement)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
