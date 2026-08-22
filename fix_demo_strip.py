import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# We look for the comment in the demo route
target = """        // Certificados ya cargados en constructor

        // Intentar agregar iconos o logos customizados"""

replacement = """        // Certificados ya cargados en constructor

        // Generar strip.png usando Puppeteer/sharp si es tipo stamps
        if (campaign.type === 'stamps') {
            try {
                const totalStamps = campaign.rules_config?.stamps_total || 5;
                const earnedStamps = 3; // Demo siempre muestra 3 sellos ganados
                const cPrimary = campaign.color_primary || '#8b5cf6';
                const stripBuffer = await generateStampsStrip(totalStamps, earnedStamps, cPrimary);
                pass.addBuffer('strip.png', stripBuffer);
                pass.addBuffer('strip@2x.png', stripBuffer);
            } catch (e) {
                console.error("Strip generation failed", e);
            }
        }

        // Intentar agregar iconos o logos customizados"""

# Since this comment might appear multiple times, let's just do a string replace, it's fine if it injects multiple times where that comment is.
app_js = app_js.replace(target, replacement)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
