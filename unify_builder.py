import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Insert Reglas in tab-builder
target_sidebar = """                        <!-- 1. Información Básica -->
                        <div>
                            <div class="premium-section-title">Información Básica</div>"""

rules_html = """                        <!-- 0. Reglas de Fidelización (UNIFICADO) -->
                        <div style="background: rgba(139, 92, 246, 0.05); padding: 24px; border-radius: 16px; border: 1px dashed rgba(139, 92, 246, 0.3);">
                            <div class="premium-section-title" style="color: var(--accent-violet);">1. Reglas de Recompensa</div>
                            <p class="premium-section-desc">Define qué ganan tus clientes al guardar esta tarjeta.</p>
                            
                            <div style="display:flex; flex-direction:column; gap:16px;">
                                <div>
                                    <label class="premium-label">¿Qué premio van a ganar?</label>
                                    <input type="text" id="unified-reward" class="premium-input" placeholder="Ej: ¡Felicidades! Ganaste un Frappé Gratis." value="Felicidades, ganaste un premio" oninput="window.updateUnifiedReward(this.value)">
                                </div>
                                <div>
                                    <label class="premium-label">Instrucciones Breves</label>
                                    <input type="text" id="unified-desc" class="premium-input" placeholder="Ej: Acumula 10 sellos para ganar." value="Acumula visitas para ganar." oninput="window.updateUnifiedDesc(this.value)">
                                </div>
                            </div>
                        </div>
                        
                        <div class="premium-divider"></div>
                        
                        <!-- 1. Diseño y Branding -->
                        <div>
                            <div class="premium-section-title">2. Diseño y Branding</div>"""

html = html.replace(target_sidebar, rules_html)

# 2. Hide old tabs from Sidebar to eliminate confusion
target_sidebar_menu_1 = """                <button class="sidebar-btn nav-tab" data-tab="tab-loyalty">
                    <i class="fa-solid fa-gift"></i>
                    <span>Mis Campañas</span>
                </button>"""
html = html.replace(target_sidebar_menu_1, "<!-- Oculto para unificar UX -->")

target_sidebar_menu_2 = """                <button class="sidebar-btn nav-tab" data-tab="tab-builder">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                    <span>Diseño de Tarjeta</span>
                </button>"""
replacement_menu_2 = """                <button class="sidebar-btn nav-tab" data-tab="tab-builder">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                    <span>Creador de Tarjetas</span>
                </button>"""
html = html.replace(target_sidebar_menu_2, replacement_menu_2)

target_sidebar_menu_3 = """                <button class="sidebar-btn nav-tab plan-pro-only" data-tab="tab-special-cards">
                    <i class="fa-solid fa-address-card"></i>
                    <span>Tarjetas & Reglas</span>
                </button>"""
html = html.replace(target_sidebar_menu_3, "<!-- Oculto para unificar UX -->")


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
