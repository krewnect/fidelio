import re

with open('index.html', 'r') as f:
    html = f.read()

new_tab_content = """<section id="tab-builder" class="tab-content">
                <style>
                    /* 3D Card Physics */
                    .iphone-device.premium-mockup { background: #000; border: 12px solid #1f1f1f; box-shadow: 0 40px 80px rgba(0,0,0,0.5), inset 0 0 10px rgba(255,255,255,0.1); border-radius: 44px; padding: 20px; height: 720px; display:flex; flex-direction:column; position:relative; overflow:hidden; }
                    .premium-mockup .dynamic-island { background: #000; border-radius: 20px; height: 30px; width: 120px; position: absolute; top: 10px; left: 50%; transform: translateX(-50%); z-index: 100; box-shadow: inset 0 -1px 2px rgba(255,255,255,0.2); }
                    .premium-mockup .iphone-screen { flex: 1; border-radius: 32px; background: #09090b; overflow: hidden; position: relative; padding: 60px 20px 20px 20px; display:flex; flex-direction:column; }
                    
                    /* Apple Wallet Dark BG aesthetic */
                    .premium-mockup .iphone-screen::before { content: ''; position:absolute; top:0; left:0; width:100%; height:100%; background: radial-gradient(circle at top, rgba(76,29,149,0.2) 0%, transparent 60%); pointer-events:none; }

                    .card-3d-scene { perspective: 1200px; width: 100%; height: 500px; position: relative; z-index: 10; margin-top:20px; }
                    .card-3d-object { width: 100%; height: 100%; position: relative; transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform-style: preserve-3d; cursor:pointer; }
                    .card-3d-object.is-flipped { transform: rotateY(180deg) scale(1.05); }
                    
                    .card-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); overflow: hidden; border: 1px solid rgba(255,255,255,0.2); }
                    .card-back { transform: rotateY(180deg); background: #18181b; padding: 30px 24px; display:flex; flex-direction:column; align-items:center; border: 1px solid #333; }
                    
                    @keyframes sheenSweep { 0% { left: -100%; } 20% { left: 200%; } 100% { left: 200%; } }
                    .holographic-sheen { position: absolute; top: 0; left: -100%; width: 50%; height: 100%; background: linear-gradient(to right, transparent, rgba(255,255,255,0.4), transparent); transform: skewX(-20deg); animation: sheenSweep 6s infinite; pointer-events: none; mix-blend-mode: overlay; }
                    
                    /* Apple Wallet QR Style */
                    .qr-container-back { background:white; padding:12px; border-radius:12px; margin-top:20px; display:flex; align-items:center; justify-content:center; box-shadow:0 10px 20px rgba(0,0,0,0.2); width:160px; height:160px; }
                    
                    /* Apple Pay / NFC badge */
                    .nfc-badge { background:rgba(255,255,255,0.1); backdrop-filter:blur(10px); padding:8px 16px; border-radius:20px; display:inline-flex; align-items:center; gap:8px; font-size:12px; font-weight:600; color:white; border:1px solid rgba(255,255,255,0.1); margin-bottom:20px; }
                    
                    /* Interactive fields */
                    .editable-hover { transition: all 0.2s; border-radius:4px; padding:2px 4px; margin:-2px -4px; cursor:text; border:1px solid transparent; }
                    .editable-hover:hover { border-color:rgba(255,255,255,0.3); background:rgba(255,255,255,0.05); }
                </style>

                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">DISEÑADOR DE WALLET</span>
                        <h1>Construye tu Experiencia Premium</h1>
                        <p>Diseña la tarjeta digital 3D interactiva que vivirán tus clientes en Apple Wallet y Google Wallet.</p>
                    </div>
                </div>

                <div class="builder-split-grid">
                    <!-- CONTROLS -->
                    <div class="builder-controls-panel">
                        <form id="pass-config-form" onsubmit="return false;">
                            <!-- STEP 1 -->
                            <div class="accordion-card">
                                <div class="card-title-bar">
                                    <span class="card-step-badge">01</span>
                                    <h2>Información del Negocio</h2>
                                </div>
                                <div class="form-group">
                                    <label>Nombre Comercial</label>
                                    <input type="text" id="rest-name" value="Mi Negocio" class="fidelio-input">
                                </div>
                                <div class="form-group">
                                    <label>Categoría / Industria (Texto Libre)</label>
                                    <input type="text" id="business-category-input" list="category-suggestions" value="Restaurante & Gastronomía" class="fidelio-input" placeholder="Ej: Barbería, Spa, Gimnasio...">
                                    <datalist id="category-suggestions">
                                        <option value="Restaurantes & Gastronomía">
                                        <option value="Cafeterías & Panaderías">
                                        <option value="Barbershops & Estéticas">
                                        <option value="Boutiques & Retail">
                                        <option value="Salud & Spa">
                                        <option value="Gimnasios & Fitness">
                                        <option value="Hoteles & Hospitalidad">
                                    </datalist>
                                </div>
                                <div class="form-group">
                                    <label>Mensaje Flash (Visible al frente)</label>
                                    <input type="text" id="rest-desc" value="Martes y Jueves: Doble Cashback" class="fidelio-input">
                                </div>
                            </div>

                            <!-- STEP 2 -->
                            <div class="accordion-card">
                                <div class="card-title-bar">
                                    <span class="card-step-badge">02</span>
                                    <h2>Identidad Visual y Hologramas</h2>
                                </div>
                                <div class="form-row-2">
                                    <div class="form-group">
                                        <label>Logo / Ícono Frontal (PNG transparente)</label>
                                        <div class="file-dropzone" id="logo-dropzone">
                                            <input type="file" id="logo-file-input" accept="image/*">
                                            <i class="fa-solid fa-crown" style="font-size:24px; color:var(--accent-violet);"></i>
                                            <span style="font-size:12px; font-weight:600; margin-top:8px;">Subir Ícono</span>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label>Cover Trasero Opcional (JPG)</label>
                                        <div class="file-dropzone" id="banner-dropzone">
                                            <input type="file" id="banner-file-input" accept="image/*">
                                            <i class="fa-solid fa-image" style="font-size:24px; color:var(--text-muted);"></i>
                                            <span style="font-size:12px; font-weight:600; margin-top:8px;">Subir Fondo Trasero</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-row-3 mt-16">
                                    <div class="form-group">
                                        <label>Fondo</label>
                                        <input type="color" id="color-primary" value="#1e1b4b" style="padding:2px; height:40px; width:100%; border-radius:8px; border:none; cursor:pointer;">
                                    </div>
                                    <div class="form-group">
                                        <label>Acento Holográfico</label>
                                        <input type="color" id="color-accent" value="#8b5cf6" style="padding:2px; height:40px; width:100%; border-radius:8px; border:none; cursor:pointer;">
                                    </div>
                                    <div class="form-group">
                                        <label>Icono</label>
                                        <select id="rest-icon" class="fidelio-input" style="padding:8px; height:40px;">
                                            <option value="fa-burger">Burger</option>
                                            <option value="fa-scissors">Scissors</option>
                                            <option value="fa-mug-hot">Mug</option>
                                            <option value="fa-dumbbell">Dumbbell</option>
                                            <option value="fa-spa">Spa</option>
                                            <option value="fa-martini-glass">Martini</option>
                                            <option value="fa-crown" selected>Crown</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- STEP 3 -->
                            <div class="accordion-card">
                                <div class="card-title-bar">
                                    <span class="card-step-badge">03</span>
                                    <h2>Términos y Programas del Reverso</h2>
                                </div>
                                
                                <div class="form-group">
                                    <label>Premio Activo (Nivel Bronce)</label>
                                    <input type="text" id="stamps-reward" value="Bebida de Cortesía" class="fidelio-input">
                                </div>

                                <div class="form-group" style="margin-top: 16px;">
                                    <label>Políticas Legales (Reverso)</label>
                                    <textarea id="pass-policies" class="fidelio-input" rows="3" placeholder="Ejem: El cashback caduca en 90 días.">Las recompensas no son transferibles ni canjeables por efectivo. Nos reservamos el derecho de modificar el programa.</textarea>
                                </div>
                            </div>
                        </form>
                    </div>

                    <!-- PREVIEW -->
                    <div class="phone-studio-panel" style="background:transparent; border:none;">
                        
                        <div class="iphone-device premium-mockup">
                            <div class="dynamic-island"><div class="lens"></div></div>
                            <div class="iphone-screen">
                                
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; z-index:20; position:relative;">
                                    <span style="color:rgba(255,255,255,0.7); font-size:16px; font-weight:600;"><i class="fa-solid fa-wallet"></i> Wallet</span>
                                    <button id="btn-flip-card" style="background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.2); color:white; padding:6px 16px; border-radius:20px; font-size:12px; font-weight:700; cursor:pointer; backdrop-filter:blur(10px); transition:all 0.3s;"><i class="fa-solid fa-rotate-right"></i> Voltear (3D)</button>
                                </div>

                                <div class="card-3d-scene">
                                    <div class="card-3d-object" id="pass-render">
                                        
                                        <!-- FRONT FACE -->
                                        <div class="card-face card-front" id="pass-front-face" style="background: linear-gradient(135deg, #1e1b4b, #8b5cf6); padding: 24px; color: white;">
                                            <div class="holographic-sheen"></div>
                                            
                                            <!-- Apple Wallet Header -->
                                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 30px;">
                                                <div style="display:flex; align-items:center; gap:12px; z-index:2;">
                                                    <div style="width:48px; height:48px; background:rgba(0,0,0,0.3); border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:inset 0 0 10px rgba(0,0,0,0.5); font-size:20px; border:1px solid rgba(255,255,255,0.1);">
                                                        <i class="fa-solid fa-crown" id="render-icon"></i>
                                                    </div>
                                                    <div>
                                                        <div id="render-name" style="font-weight:700; font-size:20px; text-shadow:0 2px 4px rgba(0,0,0,0.5); letter-spacing:-0.5px;">Mi Negocio</div>
                                                        <div id="render-category" style="font-size:12px; opacity:0.8; font-weight:500;">Restaurante & Gastronomía</div>
                                                    </div>
                                                </div>
                                                <div style="background:rgba(0,0,0,0.4); padding:4px 12px; border-radius:12px; font-size:10px; font-weight:800; letter-spacing:1px; border:1px solid rgba(255,255,255,0.2);">ORO VIP</div>
                                            </div>
                                            
                                            <!-- Main Balance -->
                                            <div style="margin-bottom: 30px; position:relative; z-index:2;">
                                                <div style="font-size:13px; font-weight:600; opacity:0.8; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Cashback Disponible</div>
                                                <div style="font-size:42px; font-weight:900; letter-spacing:-1px; text-shadow:0 2px 10px rgba(0,0,0,0.3); display:flex; align-items:baseline; gap:4px;">
                                                    $145<span style="font-size:24px;">.00</span>
                                                </div>
                                            </div>
                                            
                                            <!-- Stamps / Progress -->
                                            <div style="background:rgba(0,0,0,0.25); border-radius:16px; padding:16px; border:1px solid rgba(255,255,255,0.1); margin-bottom: 20px; position:relative; z-index:2; backdrop-filter:blur(5px);">
                                                <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:600; margin-bottom:12px;">
                                                    <span>Recompensa (3/5)</span>
                                                    <span id="render-reward-text" style="color:#10b981;">Bebida de Cortesía</span>
                                                </div>
                                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                                    <div style="width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.9); color:#1e1b4b; display:flex; align-items:center; justify-content:center; font-size:16px;"><i class="fa-solid fa-check"></i></div>
                                                    <div style="width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.9); color:#1e1b4b; display:flex; align-items:center; justify-content:center; font-size:16px;"><i class="fa-solid fa-check"></i></div>
                                                    <div style="width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.9); color:#1e1b4b; display:flex; align-items:center; justify-content:center; font-size:16px;"><i class="fa-solid fa-check"></i></div>
                                                    <div style="width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.2); display:flex; align-items:center; justify-content:center; font-size:12px; border:1px dashed rgba(255,255,255,0.4);"><i class="fa-solid fa-lock"></i></div>
                                                    <div style="width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.2); display:flex; align-items:center; justify-content:center; font-size:12px; border:1px dashed rgba(255,255,255,0.4);"><i class="fa-solid fa-lock"></i></div>
                                                </div>
                                            </div>
                                            
                                            <!-- Flash Promo -->
                                            <div style="text-align:center; position:relative; z-index:2; background:rgba(255,255,255,0.15); padding:10px; border-radius:12px; font-size:13px; font-weight:700;">
                                                <i class="fa-solid fa-bolt" style="color:#FBBF24;"></i> <span id="render-promo-text">Martes y Jueves: Doble Cashback</span>
                                            </div>
                                            
                                        </div>
                                        
                                        <!-- BACK FACE -->
                                        <div class="card-face card-back">
                                            <div class="nfc-badge">
                                                <i class="fa-brands fa-apple"></i> Apple Wallet &nbsp;|&nbsp; <i class="fa-brands fa-google"></i> Google Wallet
                                            </div>
                                            
                                            <div class="qr-container-back">
                                                <img src="dummy_qr.png" alt="QR" style="width:100%; height:100%; object-fit:contain; opacity:0.9;">
                                            </div>
                                            
                                            <div style="margin-top:16px; font-size:12px; color:#888; text-transform:uppercase; letter-spacing:1px; font-weight:700;">Acerca tu teléfono para cobrar</div>
                                            
                                            <div style="width:100%; height:1px; background:#333; margin:24px 0;"></div>
                                            
                                            <div style="width:100%; text-align:left;">
                                                <h4 style="font-size:14px; color:#ddd; margin-bottom:8px;">Detalles del Nivel VIP</h4>
                                                <p style="font-size:12px; color:#999; line-height:1.5; margin-bottom:16px;">Acumulas el 15% de todas tus compras en cashback. Acceso prioritario sin filas.</p>
                                                
                                                <h4 style="font-size:14px; color:#ddd; margin-bottom:8px;">Términos y Políticas</h4>
                                                <p id="render-policies-text" style="font-size:12px; color:#999; line-height:1.5;">Las recompensas no son transferibles ni canjeables por efectivo. Nos reservamos el derecho de modificar el programa.</p>
                                            </div>
                                        </div>
                                        
                                    </div>
                                </div>
                                
                                <div style="position:absolute; bottom:30px; left:0; width:100%; text-align:center; color:rgba(255,255,255,0.5); font-size:24px;">
                                    <div style="width:50px; height:5px; background:rgba(255,255,255,0.5); border-radius:5px; margin:0 auto;"></div>
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
