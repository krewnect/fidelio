import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        const pass = new PKPass({
            "pass.json": {"""

replacement = """        const certificates = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };
        const pass = new PKPass({
            "pass.json": {"""

text = text.replace(target, replacement)

target2 = """            pass.add('locations', locations);
        }

        // Cargar Certificados
        pass.certificates({
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        });"""

replacement2 = """            pass.add('locations', locations);
        }"""

text = text.replace(target2, replacement2)

target3 = """        const pass = new PKPass({
            "pass.json": {"""

replacement3 = """        const pass = new PKPass({
            "pass.json": {"""

# Wait, the constructor in v3 takes models and certificates.
# It is better to use `PKPass.from` or just `pass = new PKPass(models, certificates)`
# Actually, the simplest fix is to catch `pass.certificates is not a function` or update the constructor.
