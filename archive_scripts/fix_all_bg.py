import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace demo route background
app_js = re.sub(
    r'backgroundColor:\s*merchant\.color_primary\s*\|\|\s*"#090d16",\s*foregroundColor:\s*"#ffffff",\s*labelColor:\s*merchant\.color_accent\s*\|\|\s*"#8b5cf6",',
    r'backgroundColor: "rgb(255, 255, 255)",\n                foregroundColor: "rgb(17, 24, 39)",\n                labelColor: "rgb(107, 114, 128)",',
    app_js
)

# Replace any other dark backgrounds in pass.json
app_js = re.sub(
    r'backgroundColor:\s*"rgb\(17, 24, 39\)",\s*foregroundColor:\s*"#ffffff",\s*labelColor:\s*campaign\.color_accent\s*\|\|\s*"#8b5cf6",',
    r'backgroundColor: "rgb(255, 255, 255)",\n                foregroundColor: "rgb(17, 24, 39)",\n                labelColor: "rgb(107, 114, 128)",',
    app_js
)

# Inject puppeteer logic into the demo route as well!
# The demo route currently just does:
# // Intentar agregar iconos o logos customizados
# Let's inject it into the demo route
target_add = """        // Generar strip.png usando Puppeteer si es tipo stamps
        if (campaign.type === 'stamps') {"""
        
# wait, if I used regex, let's just make sure both have the strip logic.
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
