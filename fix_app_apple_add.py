import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix locations (skip them for now or just remove the bad code)
target = """        // Geofencing (si hay sucursales)
        if (branches && branches.length > 0) {
            const locations = branches.map(b => ({
                latitude: b.lat,
                longitude: b.lng,
                relevantText: `¡Hola! Estás cerca de ${b.name}. Pasa a escanear tu tarjeta.`
            }));
            pass.add('locations', locations);
        }"""

replacement = """        // Geofencing (si hay sucursales)
        /* Omitido por compatibilidad v3, se debe meter directo en pass.json si se requiere */"""

text = text.replace(target, replacement)

target2 = """            if (fs.existsSync('./icon-192.png')) pass.add('icon.png', fs.readFileSync('./icon-192.png'));
            if (fs.existsSync('./icon-192.png')) pass.add('logo.png', fs.readFileSync('./icon-192.png'));
            
            // Si el user tiene strip_icon (Base64)
            if (campaign.stamp_icon_url && campaign.stamp_icon_url.startsWith('data:image')) {
                const base64Data = campaign.stamp_icon_url.replace(/^data:image\/\w+;base64,/, "");
                const stripBuffer = Buffer.from(base64Data, 'base64');
                pass.add('strip.png', stripBuffer);
            } else if (campaign.banner_url && campaign.banner_url.startsWith('data:image')) {
                const base64Data = campaign.banner_url.replace(/^data:image\/\w+;base64,/, "");
                const stripBuffer = Buffer.from(base64Data, 'base64');
                pass.add('strip.png', stripBuffer);
            }"""

replacement2 = """            if (fs.existsSync('./icon-192.png')) {
                pass.addBuffer('icon.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('icon@2x.png', fs.readFileSync('./icon-192.png'));
                pass.addBuffer('logo.png', fs.readFileSync('./icon-192.png'));
            }
            
            // Si el user tiene strip_icon (Base64)
            if (campaign.stamp_icon_url && campaign.stamp_icon_url.startsWith('data:image')) {
                const base64Data = campaign.stamp_icon_url.replace(/^data:image\/\w+;base64,/, "");
                const stripBuffer = Buffer.from(base64Data, 'base64');
                pass.addBuffer('strip.png', stripBuffer);
            } else if (campaign.banner_url && campaign.banner_url.startsWith('data:image')) {
                const base64Data = campaign.banner_url.replace(/^data:image\/\w+;base64,/, "");
                const stripBuffer = Buffer.from(base64Data, 'base64');
                pass.addBuffer('strip.png', stripBuffer);
            }"""

text = text.replace(target2, replacement2)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
