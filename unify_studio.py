import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS
css_old = """                    /* Premium Clean Builder Redesigned */
                    .tab-builder-container { display: flex; height: calc(100vh - 100px); overflow: hidden; background: #ffffff; margin: -24px; }
                    .builder-preview-area { flex: 1; display: flex; align-items: center; justify-content: center; position: relative; background: #f8fafc; height: 100%; overflow: hidden; }
                    .builder-sidebar { 
                        width: 50%; 
                        max-width: 650px; 
                        background: #ffffff; 
                        overflow-y: auto; 
                        padding: 50px 60px; 
                        display:flex; 
                        flex-direction:column; 
                        z-index:10; 
                        border-right: 1px solid rgba(0,0,0,0.05);
                        box-shadow: 10px 0 30px rgba(0,0,0,0.02);
                    }"""

css_new = """                    /* FIDELIO CARD STUDIO (CANVA STYLE) */
                    .tab-builder-container { display: grid; grid-template-columns: 280px 1fr 380px; height: calc(100vh - 100px); overflow: hidden; background: #0f172a; margin: -24px; }
                    
                    /* Left Column: Templates */
                    .builder-templates { background: #1e293b; overflow-y: auto; padding: 24px; border-right: 1px solid #334155; }
                    .template-card { background: #0f172a; border-radius: 12px; padding: 16px; margin-bottom: 16px; cursor: pointer; border: 2px solid transparent; transition: all 0.2s; }
                    .template-card:hover { border-color: #3b82f6; transform: translateY(-2px); }
                    .template-card img { width: 100%; border-radius: 8px; margin-bottom: 12px; }
                    .template-card h4 { color: white; font-size: 14px; margin: 0 0 4px 0; font-weight: 600; }
                    .template-card p { color: #94a3b8; font-size: 11px; margin: 0; }

                    /* Center Column: Canvas */
                    .builder-preview-area { flex: 1; display: flex; align-items: center; justify-content: center; position: relative; background: #0f172a; height: 100%; overflow: hidden; }
                    
                    /* Right Column: Tools */
                    .builder-sidebar { 
                        background: #1e293b; 
                        overflow-y: auto; 
                        padding: 24px; 
                        display:flex; 
                        flex-direction:column; 
                        z-index:10; 
                        border-left: 1px solid #334155;
                        color: white;
                    }
                    .builder-sidebar .apple-section { background: #0f172a; border-color: #334155; }
                    .builder-sidebar .apple-label { color: #94a3b8; }
                    .builder-sidebar .fidelio-input { background: #1e293b; border-color: #334155; color: white; }
                    .builder-sidebar .fidelio-input:focus { border-color: #3b82f6; background: #0f172a; }
                    
                    /* Tools Tabs */
                    .tools-tabs { display: flex; gap: 8px; margin-bottom: 24px; background: #0f172a; padding: 4px; border-radius: 8px; }
                    .tool-tab { flex: 1; text-align: center; padding: 8px; color: #94a3b8; font-size: 12px; font-weight: 600; cursor: pointer; border-radius: 6px; }
                    .tool-tab.active { background: #3b82f6; color: white; }
                    .tool-content { display: none; }
                    .tool-content.active { display: block; }
                    
                    /* Material Buttons */
                    .material-btn { background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 16px; cursor: pointer; text-align: left; transition: all 0.2s; display: flex; align-items: center; gap: 16px; margin-bottom: 12px; }
                    .material-btn:hover { border-color: #3b82f6; background: #1e293b; }
                    .material-icon { width: 40px; height: 40px; border-radius: 8px; }
                    .material-glass { background: linear-gradient(135deg, rgba(255,255,255,0.4), rgba(255,255,255,0.1)); backdrop-filter: blur(10px); }
                    .material-titanium { background: linear-gradient(135deg, #cbd5e1, #94a3b8, #64748b); }
                    .material-neon { background: #000; box-shadow: inset 0 0 10px #ec4899; }
                    
                    /* Drag and Drop Overlays */
                    .drag-active .iphone-screen::before { content: 'Suelta tu logo aquí'; position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(59, 130, 246, 0.8); z-index: 9999; color: white; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; text-align: center; border-radius: 43px; border: 4px dashed white; box-sizing: border-box; }
"""

html = html.replace(css_old, css_new)

# 2. Restructure HTML inside tab-builder-container
# Find the start of builder-sidebar and builder-preview-area
# We need to extract the exact HTML of builder-sidebar and put it into the new tools tab "Modo Experto"
# And we need to add the Left column.

import sys
start_sidebar = html.find('<div class="builder-sidebar">')
if start_sidebar == -1:
    print("Cannot find builder-sidebar")
    sys.exit(1)

start_preview = html.find('<div class="builder-preview-area">')
if start_preview == -1:
    print("Cannot find builder-preview-area")
    sys.exit(1)

end_preview = html.find('</div> <!-- /builder-preview-area -->')
if end_preview == -1:
    # Try finding next closing div
    # Actually just assume it's right before </section>
    end_builder = html.find('</section>', start_preview)
    pass

# We'll just replace everything inside <div class="tab-builder-container">
container_start = html.find('<div class="tab-builder-container">')
section_end = html.find('</section>', container_start)

old_container_content = html[container_start:section_end]

# Extract the inner contents of builder-sidebar and builder-preview-area
# to reuse the inputs
sidebar_content = old_container_content[old_container_content.find('<div class="builder-sidebar">')+len('<div class="builder-sidebar">') : old_container_content.find('</div>', old_container_content.rfind('<button id="btn-save-design-push"')) + 6]
preview_content = old_container_content[old_container_content.find('<div class="builder-preview-area">')+len('<div class="builder-preview-area">') : old_container_content.find('</div> <!-- /builder-preview-area -->')]
if preview_content == "": # fallback
    preview_content = old_container_content[old_container_content.find('<div class="builder-preview-area">')+len('<div class="builder-preview-area">') : old_container_content.rfind('</div>', 0, old_container_content.rfind('</div>'))]

new_container_html = f"""<div class="tab-builder-container">
    
    <!-- COL 1: GALERÍA DE PLANTILLAS -->
    <div class="builder-templates">
        <h3 style="color: white; font-size: 16px; font-weight: 700; margin-bottom: 24px;"><i class="fa-solid fa-palette"></i> Plantillas Mágicas</h3>
        
        <div class="template-card" onclick="applyTemplate('luxury')">
            <div style="height: 100px; background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 8px; margin-bottom: 12px; display:flex; align-items:center; justify-content:center; border: 1px solid #334155;">
                <i class="fa-solid fa-plane-departure" style="color: #fbbf24; font-size: 24px;"></i>
            </div>
            <h4>Aerolínea Lujo (Titanio)</h4>
            <p>Tonos oscuros, metales y dorados para membresías VIP.</p>
        </div>
        
        <div class="template-card" onclick="applyTemplate('neon')">
            <div style="height: 100px; background: #000; box-shadow: inset 0 0 20px #ec4899; border-radius: 8px; margin-bottom: 12px; display:flex; align-items:center; justify-content:center; border: 1px solid #831843;">
                <i class="fa-solid fa-dumbbell" style="color: #ec4899; font-size: 24px;"></i>
            </div>
            <h4>Gimnasio Neón</h4>
            <p>Estética Cyberpunk, negro intenso y brillos fucsia.</p>
        </div>
        
        <div class="template-card" onclick="applyTemplate('minimal')">
            <div style="height: 100px; background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); border-radius: 8px; margin-bottom: 12px; display:flex; align-items:center; justify-content:center;">
                <i class="fa-solid fa-mug-hot" style="color: #3b82f6; font-size: 24px;"></i>
            </div>
            <h4>Cafetería Minimalista</h4>
            <p>Cristal esmerilado limpio (Glassmorphism).</p>
        </div>
    </div>

    <!-- COL 2: LIENZO (CANVAS) -->
    <div class="builder-preview-area" id="builder-canvas" ondragover="event.preventDefault(); this.classList.add('drag-active');" ondragleave="this.classList.remove('drag-active');" ondrop="handleLogoDrop(event)">
        {preview_content}
        
        <!-- Canvas Controls -->
        <div style="position: absolute; right: 40px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 16px;">
            <button onclick="document.getElementById('pass-render').style.transform = 'rotateY(0deg)'" title="Ver Frente" style="width: 48px; height: 48px; border-radius: 50%; background: #1e293b; color: white; border: 1px solid #334155; cursor: pointer; transition: all 0.2s;"><i class="fa-solid fa-mobile-screen"></i></button>
            <button onclick="document.getElementById('pass-render').style.transform = 'rotateY(180deg)'" title="Ver Reverso" style="width: 48px; height: 48px; border-radius: 50%; background: #1e293b; color: white; border: 1px solid #334155; cursor: pointer; transition: all 0.2s;"><i class="fa-solid fa-qrcode"></i></button>
            <button onclick="document.getElementById('magic-shape-select').value='event_ticket'; document.getElementById('magic-shape-select').dispatchEvent(new Event('change'));" title="Forma de Boleto" style="width: 48px; height: 48px; border-radius: 50%; background: #1e293b; color: white; border: 1px solid #334155; cursor: pointer; transition: all 0.2s;"><i class="fa-solid fa-ticket"></i></button>
        </div>
    </div>

    <!-- COL 3: ARSENAL MÁGICO (TOOLS) -->
    <div class="builder-sidebar">
        
        <div class="tools-tabs">
            <div class="tool-tab active" onclick="switchToolTab('materiales')"><i class="fa-solid fa-gem"></i> Estilos</div>
            <div class="tool-tab" onclick="switchToolTab('gamificacion')"><i class="fa-solid fa-gamepad"></i> Elementos</div>
            <div class="tool-tab" onclick="switchToolTab('experto')"><i class="fa-solid fa-gear"></i> Modo Dios</div>
        </div>
        
        <!-- Pestaña 1: Estilos / Materiales 3D -->
        <div id="tab-materiales" class="tool-content active">
            <h3 style="font-size: 14px; margin-bottom: 16px; font-weight: 700;">Materiales Apple Wallet (CSS 3D)</h3>
            <p style="font-size: 11px; color: #94a3b8; margin-bottom: 24px;">Transforma el diseño plano en objetos fotorrealistas al instante.</p>
            
            <div class="material-btn" onclick="applyMaterial('glass')">
                <div class="material-icon material-glass"></div>
                <div>
                    <h4 style="margin:0; font-size:14px; font-weight:600;">Cristal Esmerilado</h4>
                    <p style="margin:0; font-size:11px; color:#94a3b8;">Glassmorphism translúcido</p>
                </div>
            </div>
            
            <div class="material-btn" onclick="applyMaterial('titanium')">
                <div class="material-icon material-titanium"></div>
                <div>
                    <h4 style="margin:0; font-size:14px; font-weight:600;">Titanio Cepillado</h4>
                    <p style="margin:0; font-size:11px; color:#94a3b8;">Gradients metálicos Apple Pro</p>
                </div>
            </div>
            
            <div class="material-btn" onclick="applyMaterial('neon')">
                <div class="material-icon material-neon"></div>
                <div>
                    <h4 style="margin:0; font-size:14px; font-weight:600;">Cyberpunk Neón</h4>
                    <p style="margin:0; font-size:11px; color:#94a3b8;">Luz glow brillante y alto contraste</p>
                </div>
            </div>
        </div>
        
        <!-- Pestaña 2: Gamificación -->
        <div id="tab-gamificacion" class="tool-content">
            <h3 style="font-size: 14px; margin-bottom: 16px; font-weight: 700;">Elementos Interactivos</h3>
            <p style="font-size: 11px; color: #94a3b8; margin-bottom: 24px;">(Próximamente) Arrastra estos componentes al Canvas.</p>
            
            <div style="background: #0f172a; border: 1px dashed #334155; padding: 16px; border-radius: 8px; text-align: center; margin-bottom: 12px; cursor: grab;">
                <i class="fa-solid fa-gift" style="font-size: 24px; color: #8b5cf6; margin-bottom: 8px;"></i>
                <h4 style="margin:0; font-size:12px; color:white;">Caja Botín (Loot Box)</h4>
            </div>
            <div style="background: #0f172a; border: 1px dashed #334155; padding: 16px; border-radius: 8px; text-align: center; margin-bottom: 12px; cursor: grab;">
                <i class="fa-solid fa-water" style="font-size: 24px; color: #3b82f6; margin-bottom: 8px;"></i>
                <h4 style="margin:0; font-size:12px; color:white;">Barra Líquida</h4>
            </div>
        </div>
        
        <!-- Pestaña 3: Modo Dios (Formularios Viejos) -->
        <div id="tab-experto" class="tool-content">
            <h3 style="font-size: 14px; margin-bottom: 16px; font-weight: 700; color: #ef4444;"><i class="fa-solid fa-bolt"></i> Ajustes Avanzados</h3>
            <p style="font-size: 11px; color: #94a3b8; margin-bottom: 24px;">Configuración profunda del motor para usuarios técnicos.</p>
            
            <div style="display: none;">
                {sidebar_content.replace('display: none;', 'display: block;').replace('class="apple-section"', 'class="apple-section" style="margin-bottom: 16px;"')}
            </div>
            
            <button onclick="document.querySelector('#tab-experto > div').style.display = 'block'; this.style.display='none';" class="fidelio-btn-primary" style="background: #1e293b !important; color: white !important; border: 1px solid #334155 !important;">
                Mostrar Código Genético de la Tarjeta
            </button>
        </div>
        
    </div>
</div>
"""

html = html.replace(old_container_content, new_container_html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated HTML structure.")
