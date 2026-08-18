with open('dashboard.js', 'r') as f:
    lines = f.readlines()
    
start = -1
end = -1
for i, line in enumerate(lines):
    if 'function updatePassRender()' in line:
        start = i
    if start != -1 and 'if (window._updatePassRenderGlobal)' in line:
        end = i
        break

if start != -1 and end != -1:
    print("".join(lines[start:end+1]))
else:
    print(f"Not found: start={start}, end={end}")
