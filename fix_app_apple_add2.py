import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        if (branches && branches.length > 0) {
            const locations = branches.map(b => ({
                latitude: b.lat,
                longitude: b.lng,
                relevantText: `¡Bienvenido a ${b.name}! Tienes $${customer.current_balance} para usar hoy.`
            }));
            pass.add('locations', locations);
        }"""

replacement = """        if (branches && branches.length > 0) {
            /* omitted locations for v3 compat */
        }"""

text = text.replace(target, replacement)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
