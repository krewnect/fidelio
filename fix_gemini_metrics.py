import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

gemini_panel = """
                <!-- GEMINI METRICS INSIGHTS -->
                <div class="gemini-insight-panel" style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 24px; padding: 32px; margin-bottom: 24px; position: relative; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; opacity: 0.03; filter: grayscale(1); color:#111827;">
                        <i class="fa-solid fa-chart-pie"></i>
                    </div>
                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 800; color: #111827; display: flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-chart-line" style="color: #7C3AED;"></i> Análisis Financiero (Gemini IA)
                    </h3>
                    <p id="gemini-metrics-text" style="margin: 0; font-size: 15px; color: #4B5563; line-height: 1.6; margin-bottom: 16px;">
                        Gemini puede analizar la rentabilidad de tus premios y sugerirte formas de aumentar tu Ticket Promedio.
                    </p>
                    <button class="fidelio-btn-primary" onclick="if(window.fetchGeminiMetricsInsights) window.fetchGeminiMetricsInsights()">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Generar Reporte de IA
                    </button>
                </div>

                <!-- 1. ROI HIGHLIGHT & LIVE FEED -->"""

html = html.replace('<!-- 1. ROI HIGHLIGHT & LIVE FEED -->', gemini_panel)

# Oh wait, let's fix the header eyebrow to use the new div structure just in case it's a span still:
html = html.replace('<span class="workspace-eyebrow">MÉTRICAS Y ROI</span>', '<div class="workspace-eyebrow">MÉTRICAS Y ROI</div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
