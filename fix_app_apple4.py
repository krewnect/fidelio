import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target2 = """            pass.add('locations', locations);
        }

        // Cargar Certificados (decodificados de base64)
        pass.certificates({
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        });"""

replacement2 = """            pass.add('locations', locations);
        }"""

text = text.replace(target2, replacement2)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
