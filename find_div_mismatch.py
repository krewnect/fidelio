with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re

def get_div_delta(line):
    opens = len(re.findall(r'<div\b', line))
    closes = len(re.findall(r'</div>', line))
    return opens - closes

depth = 0
section_depth = 0
current_section = "None"
for i, line in enumerate(lines):
    if '<section' in line:
        current_section = line.strip()
    depth += get_div_delta(line)
    if '</section>' in line:
        if depth != 0:
            print(f"Warning: At end of section '{current_section}', div depth is {depth} (Line {i+1})")
        
print(f"Final Depth: {depth}")
