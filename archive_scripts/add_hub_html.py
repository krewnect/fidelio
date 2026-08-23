import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

hub_html = """
    <!-- CAMPAIGN COMMAND CENTER MODAL -->
    <div id="modal-campaign-hub" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.8); z-index:9999; backdrop-filter:blur(10px); align-items:center; justify-content:center;">
        <div style="background:var(--bg-panel); width:90%; max-width:600px; border-radius:24px; overflow:hidden; position:relative; box-shadow:0 20px 50px rgba(0,0,0,0.5); transform:scale(0.95); animation: fadeInUp 0.3s forwards;">
            
            <!-- Header Background -->
            <div style="height:120px; background:linear-gradient(135deg, #2a0845 0%, #6441A5 100%); position:relative;">
                <button onclick="document.getElementById('modal-campaign-hub').style.display='none';" style="position:absolute; top:20px; right:20px; background:rgba(0,0,0,0.3); border:none; color:white; font-size:20px; width:36px; height:36px; border-radius:50%; cursor:pointer; backdrop-filter:blur(5px); display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <!-- Content -->
            <div style="padding:0 32px 32px; position:relative; margin-top:-40px;">
                
                <!-- Icon & Title -->
                <div style="display:flex; align-items:flex-end; gap:20px; margin-bottom:24px;">
                    <div id="hub-camp-icon" style="width:80px; height:80px; background:var(--bg-panel); border-radius:20px; display:flex; align-items:center; justify-content:center; font-size:36px; color:var(--accent-violet); box-shadow:0 10px 25px rgba(0,0,0,0.1); border:4px solid var(--bg-panel); z-index:2;">
                        <i class="fa-solid fa-star"></i>
                    </div>
                    <div style="padding-bottom:4px;">
                        <div id="hub-camp-type" style="font-size:12px; font-weight:800; color:var(--accent-violet); text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Tarjeta de Sellos</div>
                        <h2 id="hub-camp-name" style="font-size:28px; font-weight:800; color:var(--text-main); margin:0; line-height:1.1; letter-spacing:-0.5px;">Nombre de Campaña</h2>
                    </div>
                </div>

                <!-- Metrics Overview -->
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:32px;">
                    <div style="background:var(--bg-main); padding:20px; border-radius:16px; border:1px solid var(--border-glass);">
                        <div style="font-size:13px; color:var(--text-muted); font-weight:700; margin-bottom:8px;"><i class="fa-solid fa-qrcode" style="margin-right:6px;"></i> ESCANEOS TOTALES</div>
                        <div id="hub-stat-scans" style="font-size:32px; font-weight:800; color:var(--text-main); letter-spacing:-1px;">1,204</div>
                        <div style="font-size:12px; color:#10b981; font-weight:700; margin-top:4px;"><i class="fa-solid fa-arrow-trend-up"></i> +12% esta semana</div>
                    </div>
                    <div style="background:var(--bg-main); padding:20px; border-radius:16px; border:1px solid var(--border-glass);">
                        <div style="font-size:13px; color:var(--text-muted); font-weight:700; margin-bottom:8px;"><i class="fa-solid fa-gift" style="margin-right:6px;"></i> PREMIOS CANJEADOS</div>
                        <div id="hub-stat-rewards" style="font-size:32px; font-weight:800; color:var(--accent-violet); letter-spacing:-1px;">84</div>
                        <div style="font-size:12px; color:#10b981; font-weight:700; margin-top:4px;"><i class="fa-solid fa-arrow-trend-up"></i> +5% esta semana</div>
                    </div>
                </div>
                
                <hr style="border:none; border-top:1px dashed var(--border-glass); margin:0 0 24px 0;">

                <!-- Action Buttons -->
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                    <button id="hub-btn-edit" class="btn btn-primary hover-glow" style="padding:16px; border-radius:16px; font-size:16px; display:flex; flex-direction:column; align-items:center; gap:8px;">
                        <i class="fa-solid fa-wand-magic-sparkles" style="font-size:24px;"></i>
                        <span>Editar Reglas y Diseño</span>
                    </button>
                    <button id="hub-btn-push" class="btn hover-glow" style="background:var(--bg-main); color:var(--text-main); border:1px solid var(--border-glass); padding:16px; border-radius:16px; font-size:16px; display:flex; flex-direction:column; align-items:center; gap:8px;">
                        <i class="fa-solid fa-bullhorn" style="font-size:24px; color:#3b82f6;"></i>
                        <span>Lanzar Push Notificaton</span>
                    </button>
                </div>
                
                <div style="margin-top:16px; text-align:center;">
                    <button id="hub-btn-delete" style="background:none; border:none; color:#ef4444; font-size:14px; font-weight:700; cursor:pointer; padding:8px 16px; border-radius:8px; transition:background 0.2s;" onmouseover="this.style.background='rgba(239, 68, 68, 0.1)'" onmouseout="this.style.background='none'"><i class="fa-solid fa-trash" style="margin-right:6px;"></i> Eliminar Campaña</button>
                </div>

            </div>
        </div>
    </div>
"""

# Insert before </body>
html = html.replace('</body>', hub_html + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
