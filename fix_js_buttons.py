import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace all old button classes with fidelio-btn-primary
js = re.sub(r'class="btn btn-primary"[^>]*>', r'class="fidelio-btn-primary" style="width:100%;">', js)
# Wait, some had specific onclicks, I can't just replace the whole tag.
# I will just replace 'btn btn-primary' with 'fidelio-btn-primary' and strip the inline styles.

js = js.replace('class="btn btn-primary"', 'class="fidelio-btn-primary"')
js = js.replace('class=\'btn btn-primary\'', 'class=\'fidelio-btn-primary\'')

# Remove inline backgrounds from buttons in JS
js = re.sub(r'style="[^"]*background:\s*linear-gradient[^"]*"', '', js)
js = re.sub(r'style="[^"]*background:\s*var\(--success\)[^"]*"', '', js)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
