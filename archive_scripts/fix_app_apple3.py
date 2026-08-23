import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        const pass = new PKPass({
            "pass.json": {
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,"""

replacement = """        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };
        const pass = new PKPass({
            "pass.json": {
                formatVersion: 1,
                passTypeIdentifier: passTypeIdentifier,"""

text = text.replace(target, replacement)

target2 = """            }
        });

        // Load Certificates
        pass.certificates({
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        });"""

replacement2 = """            }
        }, certs);

        // Certificados cargados en constructor"""

text = text.replace(target2, replacement2)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
