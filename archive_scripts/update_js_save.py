import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            vip_tiers: state.vipTiers,
            show_appointment_btn: document.getElementById('builder-btn-appointment')?.value === 'yes',
            show_payment_btn: document.getElementById('builder-btn-payment')?.value === 'yes'
        }"""

replacement = """            vip_tiers: state.vipTiers,
            show_appointment_btn: document.getElementById('builder-btn-appointment')?.value === 'yes',
            show_payment_btn: document.getElementById('builder-btn-payment')?.value === 'yes',
            valid_until: document.getElementById('camp-valid-until')?.value || null,
            grace_period_days: parseInt(document.getElementById('camp-grace-period')?.value) || null
        }"""

if target in js:
    js = js.replace(target, replacement)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Injected into payload")
else:
    print("Target not found")
