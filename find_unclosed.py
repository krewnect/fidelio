with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

sections = []
for i, line in enumerate(lines):
    if '<section ' in line:
        sections.append({'line': i+1, 'type': 'open', 'text': line.strip()})
    if '</section>' in line:
        sections.append({'line': i+1, 'type': 'close', 'text': line.strip()})

depth = 0
for s in sections:
    if s['type'] == 'open':
        depth += 1
        print(f"OPEN: {s['text']} (Depth: {depth})")
    else:
        depth -= 1
        print(f"CLOSE: {s['text']} (Depth: {depth})")

print(f"Final Depth: {depth}")
