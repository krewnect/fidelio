with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<div class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">0</div>', '<div id="metric-adv-loyalty" class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">0</div>')
html = html.replace('<div class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">$0.00</div>', '<div id="metric-adv-ticket" class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">$0.00</div>')
html = html.replace('<div class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">0%</div>', '<div id="metric-adv-redemption" class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">0%</div>')
html = html.replace('<div class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">0x<span style="font-size:16px; color:var(--text-muted); font-weight:500;">/mes</span></div>', '<div id="metric-adv-freq" class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">0x<span style="font-size:16px; color:var(--text-muted); font-weight:500;">/mes</span></div>')

# Also the dummy trends
html = html.replace('<div class="stat-trend trend-up" style="margin-top:12px; background: var(--bg-input); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> +12% mes anterior</div>', '<div class="stat-trend trend-up" style="margin-top:12px; background: var(--bg-input); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> Calculando...</div>')
html = html.replace('<div class="stat-trend trend-up" style="margin-top:12px; background: var(--bg-input); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> 22% > No-VIP</div>', '<div class="stat-trend trend-up" style="margin-top:12px; background: var(--bg-input); padding:4px 8px; border-radius:4px; display:inline-block;">Basado en historial</div>')
html = html.replace('<div class="stat-trend trend-up" style="margin-top:12px; background: var(--bg-input); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> Alto Engagement</div>', '<div class="stat-trend trend-up" style="margin-top:12px; background: var(--bg-input); padding:4px 8px; border-radius:4px; display:inline-block;">Basado en premios</div>')
html = html.replace('<div class="stat-trend trend-up" style="margin-top:12px; background: var(--bg-input); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> +0.4x desde Mayo</div>', '<div class="stat-trend trend-up" style="margin-top:12px; background: var(--bg-input); padding:4px 8px; border-radius:4px; display:inline-block;">Últimos 30 días</div>')

import re
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
