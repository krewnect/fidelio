import re

with open('app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace client pass
pattern_client = re.compile(r'(const pass = new PKPass\(\{.*?backFields:\s*\[.*?\]\s*\},.*?barcodes:.*?\}\)\)\s*\}, certs\);)', re.DOTALL)

def replacer_client(match):
    original = match.group(1)
    
    # We reconstruct the pass creation logic
    prefix = """const backFieldsArr = [
            { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}` }
        ];
        if (campaign.rules_config?.show_appointment_btn) {
            backFieldsArr.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=appointment` });
        }
        if (campaign.rules_config?.show_payment_btn) {
            backFieldsArr.push({ key: "payment", label: "PAGAR EN LÍNEA", value: `https://fideliorewards.com/pass.html?c=${customerId}&camp=${campaignId}&action=payment` });
        }
        backFieldsArr.push({ key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." });
        backFieldsArr.push({ key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" });\n\n        """
    
    new_code = re.sub(r'backFields:\s*\[.*?\]', 'backFields: backFieldsArr', original, flags=re.DOTALL)
    return prefix + new_code

code = re.sub(r'(const pass = new PKPass\(\{\s*"pass\.json": Buffer\.from\(JSON\.stringify\(\{.*?backFields:\s*\[.*?\]\s*\},.*?barcodes:.*?\}\)\)\s*\}, certs\);)', replacer_client, code, count=1, flags=re.DOTALL)


def replacer_demo(match):
    original = match.group(1)
    prefix = """const backFieldsDemo = [
            { key: "portal", label: "MI TARJETA VIRTUAL", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}` }
        ];
        if (campaign.rules_config?.show_appointment_btn) {
            backFieldsDemo.push({ key: "appointment", label: "AGENDAR CITA O SERVICIO", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=appointment` });
        }
        if (campaign.rules_config?.show_payment_btn) {
            backFieldsDemo.push({ key: "payment", label: "PAGAR EN LÍNEA", value: `https://fideliorewards.com/pass.html?c=${customer.id}&camp=${campaignId}&action=payment` });
        }
        backFieldsDemo.push({ key: "terms", label: "TÉRMINOS Y CONDICIONES", value: "Promoción sujeta a cambios. Válida solo en sucursales participantes. Esta tarjeta es personal e intransferible." });
        backFieldsDemo.push({ key: "contact", label: "CONTACTO", value: "soporte@fideliorewards.com" });\n\n        """
    
    new_code = re.sub(r'backFields:\s*\[.*?\]', 'backFields: backFieldsDemo', original, flags=re.DOTALL)
    # Also fix demo barcode if needed, but not strictly necessary
    return prefix + new_code

# The second occurrence is the Demo pass
# Let's just do it dynamically:
parts = code.split('app.get(\'/api/wallet/apple-demo')
if len(parts) == 2:
    p2 = re.sub(r'(const pass = new PKPass\(\{\s*"pass\.json": Buffer\.from\(JSON\.stringify\(\{.*?backFields:\s*\[.*?\]\s*\}?,.*?(?:barcodes|barcode):.*?\}\)\)\s*\}, certs\);)', replacer_demo, parts[1], count=1, flags=re.DOTALL)
    code = parts[0] + 'app.get(\'/api/wallet/apple-demo' + p2

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)
