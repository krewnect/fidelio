import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

home_start = html.find('<section id="tab-home" class="tab-content active">')
home_end = html.find('</section>', home_start) + len('</section>')

new_home = """<section id="tab-home" class="tab-content active">
                
                <!-- PORTAL PUBLICO -->
                <div class="content-panel" style="background: #111827 !important; border: none !important; color: white !important; margin-bottom: 32px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px;">
                    <div style="flex: 1; min-width: 280px;">
                        <h2 style="font-size: 18px; margin-bottom: 8px; font-weight: 700; color: #FFFFFF; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-earth-americas" style="color: #8B5CF6;"></i> Tu Portal Público</h2>
                        <p style="color: #9CA3AF; font-size: 14px; margin: 0; max-width: 500px; line-height:1.6;">Comparte este enlace con tus clientes para que se registren y descarguen su tarjeta en Apple o Google Wallet.</p>
                    </div>
                    <div style="display: flex; gap: 12px; align-items: center; background: rgba(255,255,255,0.05); padding: 8px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="padding: 0 12px; font-family: monospace; font-size: 14px; color: #E5E7EB;" id="landing-link-display">
                            fideliorewards.com/tu-negocio
                        </div>
                        <button class="fidelio-btn-primary" style="padding: 8px 16px; font-size:13px;" onclick="copyLandingLink()">
                            <i class="fa-regular fa-copy"></i> Copiar
                        </button>
                    </div>
                </div>

                <div class="workspace-header">
                    <div>
                        <div class="workspace-eyebrow">DASHBOARD</div>
                        <h1>Rendimiento en Vivo</h1>
                        <p>Métricas financieras y comportamiento de tus clientes en tiempo real.</p>
                    </div>
                    <button class="fidelio-btn-primary" style="background: #F3F4F6 !important; color: #111827 !important;" onclick="window.location.reload()"><i class="fa-solid fa-rotate-right"></i> Actualizar</button>
                </div>

                <!-- GEMINI DASHBOARD INSIGHTS -->
                <div class="gemini-insight-panel" style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 24px; padding: 32px; margin-bottom: 24px; position: relative; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; opacity: 0.05; filter: grayscale(1);">
                        <i class="fa-solid fa-chart-line"></i>
                    </div>
                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 800; color: #111827; display: flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-sparkles" style="color: #7C3AED;"></i> Asistente Gemini (Resumen Directivo)
                    </h3>
                    <p id="gemini-dashboard-text" style="margin: 0; font-size: 15px; color: #4B5563; line-height: 1.6; margin-bottom: 16px;">
                        Presiona el botón para que Gemini analice el rendimiento general de tus operaciones y te brinde recomendaciones.
                    </p>
                    <button class="fidelio-btn-primary" onclick="if(window.fetchGeminiDashboardInsights) window.fetchGeminiDashboardInsights()" style="background:#7C3AED; color:white; border:none; border-radius:12px; padding:10px 20px; font-weight:600; font-size:14px; cursor:pointer; display:flex; align-items:center; gap:8px;">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Analizar Rendimiento
                    </button>
                </div>

                <!-- KPI GRID -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px; margin-bottom: 24px;">
                    <div class="stat-card">
                        <div style="font-size: 13px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
                            <span>Ventas Impulsadas</span>
                            <i class="fa-solid fa-sack-dollar" style="color: #10B981;"></i>
                        </div>
                        <div id="metric-sales" style="font-size: 32px; font-weight: 800; color: #111827; letter-spacing: -1px;">$0.00</div>
                        <div style="font-size: 13px; color: #10B981; font-weight: 600; margin-top: 8px;"><i class="fa-solid fa-arrow-trend-up"></i> Total Histórico</div>
                    </div>
                    
                    <div class="stat-card">
                        <div style="font-size: 13px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
                            <span>Escaneos Totales</span>
                            <i class="fa-solid fa-barcode" style="color: #7C3AED;"></i>
                        </div>
                        <div id="metric-scans" style="font-size: 32px; font-weight: 800; color: #111827; letter-spacing: -1px;">0</div>
                        <div style="font-size: 13px; color: #6B7280; font-weight: 500; margin-top: 8px;">Visitas registradas</div>
                    </div>
                    
                    <div class="stat-card">
                        <div style="font-size: 13px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
                            <span>Clientes Activos</span>
                            <i class="fa-solid fa-users" style="color: #3B82F6;"></i>
                        </div>
                        <div id="metric-customers" style="font-size: 32px; font-weight: 800; color: #111827; letter-spacing: -1px;">0</div>
                        <div style="font-size: 13px; color: #6B7280; font-weight: 500; margin-top: 8px;">En tu base de datos</div>
                    </div>
                </div>

                <!-- 2 COLUMN LAYOUT -->
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
                    <div class="content-panel">
                        <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 24px 0; display:flex; justify-content:space-between; align-items:center;">
                            <span>Actividad Reciente</span>
                            <button class="fidelio-btn-primary" style="background:#F3F4F6 !important; color:#111827 !important; padding:6px 12px; font-size:12px; border-radius:8px;">Ver todo</button>
                        </h3>
                        <div id="activity-feed" style="display: flex; flex-direction: column; gap: 16px;">
                            <div style="text-align: center; color: #9CA3AF; padding: 40px 0; font-size: 14px;">Aún no hay actividad registrada hoy.</div>
                        </div>
                    </div>
                    
                    <div class="content-panel">
                        <h3 style="font-size: 16px; font-weight: 700; color: #111827; margin: 0 0 24px 0;">Atajos Rápidos</h3>
                        <div style="display: flex; flex-direction: column; gap: 12px;">
                            <button onclick="switchTab('campaigns')" style="width:100%; text-align:left; background:#F9FAFB; border:1px solid #E5E7EB; padding:16px; border-radius:12px; cursor:pointer; font-weight:600; color:#374151; display:flex; align-items:center; gap:12px; transition:all 0.2s;">
                                <div style="width:32px; height:32px; background:#E0E7FF; color:#4F46E5; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-paper-plane"></i></div>
                                Enviar Campaña
                            </button>
                            <button onclick="switchTab('crm')" style="width:100%; text-align:left; background:#F9FAFB; border:1px solid #E5E7EB; padding:16px; border-radius:12px; cursor:pointer; font-weight:600; color:#374151; display:flex; align-items:center; gap:12px; transition:all 0.2s;">
                                <div style="width:32px; height:32px; background:#DCFCE7; color:#16A34A; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-user-plus"></i></div>
                                Añadir Cliente
                            </button>
                            <button onclick="switchTab('stripe')" style="width:100%; text-align:left; background:#F9FAFB; border:1px solid #E5E7EB; padding:16px; border-radius:12px; cursor:pointer; font-weight:600; color:#374151; display:flex; align-items:center; gap:12px; transition:all 0.2s;">
                                <div style="width:32px; height:32px; background:#FEF3C7; color:#D97706; border-radius:8px; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-sack-dollar"></i></div>
                                Cobrar en Wallet
                            </button>
                        </div>
                    </div>
                </div>

            </section>"""

html = html[:home_start] + new_home + html[home_end:]

# ADD QUICK HOVER FIX FOR NEW BUTTONS
hover_css = """
/* Fix new button hovers */
#tab-home button[style*="background:#F9FAFB"]:hover {
    background: #F3F4F6 !important;
    border-color: #D1D5DB !important;
}
"""
html = html.replace('</style>', hover_css + '\n</style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

