with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the magic engine section violently obvious
old_header = '<span><i class="fa-solid fa-robot"></i> Autopilot (Deep Tech)</span>'
new_header = '<span style="color: #ef4444; font-size: 24px; font-weight: 900; animation: pulse 2s infinite;"><i class="fa-solid fa-robot"></i> AQUI ESTA EL AUTOPILOT (MAGIC ENGINE)</span>'

if "AQUI ESTA EL" not in html:
    html = html.replace(old_header, new_header)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
