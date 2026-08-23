import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# For Client Pass
target_client = """                    primaryFields: [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || (campaign.type === 'stamps' ? "Recompensa" : "Saldo VIP") }
                    ],"""

replacement_client = """                    primaryFields: campaign.type === 'stamps' ? [] : [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || "Saldo VIP" }
                    ],"""

app_js = app_js.replace(target_client, replacement_client)

# For Demo Pass
target_demo = """                    primaryFields: [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || "Recompensa VIP" }
                    ],"""

replacement_demo = """                    primaryFields: campaign.type === 'stamps' ? [] : [
                        { key: "reward", label: "BENEFICIO", value: campaign.custom_cta_label || "Recompensa VIP" }
                    ],"""

app_js = app_js.replace(target_demo, replacement_demo)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
