import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

modal_html = """
    <!-- QUICK CAMPAIGN WIZARD MODAL -->
    <div id="modal-quick-campaign" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.8); z-index:9999; backdrop-filter:blur(10px); align-items:center; justify-content:center;">
        <div style="background:var(--bg-body); width:90%; max-width:700px; border-radius:24px; padding:40px; position:relative; box-shadow:0 20px 50px rgba(0,0,0,0.5); transform:scale(0.95); transition:transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); animation: fadeInUp 0.4s forwards;">
            <button onclick="document.getElementById('modal-quick-campaign').style.display='none';" style="position:absolute; top:20px; right:20px; background:transparent; border:none; color:var(--text-muted); font-size:24px; cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            
            <div style="text-align:center; margin-bottom:32px;">
                <h2 style="font-size:28px; font-weight:800; margin-bottom:8px; background:linear-gradient(135deg, var(--accent-violet) 0%, #3b82f6 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">¡Crea tu Campaña en Segundos!</h2>
                <p style="color:var(--text-muted); font-size:16px;">Olvídate de las configuraciones tediosas. Elige una plantilla pre-armada que se adapte a tu negocio y la inteligencia de Fidelio configurará todo por ti al instante.</p>
            </div>
            
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:20px;">
                <!-- Plantilla Cafetería -->
                <div class="content-panel hover-glow" onclick="applyQuickTemplate('cafeteria')" style="background:var(--surface); border:1px solid var(--border-soft); border-radius:16px; padding:24px; text-align:center; cursor:pointer; transition:all 0.2s;">
                    <div style="width:60px; height:60px; border-radius:50%; background:rgba(245,158,11,0.1); color:#f59e0b; display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 16px;">
                        <i class="fa-solid fa-mug-hot"></i>
                    </div>
                    <h4 style="margin:0 0 8px; font-size:18px;">Cafés y Restaurantes</h4>
                    <p style="margin:0; font-size:12px; color:var(--text-muted);">Tarjeta de 10 Sellos. Bebida gratis. Colores cálidos.</p>
                </div>

                <!-- Plantilla Belleza -->
                <div class="content-panel hover-glow" onclick="applyQuickTemplate('salon')" style="background:var(--surface); border:1px solid var(--border-soft); border-radius:16px; padding:24px; text-align:center; cursor:pointer; transition:all 0.2s;">
                    <div style="width:60px; height:60px; border-radius:50%; background:rgba(236,72,153,0.1); color:#ec4899; display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 16px;">
                        <i class="fa-solid fa-scissors"></i>
                    </div>
                    <h4 style="margin:0 0 8px; font-size:18px;">Salón y Belleza</h4>
                    <p style="margin:0; font-size:12px; color:var(--text-muted);">Visitas frecuentes. Recompensa de servicio. Tonos pastel.</p>
                </div>

                <!-- Plantilla Salud -->
                <div class="content-panel hover-glow" onclick="applyQuickTemplate('clinica')" style="background:var(--surface); border:1px solid var(--border-soft); border-radius:16px; padding:24px; text-align:center; cursor:pointer; transition:all 0.2s;">
                    <div style="width:60px; height:60px; border-radius:50%; background:rgba(16,185,129,0.1); color:#10b981; display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 16px;">
                        <i class="fa-solid fa-stethoscope"></i>
                    </div>
                    <h4 style="margin:0 0 8px; font-size:18px;">Salud y Citas</h4>
                    <p style="margin:0; font-size:12px; color:var(--text-muted);">Control de citas. Descuento en consulta. Tonos médicos.</p>
                </div>

                <!-- Desde Cero -->
                <div class="content-panel hover-glow" onclick="applyQuickTemplate('custom')" style="background:var(--surface); border:1px dashed var(--border-soft); border-radius:16px; padding:24px; text-align:center; cursor:pointer; transition:all 0.2s;">
                    <div style="width:60px; height:60px; border-radius:50%; background:var(--bg-input); color:var(--text-muted); display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 16px;">
                        <i class="fa-solid fa-wand-magic-sparkles"></i>
                    </div>
                    <h4 style="margin:0 0 8px; font-size:18px;">Desde Cero</h4>
                    <p style="margin:0; font-size:12px; color:var(--text-muted);">Modo Experto. Configura todo manualmente paso a paso.</p>
                </div>
            </div>
            
            <div style="margin-top:24px; text-align:center; display:none;" id="quick-wizard-loading">
                <i class="fa-solid fa-spinner fa-spin" style="color:var(--accent-violet); font-size:32px;"></i>
                <p style="margin-top:12px; font-weight:600; color:var(--text-main);">Construyendo la magia...</p>
            </div>
        </div>
    </div>
"""

# Inject before </body>
html = html.replace('</body>', modal_html + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
