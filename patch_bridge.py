import re
with open('magic_bridge.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add deepTech features to the issueCard payload
old_secret = """            secretPayload: {
                userId: userId,
                balance: config.balance || 0,
                gamification_mode: config.mode || 'STAMPS' // LOOT_BOX, STREAK, MULTIPASS
            }"""

new_secret = """            secretPayload: {
                userId: userId,
                balance: config.balance || 0,
                gamification_mode: config.mode || 'STAMPS', // LOOT_BOX, STREAK, MULTIPASS
                deepTech: {
                    immortalPass: config.deepTech?.immortalPass || false,
                    sonicCheckIn: config.deepTech?.sonicCheckIn || false,
                    infiniteGeo: config.deepTech?.infiniteGeo || false
                }
            }"""

if "immortalPass" not in js:
    js = js.replace(old_secret, new_secret)
    with open('magic_bridge.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched magic_bridge.js")
else:
    print("Already patched.")

# Also let's patch dashboard_v3.js to read the UI and send it in saveDesignToSupabase!
with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    dash_js = f.read()

old_rules = """        rules_config: {
            cashback_percent: state.cashbackPercent,
            stamps_total: state.stampsTotal,"""

new_rules = """        rules_config: {
            deep_tech: {
                immortalPass: document.getElementById('deep-tech-immortal')?.checked || false,
                sonicCheckIn: document.getElementById('deep-tech-sonic')?.checked || false,
                infiniteGeo: document.getElementById('deep-tech-geo')?.checked || false
            },
            cashback_percent: state.cashbackPercent,
            stamps_total: state.stampsTotal,"""

if "immortalPass:" not in dash_js:
    dash_js = dash_js.replace(old_rules, new_rules)
    with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
        f.write(dash_js)
    print("Patched dashboard_v3.js")
else:
    print("Already patched dashboard_v3.js")

