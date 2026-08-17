import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the button to call renderScheduleDays directly
html = html.replace(
    '''<button class="btn btn-primary" onclick="document.getElementById('schedule-config-modal').style.display='flex';" style="background: var(--accent-violet) !important; color: #fff !important; border:none;"><i class="fa-solid fa-clock"></i> Configurar Horarios</button>''',
    '''<button class="btn btn-primary" onclick="document.getElementById('schedule-config-modal').style.display='flex'; if(window.renderScheduleDays) window.renderScheduleDays();" style="background: var(--accent-violet) !important; color: #fff !important; border:none;"><i class="fa-solid fa-clock"></i> Configurar Horarios</button>'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Button click updated.")
