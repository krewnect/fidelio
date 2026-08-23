import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

metrics_start = html.find('<section id="tab-metrics" class="tab-content">')
metrics_end = html.find('</section>', metrics_start) + len('</section>')

new_metrics = """<section id="tab-metrics" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <div class="workspace-eyebrow">Rendimiento</div>
                        <h1>Métricas y Analytics</h1>
                        <p>Analiza el retorno de inversión y el desempeño de tus campañas.</p>
                    </div>
                </div>

                <!-- GEMINI METRICS INSIGHTS -->
                <div class="gemini-insight-panel">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; opacity: 0.05; filter: grayscale(1);">
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

                <!-- KPI GRID (4 COLUMNS) -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px; margin-bottom: 24px;">
                    <div class="stat-card">
                        <div style="font-size: 13px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
                            <span>Base de Lealtad</span>
                            <i class="fa-solid fa-users" style="color: #7C3AED;"></i>
                        </div>
                        <div id="metric-base" style="font-size: 32px; font-weight: 800; color: #111827; letter-spacing: -1px;">0</div>
                        <div style="font-size: 13px; color: #10B981; font-weight: 600; margin-top: 8px;"><i class="fa-solid fa-arrow-trend-up"></i> +0% vs mes pasado</div>
                    </div>
                    
                    <div class="stat-card">
                        <div style="font-size: 13px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
                            <span>Ticket Promedio</span>
                            <i class="fa-solid fa-receipt" style="color: #7C3AED;"></i>
                        </div>
                        <div id="metric-ticket" style="font-size: 32px; font-weight: 800; color: #111827; letter-spacing: -1px;">$0.00</div>
                        <div style="font-size: 13px; color: #6B7280; font-weight: 500; margin-top: 8px;">Basado en historial</div>
                    </div>
                    
                    <div class="stat-card">
                        <div style="font-size: 13px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
                            <span>Tasa de Redención</span>
                            <i class="fa-solid fa-fire" style="color: #F59E0B;"></i>
                        </div>
                        <div id="metric-redemption" style="font-size: 32px; font-weight: 800; color: #111827; letter-spacing: -1px;">0%</div>
                        <div style="font-size: 13px; color: #6B7280; font-weight: 500; margin-top: 8px;">Basado en premios</div>
                    </div>
                    
                    <div class="stat-card">
                        <div style="font-size: 13px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
                            <span>Frecuencia</span>
                            <i class="fa-solid fa-rotate-right" style="color: #3B82F6;"></i>
                        </div>
                        <div id="metric-freq" style="font-size: 32px; font-weight: 800; color: #111827; letter-spacing: -1px;">0.0x <span style="font-size:16px; font-weight:600; color:#6B7280;">/mes</span></div>
                        <div style="font-size: 13px; color: #6B7280; font-weight: 500; margin-top: 8px;">Últimos 30 días</div>
                    </div>
                </div>

                <!-- ROI BANNER -->
                <div class="content-panel" style="display: flex; flex-wrap: wrap; gap: 32px; align-items: center; justify-content: space-between; background: #111827 !important; border: none !important; color: white !important;">
                    <div style="flex: 1; min-width: 300px;">
                        <div style="font-size: 13px; font-weight: 700; color: #8B5CF6; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 12px;">Retorno de Inversión (ROI)</div>
                        <div style="font-size: 64px; font-weight: 800; letter-spacing: -2px; margin-bottom: 8px; line-height: 1;">+0%</div>
                        <p style="color: #9CA3AF; font-size: 15px; margin: 0; max-width: 400px; line-height: 1.6;">
                            Por cada $1 MXN invertido en tu suscripción Fidelio, tus clientes han generado <strong>$0.00</strong> en ingresos atribuibles por lealtad.
                        </p>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 24px; border-radius: 20px; text-align: center; min-width: 200px;">
                        <div style="font-size: 13px; color: #9CA3AF; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">Ingreso Atribuido</div>
                        <div style="font-size: 36px; font-weight: 800; color: #10B981; letter-spacing: -1px; margin-bottom: 8px;">+$0.00</div>
                        <div style="background: rgba(16, 185, 129, 0.1); color: #10B981; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 20px; display: inline-block;">
                            <i class="fa-solid fa-arrow-trend-up"></i> Calculando...
                        </div>
                    </div>
                </div>

                <!-- CHARTS AND TABLES GRID -->
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px; margin-top: 24px;">
                    <!-- LEFT COLUMN: CHART -->
                    <div class="content-panel" style="display: flex; flex-direction: column;">
                        <h3 style="font-size: 18px; font-weight: 700; color: #111827; margin: 0 0 24px 0;">Retención de Clientes vs Nuevos</h3>
                        
                        <!-- Simple visual bars placeholder representing a chart -->
                        <div style="display: flex; align-items: flex-end; justify-content: space-around; height: 200px; padding-top: 20px; border-bottom: 1px solid #E5E7EB;">
                            <div style="width: 40px; background: #E5E7EB; height: 30%; border-radius: 6px 6px 0 0; position: relative;">
                                <div style="position: absolute; bottom: 100%; width: 100%; text-align: center; font-size: 12px; color: #6B7280; padding-bottom: 8px;">Ene</div>
                            </div>
                            <div style="width: 40px; background: #E5E7EB; height: 50%; border-radius: 6px 6px 0 0; position: relative;">
                                <div style="position: absolute; bottom: 0; width: 100%; background: #7C3AED; height: 40%; border-radius: 6px 6px 0 0;"></div>
                                <div style="position: absolute; bottom: 100%; width: 100%; text-align: center; font-size: 12px; color: #6B7280; padding-bottom: 8px;">Feb</div>
                            </div>
                            <div style="width: 40px; background: #E5E7EB; height: 40%; border-radius: 6px 6px 0 0; position: relative;">
                                <div style="position: absolute; bottom: 0; width: 100%; background: #7C3AED; height: 60%; border-radius: 6px 6px 0 0;"></div>
                                <div style="position: absolute; bottom: 100%; width: 100%; text-align: center; font-size: 12px; color: #6B7280; padding-bottom: 8px;">Mar</div>
                            </div>
                            <div style="width: 40px; background: #E5E7EB; height: 70%; border-radius: 6px 6px 0 0; position: relative;">
                                <div style="position: absolute; bottom: 0; width: 100%; background: #7C3AED; height: 80%; border-radius: 6px 6px 0 0;"></div>
                                <div style="position: absolute; bottom: 100%; width: 100%; text-align: center; font-size: 12px; color: #6B7280; padding-bottom: 8px;">Abr</div>
                            </div>
                            <div style="width: 40px; background: #E5E7EB; height: 60%; border-radius: 6px 6px 0 0; position: relative;">
                                <div style="position: absolute; bottom: 0; width: 100%; background: #7C3AED; height: 90%; border-radius: 6px 6px 0 0;"></div>
                                <div style="position: absolute; bottom: 100%; width: 100%; text-align: center; font-size: 12px; color: #6B7280; padding-bottom: 8px;">May</div>
                            </div>
                        </div>
                        <div style="display: flex; gap: 16px; margin-top: 24px; justify-content: center; font-size: 13px; color: #6B7280; font-weight: 500;">
                            <span style="display:flex; align-items:center; gap:6px;"><div style="width:10px; height:10px; background:#7C3AED; border-radius:2px;"></div> Leales</span>
                            <span style="display:flex; align-items:center; gap:6px;"><div style="width:10px; height:10px; background:#E5E7EB; border-radius:2px;"></div> Nuevos</span>
                        </div>
                    </div>
                    
                    <!-- RIGHT COLUMN: TABLE -->
                    <div class="content-panel">
                        <h3 style="font-size: 18px; font-weight: 700; color: #111827; margin: 0 0 24px 0;">Premios Redimidos</h3>
                        <div style="display: flex; flex-direction: column; gap: 16px;">
                            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 16px; border-bottom: 1px solid #E5E7EB;">
                                <div style="display: flex; align-items: center; gap: 12px;">
                                    <div style="width: 40px; height: 40px; border-radius: 10px; background: #F3F4F6; display: flex; align-items: center; justify-content: center; color: #6B7280; font-size: 16px;">
                                        <i class="fa-solid fa-gift"></i>
                                    </div>
                                    <div>
                                        <div style="font-weight: 600; color: #111827; font-size: 14px;">Café Gratis</div>
                                        <div style="font-size: 13px; color: #6B7280;">10 Sellos</div>
                                    </div>
                                </div>
                                <div style="font-weight: 700; color: #111827;">0</div>
                            </div>
                            <div style="text-align: center; padding: 24px; color: #9CA3AF; font-size: 14px;">
                                Aún no hay redenciones registradas.
                            </div>
                        </div>
                    </div>
                </div>
            </section>"""

html = html[:metrics_start] + new_metrics + html[metrics_end:]

# ADD CSS FOR THE DASHBOARD TABLES (Campañas / CRM) SO THEY DON'T LOOK UGLY/SCROLL HORIZONTALLY
table_css = """
/* Responsive Tables for Fidelio UI */
.fidelio-table-container {
    width: 100%;
    overflow-x: auto;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    background: #FFFFFF;
}
.fidelio-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    white-space: nowrap;
}
.fidelio-table th {
    background: #F9FAFB;
    padding: 16px 24px;
    font-size: 12px;
    font-weight: 700;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid #E5E7EB;
}
.fidelio-table td {
    padding: 16px 24px;
    font-size: 14px;
    color: #111827;
    border-bottom: 1px solid #E5E7EB;
}
.fidelio-table tr:last-child td {
    border-bottom: none;
}
.fidelio-table tbody tr:hover {
    background: #F9FAFB;
}
"""
html = html.replace('</style>', table_css + '\n</style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
