import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace createNewCampaign logic to bypass the hardcoded modal and go straight to the Magical Designer
target_create = r'window\.createNewCampaign = function\(\) \{[\s\S]*?\}'
new_create = """window.createNewCampaign = function() {
    // Go directly to the magical designer so they can use Gemini AI
    document.querySelector('.nav-tab[data-tab=\"tab-builder\"]').click();
}"""

js = re.sub(target_create, new_create, js)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the Nueva Campaña button pulse so they know to click it
html = html.replace('<button class="btn btn-primary" onclick="createNewCampaign()"><i class="fa-solid fa-plus"></i> Nueva Campaña</button>', '<button class="btn btn-primary hover-glow" style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); border:none; box-shadow: 0 4px 15px rgba(139,92,246,0.4);" onclick="createNewCampaign()"><i class="fa-solid fa-wand-magic-sparkles"></i> Diseñar Nueva Campaña Mágica</button>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
