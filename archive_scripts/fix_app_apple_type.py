import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        const pass = new PKPass({
            "pass.json": {"""

replacement = """        const pass = new PKPass({
            "pass.json": Buffer.from(JSON.stringify({"""

text = text.replace(target, replacement)

target2 = """                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: `${customerId}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Código Cliente"
                }
            }
        }, certs);"""

replacement2 = """                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: `${customerId}|${campaignId}`,
                    messageEncoding: "iso-8859-1",
                    altText: "Código Cliente"
                }
            }))
        }, certs);"""

text = text.replace(target2, replacement2)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
