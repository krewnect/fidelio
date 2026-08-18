import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                storeCard: {
                    primaryFields: [
                        { key: "stamps", label: "SELLOS", value: `${customer.stamps_count} / ${merchant.stamps_required}` }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || 'Invitado' }
                    ],
                    backFields: [
                        { key: "promo", label: pushTitle || "Promociones", value: pushBody || "¡Visítanos pronto y acumula más sellos!", changeMessage: "%@" }
                    ]
                }
            }))
        });
        
        pass.setCertificates({
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase
        });"""

replacement = """                storeCard: {
                    headerFields: [
                        { key: "stamps", label: "SELLOS", value: `${customer.stamps_count} / ${merchant.stamps_required}` }
                    ],
                    primaryFields: [
                        { key: "reward", label: "RECOMPENSA", value: "Activa" }
                    ],
                    secondaryFields: [
                        { key: "name", label: "CLIENTE", value: customer.name || 'Invitado' }
                    ],
                    auxiliaryFields: [
                        { key: "member", label: "NIVEL", value: "VIP" }
                    ],
                    backFields: [
                        { key: "promo", label: pushTitle || "Promociones", value: pushBody || "¡Visítanos pronto y acumula más sellos!", changeMessage: "%@" }
                    ]
                },
                barcodes: [{
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: "Mostrar para escanear"
                }]
            }))
        }, certs);"""

text = text.replace(target, replacement)

# We also need to define `certs` since it uses `pass.setCertificates` which means `certs` might not be defined above.
target2 = """        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,"""

replacement2 = """        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };
        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({
                formatVersion: 1,"""

text = text.replace(target2, replacement2)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
