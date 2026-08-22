import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# DASHBOARD WIDGET
dashboard_widget = """
                <!-- GEMINI DASHBOARD INSIGHTS -->
                <div class="gemini-insight-panel" style="background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(59,130,246,0.05)); border: 1px solid rgba(139,92,246,0.3); border-radius: 16px; padding: 24px; margin-bottom: 24px; position: relative; overflow: hidden; animation: fadeInUp 0.5s;">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; opacity: 0.05; filter: grayscale(1);">🤖</div>
                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 800; color: #4c1d95; display: flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-sparkles" style="color: #8b5cf6;"></i> Asistente Gemini (Resumen Directivo)
                    </h3>
                    <p id="gemini-dashboard-text" style="margin: 0; font-size: 14px; color: #475569; line-height: 1.6;">
                        Gemini está analizando tus métricas para darte un resumen directivo de tu negocio...
                    </p>
                </div>
"""

html = html.replace('<div class="stats-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px;">', dashboard_widget + '\n                <div class="stats-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px;">')


# CRM WIDGET
crm_widget = """
                <!-- GEMINI CRM INSIGHTS -->
                <div class="gemini-insight-panel" style="background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(59,130,246,0.05)); border: 1px solid rgba(139,92,246,0.3); border-radius: 16px; padding: 24px; margin-bottom: 24px; position: relative; overflow: hidden; animation: fadeInUp 0.5s;">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; opacity: 0.05; filter: grayscale(1);">🤖</div>
                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 800; color: #4c1d95; display: flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-magnifying-glass-chart" style="color: #8b5cf6;"></i> Análisis Inteligente de Cartera
                    </h3>
                    <p id="gemini-crm-text" style="margin: 0; font-size: 14px; color: #475569; line-height: 1.6;">
                        Gemini está revisando los perfiles de tus clientes para encontrar patrones de consumo y oportunidades de venta...
                    </p>
                </div>
"""

html = html.replace('<!-- KPI Dashboard -->\n                <div class="stats-grid" style="margin-bottom: 24px;">', crm_widget + '\n                <!-- KPI Dashboard -->\n                <div class="stats-grid" style="margin-bottom: 24px;">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
