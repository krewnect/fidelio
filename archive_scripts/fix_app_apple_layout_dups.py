import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };
        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };"""

replacement = """        const certs = {
            wwdr: Buffer.from(wwdr, 'base64'),
            signerCert: Buffer.from(signerCert, 'base64'),
            signerKey: Buffer.from(signerKey, 'base64'),
            signerKeyPassphrase: signerKeyPassphrase || undefined
        };"""

text = text.replace(target, replacement)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
