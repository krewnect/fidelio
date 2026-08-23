import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix invalid regex literal newline
js = js.replace('/```json\\n?/g', "/```json\\\\n?/g")
js = js.replace('/```\\n?/g', "/```\\\\n?/g")

# Actually, the file literally has a raw newline in the regex! Let's do a more robust fix
js = re.sub(r'text\.replace\(/```json\n\?/g, \x27\x27\)\.replace\(/```\n\?/g, \x27\x27\)', r"text.replace(/```json\\\\n?/g, '').replace(/```\\\\n?/g, '')", js)

# Fallback robust replacement if the exact string matching fails
js = re.sub(r'text = text\.replace\(/```json[\s\S]*?\?/g, \'\', js)', r"text = text.replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim();", js)
js = js.replace("text = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();", "text = text.replace(/```json\\\\n?/g, '').replace(/```\\\\n?/g, '').trim();")


with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
