import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

radar_css = """
                    /* RADAR DE FUGA CSS */
                    @keyframes radarPing {
                        0% { transform: scale(0.5); opacity: 0; }
                        50% { opacity: 1; }
                        100% { transform: scale(2.5); opacity: 0; }
                    }
                    @keyframes radarSpin {
                        from { transform: rotate(0deg); }
                        to { transform: rotate(360deg); }
                    }
                    .sonar-wrapper {
                        position: relative;
                        width: 100%;
                        height: 250px;
                        background: radial-gradient(circle, #1e293b 0%, #0f172a 100%);
                        border-radius: 20px;
                        overflow: hidden;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 2px solid #334155;
                        box-shadow: inset 0 0 40px rgba(0,0,0,0.5);
                        margin-bottom: 30px;
                    }
                    .sonar-grid {
                        position: absolute;
                        width: 100%;
                        height: 100%;
                        background-image: 
                            linear-gradient(rgba(56, 189, 248, 0.1) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(56, 189, 248, 0.1) 1px, transparent 1px);
                        background-size: 20px 20px;
                    }
                    .sonar-circles {
                        position: absolute;
                        width: 200px; height: 200px;
                        border: 1px solid rgba(56, 189, 248, 0.2);
                        border-radius: 50%;
                    }
                    .sonar-circles::before {
                        content: ''; position: absolute; top: 25px; left: 25px; right: 25px; bottom: 25px;
                        border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 50%;
                    }
                    .sonar-circles::after {
                        content: ''; position: absolute; top: 60px; left: 60px; right: 60px; bottom: 60px;
                        border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 50%;
                    }
                    .sonar-sweeper {
                        position: absolute;
                        width: 100px; height: 100px;
                        background: conic-gradient(from 0deg, transparent 70%, rgba(56, 189, 248, 0.4) 100%);
                        border-radius: 50%;
                        transform-origin: bottom right;
                        top: 25px; left: 0;
                        animation: radarSpin 4s linear infinite;
                    }
                    .red-dot {
                        position: absolute;
                        width: 12px; height: 12px;
                        background: #ef4444;
                        border-radius: 50%;
                        box-shadow: 0 0 10px #ef4444, 0 0 20px #ef4444;
                        animation: pulseGlow 1s infinite alternate;
                        cursor: pointer;
                        transition: transform 0.2s;
                        z-index: 10;
                    }
                    .red-dot:hover { transform: scale(1.5); }
                    .red-dot::after {
                        content: '';
                        position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                        border: 2px solid #ef4444; border-radius: 50%;
                        animation: radarPing 2s infinite;
                    }
"""

html = html.replace('/* MAGICAL ANIMATIONS & MICRO-INTERACTIONS */', radar_css + '\n                    /* MAGICAL ANIMATIONS & MICRO-INTERACTIONS */')

radar_ui = """
                <!-- RADAR DE FUGA -->
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <h3 style="margin:0; font-size:16px; font-weight:800; color:#0f172a;"><i class="fa-solid fa-satellite-dish" style="color:#ef4444;"></i> Radar de Fuga (Riesgo de Churn)</h3>
                    <div style="font-size:12px; color:#64748b; font-weight:600;"><span style="display:inline-block; width:8px; height:8px; background:#ef4444; border-radius:50%; box-shadow: 0 0 5px #ef4444;"></span> 3 Clientes Inactivos detectados</div>
                </div>
                <div class="sonar-wrapper">
                    <div class="sonar-grid"></div>
                    <div class="sonar-circles"></div>
                    <div class="sonar-sweeper"></div>
                    
                    <!-- Fleeing Customers (Dots) -->
                    <div class="red-dot" style="top: 30%; left: 40%;" onclick="alert('Cliente: Maria G.\\nÚltima visita: Hace 45 días.\\n¡Lanzando Push Notification de Rescate!')"></div>
                    <div class="red-dot" style="top: 60%; left: 70%;" onclick="alert('Cliente: Juan P.\\nÚltima visita: Hace 60 días.\\n¡Lanzando Push Notification de Rescate!')"></div>
                    <div class="red-dot" style="top: 20%; left: 65%;" onclick="alert('Cliente: Sofia L.\\nÚltima visita: Hace 32 días.\\n¡Lanzando Push Notification de Rescate!')"></div>
                    
                    <div style="position: absolute; bottom: 16px; right: 16px;">
                        <button onclick="if(typeof showToast==='function') showToast('Lanzando 3 salvavidas por Push Notification...', 'success');" style="background:#ef4444; color:white; border:none; padding:10px 16px; border-radius:20px; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:8px; box-shadow:0 4px 15px rgba(239, 68, 68, 0.4);">
                            <i class="fa-solid fa-life-ring"></i> Lanzar Salvavidas
                        </button>
                    </div>
                </div>
"""

target_radar = r'<!-- KPI Dashboard -->[\s\S]*?</div>\s*</div>\s*</div>'
match = re.search(target_radar, html)
if match:
    html = html[:match.end()] + '\n' + radar_ui + html[match.end():]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
