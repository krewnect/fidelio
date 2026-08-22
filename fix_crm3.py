import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = "const phoneDigits = c.phone ? c.phone.replace(/\D/g, '') : '';"
replacement = """            // XSS Escaper
            const esc = (s) => s ? String(s).replace(/[&<>'"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[m])) : '';
            c.email = esc(c.email);
            c.phone = esc(c.phone);
            c.full_name = esc(c.full_name);
            c.name = esc(c.name);

            const phoneDigits = c.phone ? c.phone.replace(/\D/g, '') : '';"""

if target in js:
    js = js.replace(target, replacement)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Added XSS sanitization")
else:
    print("Not found")
