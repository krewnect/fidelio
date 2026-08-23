import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            const btnPay = document.getElementById('builder-btn-payment');
            if (btnPay) btnPay.value = rules.show_payment_btn ? 'yes' : 'no';
        }"""

replacement = """            const btnPay = document.getElementById('builder-btn-payment');
            if (btnPay) btnPay.value = rules.show_payment_btn ? 'yes' : 'no';
            
            const vUntil = document.getElementById('camp-valid-until');
            if (vUntil && rules.valid_until) vUntil.value = rules.valid_until;
            else if (vUntil) vUntil.value = '';
            
            const gPeriod = document.getElementById('camp-grace-period');
            if (gPeriod && rules.grace_period_days) gPeriod.value = rules.grace_period_days;
            else if (gPeriod) gPeriod.value = '';
        }"""

if target in js:
    js = js.replace(target, replacement)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Injected into loader")
else:
    print("Target not found")
