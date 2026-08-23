import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add inline onclick to all nav-tabs with data-tab
def replacer(match):
    full_match = match.group(0)
    data_tab = match.group(1)
    
    # If it already has onclick, don't modify it
    if 'onclick=' in full_match:
        return full_match
        
    onclick_code = f" onclick=\"document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active')); this.classList.add('active'); document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active')); let target = document.getElementById('{data_tab}'); if(target) target.classList.add('active');\""
    
    # Insert onclick before data-tab
    return full_match.replace(f'data-tab="{data_tab}"', f'data-tab="{data_tab}" {onclick_code}')

html = re.sub(r'<div class="nav-tab[^>]*data-tab="([^"]+)"[^>]*>', replacer, html)

# Force everything to be visible for them so they can test it!
# Remove plan-business-only and style="display:none;" from the sidebar
html = html.replace('plan-business-only', '')
html = html.replace('plan-professional-only', '')
html = html.replace('plan-pro-only', '')
html = re.sub(r'style="display:\s*none;?"', '', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
