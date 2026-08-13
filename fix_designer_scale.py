import re

with open('index.html', 'r') as f:
    html = f.read()

new_tab_content = """<section id="tab-builder" class="tab-content">
                <style>
                    /* Premium Clean Builder */
                    .tab-builder-container { display: flex; height: calc(100vh - 100px); overflow: hidden; background: #fafafa; margin: -24px; }
                    .builder-sidebar { width: 420px; background: white; border-right: 1px solid var(--border-glass); overflow-y: auto; padding: 32px; display:flex; flex-direction:column; gap:24px; box-shadow: 10px 0 30px rgba(0,0,0,0.02); z-index:10; }
                    .builder-preview-area { flex: 1; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle at center, #f3f4f6 0%, #e5e7eb 100%); position: relative; overflow: hidden; }
                    
                    .premium-label { font-size: 13px; font-weight: 600; color: #374151; margin-bottom: 8px; display: block; }
                    .premium-input { width: 100%; padding: 12px 16px; border: 1px solid #d1d5db; border-radius: 8px; font-family: var(--font-main); font-size: 14px; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
                    .premium-input:focus { outline: none; border-color: var(--accent-violet); box-shadow: 0 0 0 3px rgba(76,29,149,0.1); }
                    
                    .premium-section-title { font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 4px; letter-spacing:-0.5px; }
                    .premium-section-desc { font-size: 13px; color: #6b7280; margin-bottom: 20px; line-height: 1.4; }
                    .premium-divider { height: 1px; background: #e5e7eb; margin: 8px 0; }
                    
                    /* iPhone Realistic Mockup - Thin Bezel, Focus on Card */
                    .iphone-device.premium-mockup { width: 375px; height: 812px; background: #000; border: 6px solid #1a1a1a; box-shadow: 0 50px 100px rgba(0,0,0,0.3), inset 0 0 4px rgba(255,255,255,0.2); border-radius: 44px; display:flex; flex-direction:column; position:relative; overflow:hidden; transform: scale(0.85); transform-origin: center; transition: all 0.3s ease; }
                    
                    /* Make slightly larger on big screens, but never gigantic */
                    @media (min-width: 1400px) { .iphone-device.premium-mockup { transform: scale(0.95); } }
                    
                    .premium-mockup .dynamic-island { background: #000; border-radius: 20px; height: 28px; width: 100px; position: absolute; top: 12px; left: 50%; transform: translateX(-50%); z-index: 100; box-shadow: inset 0 -1px 1px rgba(255,255,255,0.1); }
                    .premium-mockup .iphone-screen { flex: 1; border-radius: 38px; background: #000; overflow: hidden; position: relative; padding: 70px 16px 20px 16px; display:flex; flex-direction:column; align-items:center; }
                    
                    /* Card 3D Flip Mechanics restored but elegant */
                    .card-3d-scene { perspective: 1200px; width: 100%; flex:1; position: relative; z-index: 10; margin-bottom:10px; }
                    .card-3d-object { width: 100%; height: 100%; position: relative; transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); transform-style: preserve-3d; cursor:pointer; }
                    .card-3d-object.is-flipped { transform: rotateY(180deg); }
                    
                    .card-face { position: absolute; width: 100%; height: 95%; backface-visibility: hidden; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); display: flex; flex-direction: column; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }
                    
                    /* Front of Wallet Pass inside phone */
                    .card-front { background: white; }
                    .pass-top-section { padding: 20px 20px 16px 20px; color: white; background: linear-gradient(135deg, #1e1b4b, #8b5cf6); }
                    .pass-brand-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
                    .pass-logo-circle { width: 36px; height: 36px; background: rgba(0,0,0,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; color: white; border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(5px); }
                    
                    .pass-banner-img { width: 100%; height: 120px; object-fit: cover; background: rgba(0,0,0,0.1); }
                    .pass-body-section { flex: 1; background: white; padding: 20px; display: flex; flex-direction: column; }
                    .pass-field-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; font-weight: 600; margin-bottom: 4px; }
                    .pass-field-value { font-size: 18px; font-weight: 700; color: #111827; letter-spacing:-0.5px; }
                    .pass-qr-section { margin-top: auto; display: flex; flex-direction: column; align-items: center; padding-top: 16px; border-top: 1px dashed #e5e7eb; }
                    
                    /* Back of Wallet Pass */
                    .card-back { transform: rotateY(180deg); background: #1a1a1c; padding: 24px; color:white; overflow-y:auto; }
                    
                    /* Color Pickers */
                    .color-picker-wrapper { display:flex; gap:12px; align-items:center; }
                    .premium-color-input { -webkit-appearance: none; border: none; width: 40px; height: 40px; border-radius: 8px; cursor: pointer; padding: 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                    .premium-color-input::-webkit-color-swatch-wrapper { padding: 0; }
                    .premium-color-input::-webkit-color-swatch { border: none; border-radius: 8px; border: 2px solid white; box-shadow: 0 0 0 1px #e5e7eb; }
                </style>

                <div class="tab-builder-container">
                    <!-- LEFT SIDEBAR: CONTROLS -->
                    <div class="builder-sidebar">
                        <div>
                            <h1 style="font-size: 24px; font-weight: 800; letter-spacing: -1px; color: #111827;">Diseñador Wallet</h1>
                            <p style="font-size: 14px; color: #6b7280; margin-top: 8px;">Configura la tarjeta digital que tus clientes instalarán en sus teléfonos. Todo cambio se refleja al instante.</p>
                        </div>
                        
                        <div class="premium-divider"></div>
                        
                        <!-- 1. Identidad -->
                        <div>
                            <div class="premium-section-title">Identidad de Marca</div>
                            
                            <div style="display:flex; flex-direction:column; gap:16px;">
                                <div>
                                    <label class="premium-label">Nombre del Negocio</label>
                                    <input type="text" id="rest-name" class="premium-input" value="Mi Negocio">
                                </div>
                                <div>
                                    <label class="premium-label">Giro o Categoría (Opcional)</label>
                                    <input type="text" id="business-category-input" class="premium-input" value="Restaurante & Gastronomía" placeholder="Ej: Barbería, Spa...">
                                </div>
                            </div>
                        </div>
                        
                        <div class="premium-divider"></div>
                        
                        <!-- 2. Apariencia -->
                        <div>
                            <div class="premium-section-title">Apariencia Visual</div>
                            
                            <div style="display:flex; flex-direction:column; gap:16px;">
                                <div style="display:flex; gap:24px;">
                                    <div>
                                        <label class="premium-label">Color Principal</label>
                                        <div class="color-picker-wrapper">
                                            <input type="color" id="color-primary" class="premium-color-input" value="#1e1b4b">
                                        </div>
                                    </div>
                                    <div>
                                        <label class="premium-label">Color Secundario</label>
                                        <div class="color-picker-wrapper">
                                            <input type="color" id="color-accent" class="premium-color-input" value="#8b5cf6">
                                        </div>
                                    </div>
                                </div>
                                
                                <div>
                                    <label class="premium-label">Ícono (Temporal)</label>
                                    <select id="rest-icon" class="premium-input">
                                        <option value="fa-crown" selected>Corona (Premium)</option>
                                        <option value="fa-burger">Hamburguesa</option>
                                        <option value="fa-scissors">Tijeras</option>
                                        <option value="fa-mug-hot">Café</option>
                                        <option value="fa-spa">Spa / Flor</option>
                                    </select>
                                </div>
                                
                                <div>
                                    <label class="premium-label">Mensaje Corto (Promo)</label>
                                    <input type="text" id="rest-desc" class="premium-input" value="Martes Doble Cashback" maxlength="40">
                                </div>
                            </div>
                        </div>
                        
                        <div class="premium-divider"></div>
                        
                        <!-- 3. Beneficios -->
                        <div>
                            <div class="premium-section-title">Beneficios Visibles</div>
                            
                            <div style="display:flex; flex-direction:column; gap:16px;">
                                <div>
                                    <label class="premium-label">Siguiente Premio a Desbloquear</label>
                                    <input type="text" id="stamps-reward" class="premium-input" value="Bebida de Cortesía Gratis">
                                </div>
                                <div>
                                    <label class="premium-label">Términos Legales (Reverso)</label>
                                    <textarea id="pass-policies" class="premium-input" rows="3" style="resize:vertical;">Las recompensas no son transferibles ni canjeables por efectivo.</textarea>
                                </div>
                            </div>
                        </div>
                        
                        <div style="margin-top:auto; padding-top:24px;">
                            <button class="btn btn-primary" style="width:100%; justify-content:center; padding:16px; font-size:16px; border-radius:12px; background:#111827; border:none; color:white; font-weight:700;"><i class="fa-solid fa-cloud-arrow-up"></i> Guardar Diseño</button>
                        </div>
                    </div>
                    
                    <!-- RIGHT AREA: REALISTIC PHONE MOCKUP -->
                    <div class="builder-preview-area">
                        <!-- Floating Background Elements -->
                        <div style="position:absolute; top:-10%; left:-10%; width:50%; height:50%; background:radial-gradient(circle, rgba(139, 92, 246, 0.05) 0%, transparent 70%); pointer-events:none;"></div>
                        
                        <!-- REALISTIC PHONE -->
                        <div class="iphone-device premium-mockup">
                            <div class="dynamic-island"><div class="lens"></div></div>
                            <div class="iphone-screen">
                                
                                <div style="display:flex; justify-content:space-between; align-items:center; width:100%; margin-bottom:16px; z-index:20;">
                                    <div style="color:white; font-size:18px; font-weight:700; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-wallet"></i> Wallet</div>
                                    <button id="btn-flip-card" style="background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.2); color:white; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:700; cursor:pointer; backdrop-filter:blur(10px);"><i class="fa-solid fa-rotate-right"></i> Giro 3D</button>
                                </div>

                                <!-- THE PASS -->
                                <div class="card-3d-scene">
                                    <div class="card-3d-object" id="pass-render">
                                        
                                        <!-- Front of Card -->
                                        <div class="card-face card-front">
                                            <!-- Header Area -->
                                            <div class="pass-top-section" id="pass-front-face">
                                                <div class="pass-brand-row">
                                                    <div style="display: flex; align-items: center; gap: 10px;">
                                                        <div class="pass-logo-circle">
                                                            <i class="fa-solid fa-crown" id="render-icon"></i>
                                                        </div>
                                                        <div>
                                                            <div id="render-name" style="font-weight:700; font-size:16px; letter-spacing:-0.5px;">Mi Negocio</div>
                                                            <div id="render-category" style="font-size:11px; opacity:0.8; font-weight:500;">Restaurante & Gastronomía</div>
                                                        </div>
                                                    </div>
                                                </div>
                                                
                                                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                                                    <div>
                                                        <div style="font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Nivel Actual</div>
                                                        <div id="render-vip-caption" style="font-size:18px; font-weight:800; letter-spacing:-0.5px;">ORO VIP</div>
                                                    </div>
                                                    <div style="text-align:right;">
                                                        <div style="font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:2px;">Cashback</div>
                                                        <div style="font-size:18px; font-weight:800; letter-spacing:-0.5px;" id="render-balance">$145.00</div>
                                                    </div>
                                                </div>
                                            </div>
                                            
                                            <!-- Middle Image -->
                                            <div id="render-banner-container" style="background:#f9fafb;">
                                                <img id="render-banner-img" src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&q=80&w=800&h=300" alt="Banner" class="pass-banner-img">
                                            </div>
                                            
                                            <!-- Body Info -->
                                            <div class="pass-body-section">
                                                <div style="display:flex; gap:16px; margin-bottom:16px;">
                                                    <div style="flex:1;">
                                                        <div class="pass-field-label">Próxima Recompensa</div>
                                                        <div class="pass-field-value" style="font-size:14px; color:#10B981;" id="render-reward-text">Bebida de Cortesía Gratis</div>
                                                    </div>
                                                    <div style="text-align:right;">
                                                        <div class="pass-field-label">Visitas</div>
                                                        <div class="pass-field-value" style="font-size:14px;">3 / 5</div>
                                                    </div>
                                                </div>
                                                
                                                <div style="margin-bottom:16px;">
                                                    <div class="pass-field-label">Notificación Flash</div>
                                                    <div class="pass-field-value" style="font-size:13px; font-weight:600; background:#f3f4f6; padding:8px; border-radius:8px; display:inline-block; width:100%;">
                                                        <i class="fa-solid fa-bolt" style="color:#F59E0B; margin-right:6px;"></i> <span id="render-promo-text">Martes Doble Cashback</span>
                                                    </div>
                                                </div>
                                                
                                                <div class="pass-qr-section">
                                                    <img src="dummy_qr.png" alt="QR Code" style="width:100px; height:100px; mix-blend-mode:multiply; opacity:0.9;">
                                                    <div style="margin-top:8px; font-size:10px; font-weight:700; color:#9ca3af; letter-spacing:1px;">FIDELIO-8842-MEX</div>
                                                </div>
                                            </div>
                                        </div>

                                        <!-- Back of Card -->
                                        <div class="card-face card-back">
                                            <div style="background:rgba(255,255,255,0.1); padding:8px 12px; border-radius:12px; font-size:11px; font-weight:600; text-align:center; margin-bottom:20px; display:inline-block;">
                                                <i class="fa-brands fa-apple"></i> Apple Wallet &nbsp;|&nbsp; <i class="fa-brands fa-google"></i> Google Wallet
                                            </div>
                                            
                                            <h4 style="font-size:13px; color:#ddd; margin-bottom:6px;">Términos y Políticas Legales</h4>
                                            <p id="render-policies-text" style="font-size:11px; color:#999; line-height:1.5;">Las recompensas no son transferibles ni canjeables por efectivo.</p>
                                            
                                            <div style="width:100%; height:1px; background:#333; margin:20px 0;"></div>
                                            
                                            <h4 style="font-size:13px; color:#ddd; margin-bottom:6px;">Acerca de este Pase</h4>
                                            <p style="font-size:11px; color:#999; line-height:1.5;">Este pase digital está administrado por Fidelio Rewards. Cualquier modificación de saldo se refleja automáticamente mediante tecnología Push.</p>
                                        </div>

                                    </div>
                                </div>
                                
                                <div style="width:100%; display:flex; justify-content:center; padding-top:10px;">
                                    <div style="width:120px; height:4px; background:white; border-radius:2px;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>"""

pattern = r'<section id="tab-builder" class="tab-content">.*?</section>'
html = re.sub(pattern, new_tab_content, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
