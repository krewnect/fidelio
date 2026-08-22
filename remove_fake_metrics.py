import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target_mock = """        // Mock random stats based on name length for realism
        const scans = 1204 + (camp.name ? camp.name.length * 14 : 0);
        const rewards = Math.floor(scans / 10);"""

replacement_real = """        // Real stats (defaults to 0 for new campaigns)
        const scans = camp.total_scans || 0;
        const rewards = camp.total_rewards || 0;"""

js = js.replace(target_mock, replacement_real)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the hardcoded numbers and trend lines in the HTML to avoid any flashes of fake data
html = html.replace('>1,204<', '>0<')
html = html.replace('>84<', '>0<')

# Replace the fake trend percentages with an empty state or 0%
target_trend1 = '<i class="fa-solid fa-arrow-trend-up"></i> +12% esta semana'
target_trend2 = '<i class="fa-solid fa-arrow-trend-up"></i> +5% esta semana'
replacement_trend = '<i class="fa-solid fa-circle-info"></i> Esperando actividad'

html = html.replace(target_trend1, replacement_trend)
html = html.replace(target_trend2, replacement_trend)

# Change color of the "Esperando actividad" to muted instead of green
html = html.replace('color:#10b981;', 'color:var(--text-muted);')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
