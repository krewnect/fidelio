import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        const pass = new PKPass({
            "pass.json": {
                formatVersion: 1,"""

replacement = """        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };
        const pass = new PKPass({
            "pass.json": {
                formatVersion: 1,"""

text = text.replace(target, replacement)

# Now, we need to pass `certs` to PKPass constructor!
target2 = """            }
        });

        // Geofencing"""

replacement2 = """            }
        }, certs);

        // Geofencing"""

text = text.replace(target2, replacement2)

target3 = """        // Cargar Certificados
        pass.certificates({
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        });"""

replacement3 = """        // Certificados ya cargados en constructor"""

text = text.replace(target3, replacement3)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
