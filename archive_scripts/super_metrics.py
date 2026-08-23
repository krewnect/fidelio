import re

with open('index.html', 'r') as f:
    html = f.read()

new_metrics_content = """<section id="tab-metrics" class="tab-content">
                <style>
                    /* Dynamic Animations */
                    @keyframes pulseGlow { 0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }
                    @keyframes floatUp { 0% { transform: translateY(20px); opacity: 0; } 100% { transform: translateY(0); opacity: 1; } }
                    @keyframes progressFill { 0% { width: 0; } 100% { width: 100%; } }
                    @keyframes numberCounter { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                    @keyframes chartBarGrow { from { height: 0; } }
                    
                    .metric-card-hover { transition: all 0.3s ease; }
                    .metric-card-hover:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(76, 29, 149, 0.12); border-color: rgba(76, 29, 149, 0.3); }
                    
                    .live-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.1); color: #10B981; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.2); }
                    .live-dot { width: 8px; height: 8px; background: #10B981; border-radius: 50%; animation: pulseGlow 2s infinite; }
                    
                    .bento-chart-bar { animation: chartBarGrow 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; transform-origin: bottom; }
                    
                    .table-row-hover { transition: background 0.2s; }
                    .table-row-hover:hover { background: var(--bg-input); cursor: pointer; }
                    
                    .heatmap-cell { border-radius: 4px; transition: transform 0.2s; cursor: pointer; }
                    .heatmap-cell:hover { transform: scale(1.1); box-shadow: 0 4px 10px rgba(0,0,0,0.1); z-index: 10; position: relative; }
                    
                    .stagger-1 { animation: floatUp 0.6s ease forwards 0.1s; opacity: 0; }
                    .stagger-2 { animation: floatUp 0.6s ease forwards 0.2s; opacity: 0; }
                    .stagger-3 { animation: floatUp 0.6s ease forwards 0.3s; opacity: 0; }
                    .stagger-4 { animation: floatUp 0.6s ease forwards 0.4s; opacity: 0; }
                    .stagger-5 { animation: floatUp 0.6s ease forwards 0.5s; opacity: 0; }
                </style>

                <div class="workspace-header stagger-1">
                    <div>
                        <div style="display:flex; align-items:center; gap:16px;">
                            <span class="workspace-eyebrow">MÉTRICAS Y ROI</span>
                            <div class="live-badge"><div class="live-dot"></div> Live Analytics</div>
                        </div>
                        <h1>Inteligencia de Negocio Avanzada</h1>
                        <p>Descubre el impacto económico real, el comportamiento de tus clientes y la efectividad de tus campañas.</p>
                    </div>
                    <div style="display:flex; gap:12px;">
                        <select class="fidelio-input" style="width:auto; cursor:pointer;">
                            <option>Últimos 30 días</option>
                            <option>Últimos 3 meses</option>
                            <option>Este año</option>
                            <option>Histórico Total</option>
                        </select>
                        <button class="btn btn-outline metric-card-hover"><i class="fa-solid fa-cloud-arrow-down"></i> PDF Report</button>
                    </div>
                </div>

                <!-- 1. ROI HIGHLIGHT & LIVE FEED -->
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px; margin-bottom: 24px;" class="stagger-1">
                    <div class="metric-card-hover" style="background: linear-gradient(135deg, var(--accent-violet) 0%, #1e0542 100%); border-radius: var(--radius-md); padding: 40px; color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-lg); position: relative; overflow: hidden;">
                        <!-- Background glow effect -->
                        <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: rgba(16, 185, 129, 0.2); border-radius: 50%; filter: blur(40px);"></div>
                        
                        <div style="position: relative; z-index: 2;">
                            <span style="text-transform: uppercase; letter-spacing: 2px; font-size: 12px; opacity: 0.8; font-weight: 700; display:flex; align-items:center; gap:8px;">
                                <i class="fa-solid fa-chart-line"></i> Retorno de Inversión Estimado
                            </span>
                            <h2 style="font-size: 64px; margin: 8px 0 0 0; color: white; font-weight: 900; letter-spacing:-1px;">
                                <span style="animation: numberCounter 1s ease-out forwards;">+342%</span>
                            </h2>
                            <p style="opacity: 0.9; margin-top: 8px; max-width: 450px; font-size: 15px; line-height: 1.6;">Por cada $1 invertido en Fidelio, tus clientes han generado $3.42 en ventas adicionales y retención comprobada.</p>
                        </div>
                        <div style="position: relative; z-index: 2; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); box-shadow: inset 0 0 20px rgba(255,255,255,0.05);">
                            <div style="font-size: 13px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; margin-bottom: 8px;">Ingreso Atribuido a Lealtad</div>
                            <div style="font-size: 38px; font-weight: 800; color: #34d399; display:flex; align-items:baseline; gap:4px;">
                                +$124k <span style="font-size:16px; font-weight:600; opacity:0.8; color:white;">MXN</span>
                            </div>
                            <div style="margin-top: 12px; display:flex; align-items:center; gap:8px; font-size: 12px; color: #34d399; background:rgba(52, 211, 153, 0.1); padding:4px 10px; border-radius:12px; width:fit-content;">
                                <i class="fa-solid fa-arrow-trend-up"></i> +18% vs mes pasado
                            </div>
                        </div>
                    </div>
                    
                    <!-- LIVE TICKER -->
                    <div class="metric-card-hover" style="background: white; border-radius: var(--radius-md); padding: 24px; border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm); display:flex; flex-direction:column;">
                        <h3 style="color: var(--text-main); font-size: 16px; margin-bottom: 16px; display:flex; align-items:center; gap:8px;">
                            <i class="fa-solid fa-bolt" style="color:var(--accent-amber);"></i> Actividad en Vivo
                        </h3>
                        <div style="flex:1; overflow:hidden; position:relative;">
                            <div style="position:absolute; top:0; left:0; width:100%; height:20px; background:linear-gradient(to bottom, white, transparent); z-index:2;"></div>
                            <div style="position:absolute; bottom:0; left:0; width:100%; height:20px; background:linear-gradient(to top, white, transparent); z-index:2;"></div>
                            <div style="display:flex; flex-direction:column; gap:12px; padding: 10px 0;">
                                <div style="display:flex; align-items:center; gap:12px; font-size:13px; opacity:0.6;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:var(--bg-input); display:flex; align-items:center; justify-content:center; font-size:12px;"><i class="fa-solid fa-wallet"></i></div>
                                    <div style="flex:1;"><strong>Roberto O.</strong> usó $45 cashback</div>
                                    <div style="font-size:11px; color:var(--text-muted);">Hace 2m</div>
                                </div>
                                <div style="display:flex; align-items:center; gap:12px; font-size:13px;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:rgba(16, 185, 129, 0.1); color:#10B981; display:flex; align-items:center; justify-content:center; font-size:12px;"><i class="fa-solid fa-qrcode"></i></div>
                                    <div style="flex:1;"><strong>Ana G.</strong> escaneó mesa #4 (+120 pts)</div>
                                    <div style="font-size:11px; color:var(--text-muted);">Hace 5m</div>
                                </div>
                                <div style="display:flex; align-items:center; gap:12px; font-size:13px; opacity:0.8;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:rgba(245, 158, 11, 0.1); color:#F59E0B; display:flex; align-items:center; justify-content:center; font-size:12px;"><i class="fa-solid fa-crown"></i></div>
                                    <div style="flex:1;"><strong>Carlos R.</strong> subió a VIP Oro 🏆</div>
                                    <div style="font-size:11px; color:var(--text-muted);">Hace 14m</div>
                                </div>
                                <div style="display:flex; align-items:center; gap:12px; font-size:13px; opacity:0.5;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:var(--bg-input); display:flex; align-items:center; justify-content:center; font-size:12px;"><i class="fa-solid fa-envelope-open"></i></div>
                                    <div style="flex:1;">24 clientes abrieron promo Cumpleaños</div>
                                    <div style="font-size:11px; color:var(--text-muted);">Hace 30m</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 2. MICRO METRICS GRID -->
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px;" class="stagger-2">
                    <div class="stat-card metric-card-hover" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <div class="stat-label" style="font-weight:600; text-transform:uppercase; letter-spacing:0.5px; font-size:11px;">Base de Lealtad</div>
                                <div class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">1,248</div>
                            </div>
                            <div class="stat-icon" style="background: rgba(76, 29, 149, 0.1); color: var(--accent-violet);"><i class="fa-solid fa-users"></i></div>
                        </div>
                        <div class="stat-trend trend-up" style="margin-top:12px; background:rgba(16, 185, 129, 0.1); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> +12% mes anterior</div>
                    </div>
                    <div class="stat-card metric-card-hover" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <div class="stat-label" style="font-weight:600; text-transform:uppercase; letter-spacing:0.5px; font-size:11px;">Ticket Promedio (VIP)</div>
                                <div class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">$485</div>
                            </div>
                            <div class="stat-icon" style="background: rgba(16, 185, 129, 0.1); color: #10B981;"><i class="fa-solid fa-receipt"></i></div>
                        </div>
                        <div class="stat-trend trend-up" style="margin-top:12px; background:rgba(16, 185, 129, 0.1); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> 22% > No-VIP</div>
                    </div>
                    <div class="stat-card metric-card-hover" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <div class="stat-label" style="font-weight:600; text-transform:uppercase; letter-spacing:0.5px; font-size:11px;">Tasa de Redención</div>
                                <div class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">43.5%</div>
                            </div>
                            <div class="stat-icon" style="background: rgba(245, 158, 11, 0.1); color: #F59E0B;"><i class="fa-solid fa-fire"></i></div>
                        </div>
                        <div class="stat-trend trend-up" style="margin-top:12px; background:rgba(16, 185, 129, 0.1); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> Alto Engagement</div>
                    </div>
                    <div class="stat-card metric-card-hover" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <div class="stat-label" style="font-weight:600; text-transform:uppercase; letter-spacing:0.5px; font-size:11px;">Frecuencia Visitas</div>
                                <div class="stat-value" style="font-size:32px; font-weight:800; margin-top:8px;">2.8x<span style="font-size:16px; color:var(--text-muted); font-weight:500;">/mes</span></div>
                            </div>
                            <div class="stat-icon" style="background: rgba(6, 182, 212, 0.1); color: #06b6d4;"><i class="fa-solid fa-rotate-right"></i></div>
                        </div>
                        <div class="stat-trend trend-up" style="margin-top:12px; background:rgba(16, 185, 129, 0.1); padding:4px 8px; border-radius:4px; display:inline-block;"><i class="fa-solid fa-arrow-up"></i> +0.4x desde Mayo</div>
                    </div>
                </div>

                <!-- 3. BEHAVIOR & CAMPAIGNS (Advanced Data) -->
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px; margin-bottom: 24px;" class="stagger-3">
                    
                    <!-- HEATMAP & BEHAVIOR -->
                    <div class="metric-card-hover" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px;">
                            <div>
                                <h3 style="color: var(--text-main); font-size: 18px; margin:0;"><i class="fa-solid fa-map-location-dot" style="color:var(--accent-violet); margin-right:8px;"></i>Mapa de Calor de Redención</h3>
                                <p style="font-size:12px; color:var(--text-muted); margin-top:4px;">Descubre en qué horarios y días tus clientes usan más sus beneficios.</p>
                            </div>
                        </div>
                        
                        <!-- Fake Heatmap Grid -->
                        <div style="display:flex; flex-direction:column; gap:4px;">
                            <!-- Header -->
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; text-align:center; font-size:11px; font-weight:700; color:var(--text-muted); margin-bottom:8px;">
                                <div></div><div>Lun</div><div>Mar</div><div>Mié</div><div>Jue</div><div>Vie</div><div>Sáb</div><div>Dom</div>
                            </div>
                            <!-- Rows -->
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px;">
                                <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">12 PM</div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.1);" title="Lun 12PM: Bajo"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);" title="Mar 12PM: Regular"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.1);" title="Mie 12PM: Bajo"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.3);" title="Jue 12PM: Medio"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.6);" title="Vie 12PM: Alto"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.8);" title="Sab 12PM: Muy Alto"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.5);" title="Dom 12PM: Alto"></div>
                            </div>
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px;">
                                <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">2 PM</div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.3);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.4);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.3);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.5);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.9);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,1.0);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.7);"></div>
                            </div>
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px;">
                                <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">6 PM</div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.1);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.1);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.4);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.8);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.9);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.4);"></div>
                            </div>
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px;">
                                <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">8 PM</div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.3);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.6);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,1.0);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,1.0);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);"></div>
                            </div>
                        </div>
                        
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:20px; font-size:12px; color:var(--text-muted); border-top:1px solid var(--border-glass); padding-top:16px;">
                            <div style="display:flex; align-items:center; gap:8px;">
                                Menos tráfico <div style="width:60px; height:8px; background:linear-gradient(to right, rgba(76,29,149,0.1), rgba(76,29,149,1)); border-radius:4px;"></div> Más tráfico
                            </div>
                            <div style="font-weight:600; color:var(--accent-violet);">💡 Tip: Lanza campañas flash los Martes a las 6 PM.</div>
                        </div>
                    </div>
                    
                    <!-- LEADERBOARD TOP CLIENTS -->
                    <div class="metric-card-hover" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm); display:flex; flex-direction:column;">
                        <h3 style="margin-bottom: 20px; color: var(--text-main); font-size: 18px;"><i class="fa-solid fa-ranking-star" style="color:var(--accent-amber); margin-right:8px;"></i>Top Clientes (Mes)</h3>
                        
                        <div style="flex:1; display:flex; flex-direction:column; gap:12px;">
                            <div class="table-row-hover" style="display:flex; align-items:center; justify-content:space-between; padding:8px; border-radius:8px;">
                                <div style="display:flex; align-items:center; gap:12px;">
                                    <div style="width:28px; height:28px; background:#F59E0B; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:bold;">1</div>
                                    <div>
                                        <div style="font-size:14px; font-weight:600; color:var(--text-main);">Mariana Vega</div>
                                        <div style="font-size:11px; color:var(--accent-amber); font-weight:600;">VIP Oro</div>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-size:14px; font-weight:700;">$4,250</div>
                                    <div style="font-size:11px; color:var(--text-muted);">6 visitas</div>
                                </div>
                            </div>
                            
                            <div class="table-row-hover" style="display:flex; align-items:center; justify-content:space-between; padding:8px; border-radius:8px;">
                                <div style="display:flex; align-items:center; gap:12px;">
                                    <div style="width:28px; height:28px; background:#9CA3AF; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:bold;">2</div>
                                    <div>
                                        <div style="font-size:14px; font-weight:600; color:var(--text-main);">David Silva</div>
                                        <div style="font-size:11px; color:var(--text-muted); font-weight:600;">VIP Plata</div>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-size:14px; font-weight:700;">$3,800</div>
                                    <div style="font-size:11px; color:var(--text-muted);">4 visitas</div>
                                </div>
                            </div>
                            
                            <div class="table-row-hover" style="display:flex; align-items:center; justify-content:space-between; padding:8px; border-radius:8px;">
                                <div style="display:flex; align-items:center; gap:12px;">
                                    <div style="width:28px; height:28px; background:#B45309; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:bold;">3</div>
                                    <div>
                                        <div style="font-size:14px; font-weight:600; color:var(--text-main);">Elena Rios</div>
                                        <div style="font-size:11px; color:var(--text-muted); font-weight:600;">VIP Bronce</div>
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-size:14px; font-weight:700;">$2,950</div>
                                    <div style="font-size:11px; color:var(--text-muted);">5 visitas</div>
                                </div>
                            </div>
                        </div>
                        <button class="btn btn-outline" style="width:100%; margin-top:16px; font-size:13px;">Ver CRM Completo</button>
                    </div>
                </div>

                <!-- 4. ADVANCED CAMPAIGN PERFORMANCE -->
                <div class="metric-card-hover stagger-4" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm); margin-bottom: 24px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px;">
                        <h3 style="color: var(--text-main); font-size: 18px; margin:0;"><i class="fa-solid fa-wand-magic-sparkles" style="color:var(--accent-violet); margin-right:8px;"></i>Rendimiento de Campañas (Motor IA)</h3>
                        <div style="display:flex; gap:8px;">
                            <span style="background:rgba(16, 185, 129, 0.1); color:#10B981; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600;">+24% Eficiencia vs Correos Tradicionales</span>
                        </div>
                    </div>
                    
                    <div style="display:flex; flex-direction:column; gap:8px;">
                        <div style="display:grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr; align-items:center; padding:12px 16px; background:var(--bg-input); border-radius:8px; font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px;">
                            <div>Campaña (Push a Wallet)</div>
                            <div>Audiencia</div>
                            <div style="text-align:right;">Apertura</div>
                            <div style="text-align:right;">Conversión</div>
                            <div style="text-align:right;">Retorno ($)</div>
                        </div>
                        
                        <div class="table-row-hover" style="display:grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr; align-items:center; padding:16px; border-bottom:1px solid var(--border-glass); border-radius:8px; font-size:14px;">
                            <div><div style="font-weight:700; color:var(--text-main); margin-bottom:4px;">Recuperación (Churn Risk)</div><div style="font-size:12px; color:var(--text-muted);"><span style="background:var(--bg-input); padding:2px 6px; border-radius:4px;"><i class="fa-solid fa-tag"></i> Doble Cashback</span></div></div>
                            <div><div style="font-size:13px; font-weight:600;">340 clientes</div><div style="font-size:11px; color:var(--text-muted);">Sin visita en >45 días</div></div>
                            <div style="text-align:right;">
                                <div style="font-weight:700;">68%</div>
                                <div style="width:100%; height:4px; background:var(--bg-input); border-radius:2px; margin-top:4px; overflow:hidden;"><div style="width:68%; height:100%; background:var(--accent-cyan);"></div></div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-weight:700; color:var(--accent-emerald);">14.2%</div>
                                <div style="font-size:11px; color:var(--text-muted);">48 regresaron</div>
                            </div>
                            <div style="text-align:right; font-weight:800; color:var(--text-main); font-size:16px;">$12,400</div>
                        </div>
                        
                        <div class="table-row-hover" style="display:grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr; align-items:center; padding:16px; border-bottom:1px solid var(--border-glass); border-radius:8px; font-size:14px;">
                            <div><div style="font-weight:700; color:var(--text-main); margin-bottom:4px;">Cumpleaños (Agosto)</div><div style="font-size:12px; color:var(--text-muted);"><span style="background:var(--bg-input); padding:2px 6px; border-radius:4px;"><i class="fa-solid fa-cake-candles"></i> Cortesía Sorpresa</span></div></div>
                            <div><div style="font-size:13px; font-weight:600;">85 clientes</div><div style="font-size:11px; color:var(--text-muted);">Cumplen este mes</div></div>
                            <div style="text-align:right;">
                                <div style="font-weight:700;">85%</div>
                                <div style="width:100%; height:4px; background:var(--bg-input); border-radius:2px; margin-top:4px; overflow:hidden;"><div style="width:85%; height:100%; background:var(--accent-cyan);"></div></div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-weight:700; color:var(--accent-emerald);">42.5%</div>
                                <div style="font-size:11px; color:var(--text-muted);">36 redimieron</div>
                            </div>
                            <div style="text-align:right; font-weight:800; color:var(--text-main); font-size:16px;">$5,800</div>
                        </div>
                        
                        <div class="table-row-hover" style="display:grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr; align-items:center; padding:16px; border-radius:8px; font-size:14px;">
                            <div><div style="font-weight:700; color:var(--text-main); margin-bottom:4px;">Promoción Días Lentos</div><div style="font-size:12px; color:var(--text-muted);"><span style="background:var(--bg-input); padding:2px 6px; border-radius:4px;"><i class="fa-solid fa-clock"></i> Upgrade a VIP (4-7pm)</span></div></div>
                            <div><div style="font-size:13px; font-weight:600;">Todos los Activos</div><div style="font-size:11px; color:var(--text-muted);">Lanzado Martes</div></div>
                            <div style="text-align:right;">
                                <div style="font-weight:700;">52%</div>
                                <div style="width:100%; height:4px; background:var(--bg-input); border-radius:2px; margin-top:4px; overflow:hidden;"><div style="width:52%; height:100%; background:var(--accent-cyan);"></div></div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-weight:700; color:var(--accent-emerald);">8.1%</div>
                                <div style="font-size:11px; color:var(--text-muted);">80 aprovecharon</div>
                            </div>
                            <div style="text-align:right; font-weight:800; color:var(--text-main); font-size:16px;">$3,200</div>
                        </div>
                    </div>
                </div>

                <!-- 5. BOTTOM CHARTS ROW -->
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px;" class="stagger-5">
                    <!-- MAIN SALES CHART -->
                    <div class="metric-card-hover" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px;">
                            <h3 style="color: var(--text-main); font-size: 18px; margin:0;"><i class="fa-solid fa-chart-area" style="color:var(--accent-violet); margin-right:8px;"></i>Adquisición vs Retención de Ventas</h3>
                            <div style="font-size:12px; color:var(--text-muted); display:flex; gap:16px;">
                                <span><i class="fa-solid fa-circle" style="color:var(--accent-violet); font-size:8px; margin-right:4px;"></i> Retenidas (Lealtad)</span>
                                <span><i class="fa-solid fa-circle" style="color:var(--bg-input); font-size:8px; margin-right:4px;"></i> Nuevas (1era vez)</span>
                            </div>
                        </div>
                        <div style="height: 250px; background: repeating-linear-gradient(0deg, transparent, transparent 49px, var(--border-glass) 49px, var(--border-glass) 50px); display:flex; align-items:flex-end; gap:24px; padding-top:20px; padding-bottom:0; overflow:hidden;">
                            <!-- Animated Chart Bars -->
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div class="bento-chart-bar" style="width:40%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 30%;"></div>
                                <div class="bento-chart-bar" style="width:60%; background: linear-gradient(to top, var(--accent-violet), #7e22ce); border-radius: 6px 6px 0 0; height: 45%;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Ene</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div class="bento-chart-bar" style="width:40%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 28%; animation-delay:0.1s;"></div>
                                <div class="bento-chart-bar" style="width:60%; background: linear-gradient(to top, var(--accent-violet), #7e22ce); border-radius: 6px 6px 0 0; height: 52%; animation-delay:0.1s;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Feb</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div class="bento-chart-bar" style="width:40%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 35%; animation-delay:0.2s;"></div>
                                <div class="bento-chart-bar" style="width:60%; background: linear-gradient(to top, var(--accent-violet), #7e22ce); border-radius: 6px 6px 0 0; height: 60%; animation-delay:0.2s;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Mar</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div class="bento-chart-bar" style="width:40%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 32%; animation-delay:0.3s;"></div>
                                <div class="bento-chart-bar" style="width:60%; background: linear-gradient(to top, var(--accent-violet), #7e22ce); border-radius: 6px 6px 0 0; height: 75%; animation-delay:0.3s;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Abr</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div class="bento-chart-bar" style="width:40%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 40%; animation-delay:0.4s;"></div>
                                <div class="bento-chart-bar" style="width:60%; background: linear-gradient(to top, var(--accent-violet), #7e22ce); border-radius: 6px 6px 0 0; height: 95%; box-shadow: 0 0 20px rgba(76,29,149,0.4); animation-delay:0.4s;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:800; color:var(--accent-violet);">May</div>
                            </div>
                            <div style="flex:1; display:flex; align-items:flex-end; gap:4px; position:relative; height:100%;">
                                <div class="bento-chart-bar" style="width:40%; background: var(--bg-input); border-radius: 6px 6px 0 0; height: 38%; animation-delay:0.5s;"></div>
                                <div class="bento-chart-bar" style="width:60%; background: linear-gradient(to top, var(--accent-violet), #7e22ce); border-radius: 6px 6px 0 0; height: 85%; animation-delay:0.5s;"></div>
                                <div style="position:absolute; bottom:-25px; width:100%; text-align:center; font-size:11px; font-weight:600; color:var(--text-muted);">Jun</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- REWARDS DISTRIBUTION -->
                    <div class="metric-card-hover" style="background: white; padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-glass); box-shadow: var(--shadow-sm); display:flex; flex-direction:column;">
                        <h3 style="margin-bottom: 24px; color: var(--text-main); font-size: 18px;"><i class="fa-solid fa-gift" style="color:var(--accent-emerald); margin-right:8px;"></i>Premios Más Solicitados</h3>
                        
                        <div style="flex:1; display:flex; flex-direction:column; gap:20px; justify-content:center;">
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:13px; font-weight:700; color:var(--text-main);">
                                    <span><i class="fa-solid fa-money-bill-wave" style="color:#10B981; margin-right:6px;"></i> Cashback (Dinero Virtual)</span>
                                    <span>54%</span>
                                </div>
                                <div style="width:100%; height:12px; background:var(--bg-input); border-radius:6px; overflow:hidden; box-shadow:inset 0 1px 3px rgba(0,0,0,0.1);">
                                    <div style="width:54%; height:100%; background:linear-gradient(90deg, #10B981, #34D399); border-radius:6px; animation: progressFill 1s ease-out forwards;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:13px; font-weight:700; color:var(--text-main);">
                                    <span><i class="fa-solid fa-cake-candles" style="color:#F59E0B; margin-right:6px;"></i> Cortesía Cumpleaños</span>
                                    <span>28%</span>
                                </div>
                                <div style="width:100%; height:12px; background:var(--bg-input); border-radius:6px; overflow:hidden; box-shadow:inset 0 1px 3px rgba(0,0,0,0.1);">
                                    <div style="width:28%; height:100%; background:linear-gradient(90deg, #F59E0B, #FBBF24); border-radius:6px; animation: progressFill 1.2s ease-out forwards;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:13px; font-weight:700; color:var(--text-main);">
                                    <span><i class="fa-solid fa-crown" style="color:var(--accent-violet); margin-right:6px;"></i> Beneficio VIP (Fila Rápida)</span>
                                    <span>12%</span>
                                </div>
                                <div style="width:100%; height:12px; background:var(--bg-input); border-radius:6px; overflow:hidden; box-shadow:inset 0 1px 3px rgba(0,0,0,0.1);">
                                    <div style="width:12%; height:100%; background:linear-gradient(90deg, var(--accent-violet), #8B5CF6); border-radius:6px; animation: progressFill 1.4s ease-out forwards;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:13px; font-weight:700; color:var(--text-muted);">
                                    <span>Otros (Regalos Sorpresa)</span>
                                    <span>6%</span>
                                </div>
                                <div style="width:100%; height:12px; background:var(--bg-input); border-radius:6px; overflow:hidden; box-shadow:inset 0 1px 3px rgba(0,0,0,0.1);">
                                    <div style="width:6%; height:100%; background:linear-gradient(90deg, #9CA3AF, #D1D5DB); border-radius:6px; animation: progressFill 1.6s ease-out forwards;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </section>"""

pattern = r'<section id="tab-metrics" class="tab-content">.*?</section>'
html = re.sub(pattern, new_metrics_content, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
