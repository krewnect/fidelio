import re

with open('index.html', 'r') as f:
    html = f.read()

new_tab = """            <section id="tab-branches" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">CONFIGURACIÓN MULTISEDE</span>
                        <h1>Sucursales y Reseñas</h1>
                        <p>Geolocalización para Apple Wallet y motor de reseñas independiente por sucursal.</p>
                    </div>
                </div>
                
                <div class="accordion-card" style="max-width: 800px;">
                    <div class="card-title-bar" style="margin-bottom:16px; justify-content:space-between;">
                        <div style="display:flex; align-items:center; gap:16px;">
                            <div style="width:48px; height:48px; border-radius:12px; background:rgba(139, 92, 246, 0.1); display:flex; align-items:center; justify-content:center; color:var(--accent-violet); font-size:20px;">
                                <i class="fa-solid fa-map-location-dot"></i>
                            </div>
                            <div>
                                <h2 style="margin:0; font-size:20px;">Red de Sucursales</h2>
                                <p style="margin:0; font-size:13px; color:var(--text-muted);">Administra la información, responsables y enlaces de Google Maps de cada ubicación.</p>
                            </div>
                        </div>
                        <button class="btn btn-primary" id="btn-add-branch-modal" style="background:var(--text-main);"><i class="fa-solid fa-plus"></i> Añadir Sucursal</button>
                    </div>
                    
                    <div style="background:var(--bg-input); border-radius:16px; padding:24px; border:1px solid rgba(0,0,0,0.03);">
                        <div id="branches-list-container" style="display:flex; flex-direction:column; gap:12px;">
                            <p style="color:var(--text-muted); text-align:center; padding: 20px;"><i class="fa-solid fa-circle-notch fa-spin"></i> Cargando red de sucursales...</p>
                        </div>
                    </div>
                </div>
            </section>"""

pattern = r'<section id="tab-branches" class="tab-content">.*?</section>'
html = re.sub(pattern, new_tab, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
