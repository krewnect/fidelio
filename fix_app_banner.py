import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

target_client = """                const stripBuffer = await generateStampsStrip(totalStamps, earnedStamps, cPrimary);"""
replacement_client = """                const stripBuffer = await generateStampsStrip(totalStamps, earnedStamps, cPrimary, campaign.banner_url);"""
app_js = app_js.replace(target_client, replacement_client)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
