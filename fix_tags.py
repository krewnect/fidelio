import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the sidebar menu
section_start = html.find('<nav class="sidebar-menu">')
section_end = html.find('</nav>', section_start)

if section_start != -1 and section_end != -1:
    sidebar_html = html[section_start:section_end]
    
    # Replace <button class="nav-tab... "> with <div class="nav-tab... ">
    sidebar_html = re.sub(r'<button class="nav-tab', r'<div class="nav-tab', sidebar_html)
    sidebar_html = re.sub(r'</button>', r'</div>', sidebar_html)
    
    html = html[:section_start] + sidebar_html + html[section_end:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Tags replaced.")
else:
    print("WARNING: Sidebar not found.")

