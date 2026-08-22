with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re

def get_div_delta(line):
    opens = len(re.findall(r'<div\b', line))
    closes = len(re.findall(r'</div>', line))
    return opens - closes

depth = 0
for i, line in enumerate(lines):
    delta = get_div_delta(line)
    depth += delta
    if depth == 1 and delta > 0:
        print(f"Depth became 1 at line {i+1}: {line.strip()}")
    if depth < 0:
        print(f"Depth became negative at line {i+1}: {line.strip()}")

print(f"Final Depth: {depth}")
