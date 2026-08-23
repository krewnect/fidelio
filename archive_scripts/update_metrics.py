import re

with open('index.html', 'r') as f:
    html = f.read()

new_metrics_content = """<section id="tab-metrics" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">MÉTRICAS Y ROI</span>
                        <h1>Inteligencia de Negocio</h1>
                        <p>Descubre el impacto económico real de tu programa de lealtad Fidelio.</p>
                    </div>
                    <div style="display:flex; gap:12px;">
                        <select class="fidelio-input" style="width:auto;">
                            <option>Últimos 30 días</option>
                            <option>Últimos 3 meses</option>
                            <option>Este año</option>
                            <option>Historico Total</option>
                        </select>
                        <button class="btn btn-outline"><i class="fa-solid fa-download"></i> Exportar Reporte</button>
                    </div>
                </div>

                <!-- ROI HIGHLIGHT -->
                <div style="background: linear-gradient(135deg, var(--accent-violet) 0%, #2e0d5f 100%); border-radius: var(--radius-md); padding: 32px; color: white; display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; box-shadow: var(--shadow-lg);">
                    <div>
                        <span style="text-transform: uppercase; letter-spacing: 2px; font-size: 12px; opacity: 0.8; font-weight: 700;">Retorno de Inversión (ROI) Estimado</span>
                        <h2 style="font-size: 48px; margin: 8px 0 0 0; color: white;">+342%</h2>
                        <p style="opacity: 0.9; margin-top: 8px; max-width: 500px;">Por cada $1 invertido en Fidelio, tus clientes fidelizados han generado $3.42 adicionales en ventas.</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 24px; border-radius: var(--radius-md); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                        <div style="font-size: 14px; opacity: 0.8; margin-bottom: 4px;">Ingreso Atribuido a Lealtad</div>
                        <div style="font-size: 32px; font-weight: 800; color: #10B981;">+$124,500 <span style="font-size:16px; font-weight:600; opacity:0.8;">MXN</span></div>
                    </div>
                </div>
                
                <!-- BENTO GRID METRICS -->
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px;">
                    <div class="stat-card" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div class="stat-icon" style="background: rgba(76, 29, 149, 0.1); color: var(--accent-violet);"><i class="fa-solid fa-users"></i></div>
                        <div class="stat-value">1,248</div>
                        <div class="stat-label">Clientes en Wallet</div>
                        <div class="stat-trend trend-up"><i class="fa-solid fa-arrow-up"></i> 12% vs mes anterior</div>
                    </div>
                    <div class="stat-card" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div class="stat-icon" style="background: rgba(16, 185, 129, 0.1); color: #10B981;"><i class="fa-solid fa-wallet"></i></div>
                        <div class="stat-value">$42,300</div>
                        <div class="stat-label">Cashback Emitido</div>
                        <div class="stat-trend trend-up"><i class="fa-solid fa-arrow-up"></i> 5% vs mes anterior</div>
                    </div>
                    <div class="stat-card" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div class="stat-icon" style="background: rgba(245, 158, 11, 0.1); color: #F59E0B;"><i class="fa-solid fa-fire"></i></div>
                        <div class="stat-value">$18,400</div>
                        <div class="stat-label">Cashback Redimido (Usado)</div>
                        <div class="stat-trend trend-down" style="color:var(--text-muted);"><i class="fa-solid fa-arrow-up"></i> 2% vs mes anterior</div>
                    </div>
                    <div class="stat-card" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div class="stat-icon" style="background: rgba(239, 68, 68, 0.1); color: #EF4444;"><i class="fa-solid fa-repeat"></i></div>
                        <div class="stat-value">2.4x</div>
                        <div class="stat-label">Visitas Mensuales Promedio</div>
                        <div class="stat-trend trend-up"><i class="fa-solid fa-arrow-up"></i> 0.3x vs trimestre anterior</div>
                    </div>
                </div>

                <!-- CAMPAIGNS & PROMOTIONS -->
                <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 24px; margin-bottom: 40px;">
                    <!-- MARKETING CAMPAIGNS -->
                    <div style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px;">
                            <h3 style="color: var(--text-main); font-size: 18px; margin:0;"><i class="fa-solid fa-robot" style="color:var(--accent-violet); margin-right:8px;"></i>Rendimiento de Campañas IA</h3>
                            <button style="background:none; border:none; color:var(--accent-violet); font-weight:600; cursor:pointer;">Ver Todas</button>
                        </div>
                        
                        <div style="display:flex; flex-direction:column; gap:16px;">
                            <div style="display:grid; grid-template-columns: 2fr 1fr 1fr 1fr; align-items:center; padding:12px; background:var(--bg-input); border-radius:8px; font-size:14px; font-weight:600; color:var(--text-muted);">
                                <div>Campaña</div>
                                <div style="text-align:right;">Apertura</div>
                                <div style="text-align:right;">Conversión</div>
                                <div style="text-align:right;">Retorno</div>
                            </div>
                            
                            <div style="display:grid; grid-template-columns: 2fr 1fr 1fr 1fr; align-items:center; padding:12px; border-bottom:1px solid var(--border-glass); font-size:14px;">
                                <div><div style="font-weight:600; color:var(--text-main);">Recuperación de Clientes</div><div style="font-size:12px; color:var(--text-muted);">Doble Cashback Fin de Semana</div></div>
                                <div style="text-align:right; font-weight:600;">68%</div>
                                <div style="text-align:right; font-weight:600; color:var(--accent-emerald);">14.2%</div>
                                <div style="text-align:right; font-weight:700;">$12,400</div>
                            </div>
                            <div style="display:grid; grid-template-columns: 2fr 1fr 1fr 1fr; align-items:center; padding:12px; border-bottom:1px solid var(--border-glass); font-size:14px;">
                                <div><div style="font-weight:600; color:var(--text-main);">Feliz Cumpleaños (Agosto)</div><div style="font-size:12px; color:var(--text-muted);">Cortesía Sorpresa Automática</div></div>
                                <div style="text-align:right; font-weight:600;">85%</div>
                                <div style="text-align:right; font-weight:600; color:var(--accent-emerald);">42.5%</div>
                                <div style="text-align:right; font-weight:700;">$5,800</div>
                            </div>
                            <div style="display:grid; grid-template-columns: 2fr 1fr 1fr 1fr; align-items:center; padding:12px; font-size:14px;">
                                <div><div style="font-weight:600; color:var(--text-main);">Martes Locos (Días Lentos)</div><div style="font-size:12px; color:var(--text-muted);">Upgrade Nivel VIP 4pm-7pm</div></div>
                                <div style="text-align:right; font-weight:600;">52%</div>
                                <div style="text-align:right; font-weight:600; color:var(--accent-emerald);">8.1%</div>
                                <div style="text-align:right; font-weight:700;">$3,200</div>
                            </div>
                        </div>
                    </div>

                    <!-- REWARD SUCCESS -->
                    <div style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <h3 style="margin-bottom: 24px; color: var(--text-main); font-size: 18px;"><i class="fa-solid fa-gift" style="color:var(--accent-amber); margin-right:8px;"></i>Recompensas Más Exitosas</h3>
                        
                        <div style="display:flex; flex-direction:column; gap:20px;">
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px; font-weight:600;">
                                    <span>Cashback Puntos (General)</span>
                                    <span>54%</span>
                                </div>
                                <div style="width:100%; height:8px; background:var(--bg-input); border-radius:4px; overflow:hidden;">
                                    <div style="width:54%; height:100%; background:var(--accent-violet); border-radius:4px;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px; font-weight:600;">
                                    <span>Cortesía de Cumpleaños</span>
                                    <span>28%</span>
                                </div>
                                <div style="width:100%; height:8px; background:var(--bg-input); border-radius:4px; overflow:hidden;">
                                    <div style="width:28%; height:100%; background:var(--accent-emerald); border-radius:4px;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px; font-weight:600;">
                                    <span>Beneficio VIP Oro (Filas)</span>
                                    <span>12%</span>
                                </div>
                                <div style="width:100%; height:8px; background:var(--bg-input); border-radius:4px; overflow:hidden;">
                                    <div style="width:12%; height:100%; background:var(--accent-amber); border-radius:4px;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:14px; font-weight:600;">
                                    <span>Otros (Regalos de Temporada)</span>
                                    <span>6%</span>
                                </div>
                                <div style="width:100%; height:8px; background:var(--bg-input); border-radius:4px; overflow:hidden;">
                                    <div style="width:6%; height:100%; background:var(--text-muted); border-radius:4px;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- CHARTS ROW -->
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;">
                    <div style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px;">
                            <h3 style="color: var(--text-main); font-size: 18px; margin:0;">Crecimiento de Ventas Atribuidas a Lealtad</h3>
                            <div style="font-size:12px; color:var(--text-muted);"><i class="fa-solid fa-circle" style="color:var(--accent-violet); font-size:8px; margin-right:4px;"></i> 2026 vs <i class="fa-solid fa-circle" style="color:var(--border-glass); font-size:8px; margin-right:4px;"></i> 2025</div>
                        </div>
                        <div style="height: 250px; background: repeating-linear-gradient(0deg, transparent, transparent 49px, var(--border-glass) 49px, var(--border-glass) 50px); display:flex; align-items:flex-end; gap:24px; padding-top:20px; padding-bottom:0;">
                            <!-- Fake chart bars with beautiful design -->
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div style="width:50%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 20%;"></div>
                                <div style="width:50%; background: var(--accent-violet); opacity: 0.9; border-radius: 6px 6px 0 0; height: 35%;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Ene</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div style="width:50%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 25%;"></div>
                                <div style="width:50%; background: var(--accent-violet); opacity: 0.9; border-radius: 6px 6px 0 0; height: 42%;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Feb</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div style="width:50%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 22%;"></div>
                                <div style="width:50%; background: var(--accent-violet); opacity: 0.9; border-radius: 6px 6px 0 0; height: 50%;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Mar</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div style="width:50%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 30%;"></div>
                                <div style="width:50%; background: var(--accent-violet); opacity: 0.9; border-radius: 6px 6px 0 0; height: 65%;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Abr</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div style="width:50%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 35%;"></div>
                                <div style="width:50%; background: var(--accent-violet); opacity: 1; border-radius: 6px 6px 0 0; height: 85%; box-shadow: 0 0 15px rgba(76,29,149,0.3);"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-main);">May</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div style="width:50%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 28%;"></div>
                                <div style="width:50%; background: var(--accent-violet); opacity: 0.9; border-radius: 6px 6px 0 0; height: 75%;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Jun</div>
                            </div>
                        </div>
                    </div>
                    <div style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm); display:flex; flex-direction:column;">
                        <h3 style="margin-bottom: 24px; color: var(--text-main); font-size: 18px;">Demografía y Lealtad</h3>
                        <div style="flex:1; display:flex; align-items:center; justify-content:center; position:relative;">
                            <!-- Fake Donut Chart -->
                            <div style="width: 160px; height: 160px; border-radius: 50%; background: conic-gradient(var(--accent-violet) 0% 65%, var(--accent-emerald) 65% 85%, var(--accent-amber) 85% 100%); display:flex; align-items:center; justify-content:center; box-shadow: var(--shadow-md);">
                                <div style="width: 120px; height: 120px; border-radius: 50%; background: white; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                                    <div style="font-size:24px; font-weight:800; color:var(--text-main);">65%</div>
                                    <div style="font-size:10px; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; text-align:center;">Clientes<br>Frecuentes</div>
                                </div>
                            </div>
                        </div>
                        <div style="margin-top:24px; display:flex; flex-direction:column; gap:8px; font-size:13px;">
                            <div style="display:flex; justify-content:space-between;"><span style="color:var(--text-muted);"><i class="fa-solid fa-circle" style="color:var(--accent-violet); font-size:8px; margin-right:8px;"></i>Frecuentes (>3 visitas/mes)</span> <strong>65%</strong></div>
                            <div style="display:flex; justify-content:space-between;"><span style="color:var(--text-muted);"><i class="fa-solid fa-circle" style="color:var(--accent-emerald); font-size:8px; margin-right:8px;"></i>Ocasionales (1-2 visitas/mes)</span> <strong>20%</strong></div>
                            <div style="display:flex; justify-content:space-between;"><span style="color:var(--text-muted);"><i class="fa-solid fa-circle" style="color:var(--accent-amber); font-size:8px; margin-right:8px;"></i>Nuevos (Último mes)</span> <strong>15%</strong></div>
                        </div>
                    </div>
                </div>
            </section></main>"""

# Using regex to replace the old tab-metrics section
pattern = r'<section id="tab-metrics" class="tab-content">.*?</section>\s*</main>'
html = re.sub(pattern, new_metrics_content, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
