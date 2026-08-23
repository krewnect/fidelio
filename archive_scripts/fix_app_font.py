import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

target_client = """                logoText: campaign.name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(17, 24, 39)",
                labelColor: "rgb(107, 114, 128)","""

replacement_client = """                logoText: campaign.name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(0, 0, 0)",
                labelColor: "rgb(100, 100, 100)","""

app_js = app_js.replace(target_client, replacement_client)

target_demo = """                logoText: merchant.business_name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(17, 24, 39)",
                labelColor: "rgb(107, 114, 128)","""

replacement_demo = """                logoText: merchant.business_name || "Mi Negocio",
                backgroundColor: "rgb(255, 255, 255)",
                foregroundColor: "rgb(0, 0, 0)",
                labelColor: "rgb(100, 100, 100)","""

app_js = app_js.replace(target_demo, replacement_demo)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
