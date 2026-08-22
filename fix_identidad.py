import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

identidad_block = """
                            <p style="font-size: 15px; color: #64748b; margin-top: 8px; line-height: 1.5;">Configura la tarjeta digital Wallet de tu negocio. Todos los cambios se reflejan al instante en la vista previa derecha.</p>

                            <!-- AI COPILOT BANNER -->
                            <div style="background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(59,130,246,0.1)); border: 1px solid rgba(139,92,246,0.3); border-radius: 16px; padding: 24px; margin-top: 20px; display: flex; flex-direction: column; gap: 12px; position: relative; overflow: hidden;">
                                <div style="position: absolute; top: -20px; right: -20px; font-size: 80px; opacity: 0.1; filter: grayscale(1);">🤖</div>
                                <h3 style="margin:0; font-size: 16px; font-weight: 800; color: #4c1d95; display:flex; align-items:center; gap:8px;">
                                    <i class="fa-solid fa-wand-magic-sparkles" style="color: #8b5cf6;"></i> Diseñar con Inteligencia Artificial
                                </h3>
                                <p style="margin:0; font-size: 13px; color: #475569; line-height: 1.5;">Llena los datos básicos de Identidad y presiona el botón. Gemini analizará tu industria y generará la estrategia de lealtad, premio y colores perfectos para tu negocio en segundos.</p>
                                <button type="button" onclick="if(window.triggerRealAIMagicDesign) window.triggerRealAIMagicDesign()" style="background: linear-gradient(135deg, #8b5cf6, #6d28d9); color: white; border: none; padding: 12px 20px; border-radius: 10px; font-weight: 700; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 15px rgba(139,92,246,0.4); transition: transform 0.2s;">
                                    <i class="fa-solid fa-brain"></i> Estratega IA (Gemini)
                                </button>
                            </div>
                            
                            </div>

                        <!-- 1. IDENTIDAD -->
                        <div class="apple-section">
                            <div class="apple-section-header"><i class="fa-solid fa-store"></i> 1. Identidad de Marca</div>
                            
                            <div class="apple-input-group">
                                <label class="apple-label">Nombre del Negocio / Especialista</label>
                                <input type="text" id="rest-name" class="apple-input" value="Mi Negocio" oninput="if(window.updatePassRender) window.updatePassRender()">
                            </div>
                            
                            <div style="display:flex; gap:16px;">
                                <div class="apple-input-group" style="flex:1;">
                                    <label class="apple-label">Categoría o Industria</label>
                                    <input type="text" id="business-category-input" class="apple-input" value="Cafetería" placeholder="Ej. Veterinaria, Spa...">
                                </div>
                                <div class="apple-input-group" style="flex:1;">
                                    <label class="apple-label">Ícono Decorativo</label>
                                    <select id="rest-icon" class="apple-input" onchange="if(window.updatePassRender) window.updatePassRender()">
                                        <option value="fa-star">Estrella (Clásico)</option>
                                        <option value="fa-mug-hot">Taza (Cafetería)</option>
                                        <option value="fa-scissors">Tijeras (Peluquería)</option>
                                        <option value="fa-dumbbell">Pesas (Gimnasio)</option>
                                        <option value="fa-paw">Huella (Veterinaria)</option>
                                        <option value="fa-heart">Corazón (Salud/Belleza)</option>
                                        <option value="fa-tooth">Diente (Dentista)</option>
                                    </select>
                                </div>
                            </div>
                        </div>
"""

target = r'<p style="font-size: 15px; color: #64748b; margin-top: 8px; line-height: 1\.5;">Configura la tarjeta digital Wallet de tu negocio\. Todos los cambios se reflejan al instante en la vista previa derecha\.</p>\s*</div>'
html = re.sub(target, identidad_block, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
