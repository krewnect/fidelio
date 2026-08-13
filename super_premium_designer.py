import re

with open('index.html', 'r') as f:
    html = f.read()

new_tab_content = """<section id="tab-builder" class="tab-content">
                <style>
                    /* Stripe/Vercel Aesthetic for Builder */
                    .tab-builder-container { display: flex; height: calc(100vh - 100px); overflow: hidden; background: #fafafa; margin: -24px; }
                    .builder-sidebar { width: 420px; background: white; border-right: 1px solid var(--border-glass); overflow-y: auto; padding: 32px; display:flex; flex-direction:column; gap:24px; box-shadow: 10px 0 30px rgba(0,0,0,0.02); z-index:10; }
                    .builder-preview-area { flex: 1; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle at center, #f3f4f6 0%, #e5e7eb 100%); position: relative; overflow: hidden; }
                    
                    /* Clean Form Elements */
                    .premium-label { font-size: 13px; font-weight: 600; color: #374151; margin-bottom: 8px; display: block; }
                    .premium-input { width: 100%; padding: 12px 16px; border: 1px solid #d1d5db; border-radius: 8px; font-family: var(--font-main); font-size: 14px; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
                    .premium-input:focus { outline: none; border-color: var(--accent-violet); box-shadow: 0 0 0 3px rgba(76,29,149,0.1); }
                    
                    .premium-section-title { font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 4px; letter-spacing:-0.5px; }
                    .premium-section-desc { font-size: 13px; color: #6b7280; margin-bottom: 20px; line-height: 1.4; }
                    .premium-divider { height: 1px; background: #e5e7eb; margin: 8px 0; }
                    
                    /* Massive Apple Wallet Pass */
                    .wallet-pass-hero { width: 380px; height: 600px; background: white; border-radius: 20px; box-shadow: 0 50px 100px -20px rgba(0,0,0,0.25), 0 30px 60px -30px rgba(0,0,0,0.3); position: relative; display: flex; flex-direction: column; overflow: hidden; transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1); transform-origin: center; }
                    
                    /* Dynamic scaling to make it huge but fit */
                    @media (min-width: 1400px) { .wallet-pass-hero { transform: scale(1.3); } }
                    @media (min-width: 1600px) { .wallet-pass-hero { transform: scale(1.5); } }
                    
                    .pass-top-section { padding: 24px; color: white; position: relative; background: linear-gradient(135deg, #1e1b4b, #8b5cf6); }
                    .pass-brand-row { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; position:relative; z-index:2; }
                    .pass-brand-info { display: flex; align-items: center; gap: 12px; }
                    .pass-logo-circle { width: 44px; height: 44px; background: rgba(0,0,0,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; color: white; border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(5px); }
                    
                    .pass-banner-img { width: 100%; height: 140px; object-fit: cover; background: rgba(255,255,255,0.1); }
                    
                    .pass-body-section { flex: 1; background: white; padding: 24px; display: flex; flex-direction: column; }
                    
                    .pass-field-group { margin-bottom: 20px; }
                    .pass-field-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; font-weight: 600; margin-bottom: 4px; }
                    .pass-field-value { font-size: 24px; font-weight: 700; color: #111827; letter-spacing:-0.5px; }
                    
                    .pass-qr-section { margin-top: auto; display: flex; flex-direction: column; align-items: center; padding-top: 20px; border-top: 1px dashed #e5e7eb; }
                    
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
                            <h1 style="font-size: 24px; font-weight: 800; letter-spacing: -1px; color: #111827;">Estudio de Diseño</h1>
                            <p style="font-size: 14px; color: #6b7280; margin-top: 8px;">Configura la tarjeta digital que tus clientes instalarán en sus teléfonos. Todo cambio se refleja al instante.</p>
                        </div>
                        
                        <div class="premium-divider"></div>
                        
                        <!-- 1. Identidad -->
                        <div>
                            <div class="premium-section-title">Identidad de Marca</div>
                            <div class="premium-section-desc">El nombre y el giro de tu establecimiento.</div>
                            
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
                            <div class="premium-section-desc">Personaliza los colores para alinear la tarjeta con tu marca.</div>
                            
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
                            <div class="premium-section-desc">Lo que tus clientes verán como recompensa activa.</div>
                            
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
                    
                    <!-- RIGHT AREA: MASSIVE PREVIEW -->
                    <div class="builder-preview-area">
                        <!-- Floating Background Elements for Premium feel -->
                        <div style="position:absolute; top:-10%; left:-10%; width:50%; height:50%; background:radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%);"></div>
                        <div style="position:absolute; bottom:-10%; right:-10%; width:50%; height:50%; background:radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);"></div>
                        
                        <div style="position:absolute; top: 40px; right: 40px; background:white; padding:8px 16px; border-radius:20px; font-size:13px; font-weight:700; color:#10B981; box-shadow:0 10px 20px rgba(0,0,0,0.05); display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-circle-check"></i> Diseño optimizado para Apple Wallet</div>

                        <!-- THE PASS -->
                        <div class="wallet-pass-hero" id="pass-render">
                            <!-- Header Area -->
                            <div class="pass-top-section" id="pass-front-face">
                                <!-- Apple Wallet Cutouts (Visual only) -->
                                <div style="position:absolute; top:12px; right:24px; width:40px; height:4px; background:rgba(255,255,255,0.3); border-radius:2px;"></div>
                                
                                <div class="pass-brand-row">
                                    <div class="pass-brand-info">
                                        <div class="pass-logo-circle">
                                            <i class="fa-solid fa-crown" id="render-icon"></i>
                                        </div>
                                        <div>
                                            <div id="render-name" style="font-weight:700; font-size:22px; letter-spacing:-0.5px;">Mi Negocio</div>
                                            <div id="render-category" style="font-size:13px; opacity:0.8; font-weight:500;">Restaurante & Gastronomía</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                                    <div>
                                        <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:4px;">Nivel Actual</div>
                                        <div id="render-vip-caption" style="font-size:24px; font-weight:800; letter-spacing:-0.5px;">ORO VIP</div>
                                    </div>
                                    <div style="text-align:right;">
                                        <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:1px; opacity:0.8; margin-bottom:4px;">Cashback</div>
                                        <div style="font-size:24px; font-weight:800; letter-spacing:-0.5px;" id="render-balance">$145.00</div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Middle Image -->
                            <div id="render-banner-container" style="background:#f9fafb;">
                                <img id="render-banner-img" src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&q=80&w=800&h=300" alt="Banner" class="pass-banner-img">
                            </div>
                            
                            <!-- Body Info -->
                            <div class="pass-body-section">
                                <div style="display:flex; gap:24px; margin-bottom:24px;">
                                    <div style="flex:1;">
                                        <div class="pass-field-label">Próxima Recompensa</div>
                                        <div class="pass-field-value" style="font-size:16px; color:#10B981;" id="render-reward-text">Bebida de Cortesía Gratis</div>
                                    </div>
                                    <div style="text-align:right;">
                                        <div class="pass-field-label">Visitas</div>
                                        <div class="pass-field-value" style="font-size:16px;">3 / 5</div>
                                    </div>
                                </div>
                                
                                <div class="pass-field-group">
                                    <div class="pass-field-label">Notificación Flash</div>
                                    <div class="pass-field-value" style="font-size:15px; font-weight:600; background:#f3f4f6; padding:12px; border-radius:8px; display:inline-block; width:100%;">
                                        <i class="fa-solid fa-bolt" style="color:#F59E0B; margin-right:8px;"></i> <span id="render-promo-text">Martes Doble Cashback</span>
                                    </div>
                                </div>
                                
                                <div class="pass-qr-section">
                                    <img src="dummy_qr.png" alt="QR Code" style="width:140px; height:140px; mix-blend-mode:multiply; opacity:0.9;">
                                    <div style="margin-top:12px; font-size:11px; font-weight:700; color:#9ca3af; letter-spacing:1.5px;">FIDELIO-8842-MEX</div>
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
