import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_marketing = """            <section id="tab-marketing" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">CRECIMIENTO</span>
                        <h1>Marketing & Push</h1>
                        <p>Segmenta a tus clientes y envía notificaciones directo a su pantalla de bloqueo.</p>
                    </div>
                </div>
                
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; max-width:1000px;">
                    <div class="content-panel">
                        <h3 style="margin-bottom:16px;"><i class="fa-solid fa-wand-magic-sparkles" style="color:var(--accent-violet);"></i> Campañas de Inteligencia Artificial</h3>
                        <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:16px;">Selecciona una campaña predictiva. Fidelio autogenerará el texto y seleccionará la audiencia óptima.</p>
                        
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom: 24px;">
                            <div class="campaign-card" onclick="selectCampaign('recuperacion')">
                                <div><i class="fa-solid fa-heart-crack"></i></div>
                                <strong>Recuperar Perdidos</strong>
                                <small>Clientes en riesgo</small>
                            </div>
                            <div class="campaign-card" onclick="selectCampaign('cumpleanos')">
                                <div><i class="fa-solid fa-cake-candles"></i></div>
                                <strong>Cumpleañeros</strong>
                                <small>Mes actual</small>
                            </div>
                            <div class="campaign-card" onclick="selectCampaign('dias_lentos')">
                                <div><i class="fa-solid fa-clock"></i></div>
                                <strong>Días Muertos</strong>
                                <small>Impulso de tráfico</small>
                            </div>
                            <div class="campaign-card" onclick="selectCampaign('vip_exclusivo')">
                                <div><i class="fa-solid fa-crown"></i></div>
                                <strong>VIP Exclusivo</strong>
                                <small>Solo nivel Oro</small>
                            </div>
                            <div class="campaign-card" onclick="selectCampaign('resenas')">
                                <div><i class="fa-solid fa-star"></i></div>
                                <strong>Caza Reseñas</strong>
                                <small>Frecuentes recientes</small>
                            </div>
                            <div class="campaign-card active" onclick="selectCampaign('manual')">
                                <div><i class="fa-solid fa-pen-nib"></i></div>
                                <strong>Crear Manual</strong>
                                <small>Texto libre</small>
                            </div>
                        </div>

                        <h3 style="margin-bottom:12px; border-top: 1px solid var(--border-glass); padding-top: 20px;">Filtro Manual (Opcional)</h3>
                        <div class="segment-card" onclick="selectSegment('all')" id="seg-card-all">
                            <div><strong>Todos los Clientes</strong> <small style="display:block; color:var(--text-muted);">Base completa</small></div>
                            <span class="tier-pill oro" id="seg-all-count">0</span>
                        </div>
                        <div class="segment-card" onclick="selectSegment('active')" id="seg-card-active">
                            <div><strong>Frecuentes</strong> <small style="display:block; color:var(--text-muted);">Visitaron en los últimos 30 días</small></div>
                            <span class="tier-pill activo" id="seg-active-count">0</span>
                        </div>
                        <div class="segment-card" onclick="selectSegment('risk')" id="seg-card-risk">
                            <div><strong>En Riesgo (Perdidos)</strong> <small style="display:block; color:var(--text-muted);">Sin visitas por más de 30 días</small></div>
                            <span class="tier-pill riesgo" id="seg-risk-count">0</span>
                        </div>
                    </div>
                    
                    <div class="content-panel" style="display:flex; flex-direction:column;">
                        <h3 style="margin-bottom:16px;"><i class="fa-solid fa-paper-plane"></i> Lanzar Campaña Push</h3>
                        <div style="background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.2); padding: 16px; border-radius: 12px; margin-bottom: 24px;">
                            <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:4px;">Audiencia objetivo:</p>
                            <strong id="selected-segment-name" style="color:#fff; font-size: 1.1rem;">Todos los Clientes</strong>
                        </div>
                        
                        <div class="form-group" style="flex:1;">
                            <label>Mensaje Push a Pantalla de Bloqueo</label>
                            <textarea id="push-message" class="fidelio-input" style="height: 150px; resize: none; font-size: 1.1rem; padding: 16px;" placeholder="Ej. ¡Te extrañamos! Visítanos este fin de semana y obtén doble cashback. Escribe tu mensaje aquí..."></textarea>
                        </div>
                        
                        <button id="btn-send-push" class="btn-primary" style="width:100%; padding: 16px; font-size: 1.1rem; margin-top: 20px;"><i class="fa-solid fa-tower-broadcast"></i> Disparar Push a Apple Wallet</button>
                    </div>
                </div>
            </section>"""

new_marketing = """            <section id="tab-marketing" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">CRECIMIENTO INTELIGENTE</span>
                        <h1>Marketing & Campañas AI</h1>
                        <p>Fidelio analiza a tus clientes y te sugiere campañas automáticas omnicanal (Wallet, WhatsApp, Email).</p>
                    </div>
                </div>
                
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:24px;">
                    <!-- LEFT COLUMN: AI MODULES LIST -->
                    <div style="display:flex; flex-direction:column; gap:16px;">
                        
                        <div class="accordion-card campaign-module active" onclick="selectAICampaign('recuperacion', this)">
                            <div style="display:flex; align-items:center; gap: 16px;">
                                <div class="stat-icon" style="background:rgba(139, 92, 246, 0.1); color:var(--accent-violet);"><i class="fa-solid fa-heart-crack"></i></div>
                                <div style="flex:1;">
                                    <h4 style="margin:0; font-size:16px;">Recuperar Perdidos</h4>
                                    <p style="margin:4px 0 0 0; font-size:12px; color:var(--text-muted);">Clientes sin visitas en >30 días</p>
                                </div>
                                <div style="color:var(--text-muted);"><i class="fa-solid fa-chevron-right"></i></div>
                            </div>
                        </div>

                        <div class="accordion-card campaign-module" onclick="selectAICampaign('cumpleanos', this)">
                            <div style="display:flex; align-items:center; gap: 16px;">
                                <div class="stat-icon" style="background:rgba(139, 92, 246, 0.1); color:var(--accent-violet);"><i class="fa-solid fa-cake-candles"></i></div>
                                <div style="flex:1;">
                                    <h4 style="margin:0; font-size:16px;">Cumpleañeros del Mes</h4>
                                    <p style="margin:4px 0 0 0; font-size:12px; color:var(--text-muted);">Envía regalo en su mes de cumpleaños</p>
                                </div>
                                <div style="color:var(--text-muted);"><i class="fa-solid fa-chevron-right"></i></div>
                            </div>
                        </div>

                        <div class="accordion-card campaign-module" onclick="selectAICampaign('dias_lentos', this)">
                            <div style="display:flex; align-items:center; gap: 16px;">
                                <div class="stat-icon" style="background:rgba(139, 92, 246, 0.1); color:var(--accent-violet);"><i class="fa-solid fa-clock"></i></div>
                                <div style="flex:1;">
                                    <h4 style="margin:0; font-size:16px;">Inyección Días Lentos</h4>
                                    <p style="margin:4px 0 0 0; font-size:12px; color:var(--text-muted);">Aumenta tráfico en horas valle</p>
                                </div>
                                <div style="color:var(--text-muted);"><i class="fa-solid fa-chevron-right"></i></div>
                            </div>
                        </div>

                        <div class="accordion-card campaign-module" onclick="selectAICampaign('vip_exclusivo', this)">
                            <div style="display:flex; align-items:center; gap: 16px;">
                                <div class="stat-icon" style="background:rgba(139, 92, 246, 0.1); color:var(--accent-violet);"><i class="fa-solid fa-crown"></i></div>
                                <div style="flex:1;">
                                    <h4 style="margin:0; font-size:16px;">Recompensa VIP</h4>
                                    <p style="margin:4px 0 0 0; font-size:12px; color:var(--text-muted);">Trato preferencial solo para Nivel Oro</p>
                                </div>
                                <div style="color:var(--text-muted);"><i class="fa-solid fa-chevron-right"></i></div>
                            </div>
                        </div>

                        <div class="accordion-card campaign-module" onclick="selectAICampaign('manual', this)">
                            <div style="display:flex; align-items:center; gap: 16px;">
                                <div class="stat-icon" style="background:rgba(139, 92, 246, 0.1); color:var(--accent-violet);"><i class="fa-solid fa-pen-nib"></i></div>
                                <div style="flex:1;">
                                    <h4 style="margin:0; font-size:16px;">Campaña Libre</h4>
                                    <p style="margin:4px 0 0 0; font-size:12px; color:var(--text-muted);">Segmentación y mensaje manual</p>
                                </div>
                                <div style="color:var(--text-muted);"><i class="fa-solid fa-chevron-right"></i></div>
                            </div>
                        </div>

                    </div>
                    
                    <!-- RIGHT COLUMN: CONFIGURATION PANEL -->
                    <div class="content-panel" style="display:flex; flex-direction:column; position: sticky; top: 0; max-height: calc(100vh - 150px); overflow-y: auto;">
                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border-glass); padding-bottom:16px; margin-bottom:20px;">
                            <h3 id="config-camp-title" style="margin:0;"><i class="fa-solid fa-heart-crack" style="color:var(--accent-violet); margin-right:8px;"></i> Recuperar Perdidos</h3>
                            <span class="live-badge" style="background: rgba(139, 92, 246, 0.1); color: var(--accent-violet); border: 1px solid rgba(139, 92, 246, 0.2);"><div class="live-dot" style="background:var(--accent-violet);"></div> Listo para configurar</span>
                        </div>

                        <!-- CHANNELS -->
                        <h4 style="font-size:14px; margin-bottom:12px; color:var(--text-main);">Canales de Emisión</h4>
                        <div style="display:flex; gap:12px; margin-bottom: 24px;">
                            <label class="channel-toggle active" id="ch-wallet">
                                <input type="checkbox" checked style="display:none;" onchange="window.toggleChannel(this)">
                                <i class="fa-brands fa-apple"></i> Apple Wallet Push
                            </label>
                            <label class="channel-toggle" id="ch-whatsapp">
                                <input type="checkbox" checked style="display:none;" onchange="window.toggleChannel(this)">
                                <i class="fa-brands fa-whatsapp"></i> WhatsApp
                            </label>
                            <label class="channel-toggle" id="ch-email">
                                <input type="checkbox" style="display:none;" onchange="window.toggleChannel(this)">
                                <i class="fa-solid fa-envelope"></i> Email
                            </label>
                        </div>

                        <!-- TRIGGERS -->
                        <h4 style="font-size:14px; margin-bottom:12px; color:var(--text-main);">Automatización</h4>
                        <div style="display:flex; gap:16px; margin-bottom:24px;">
                            <label class="radio-card" style="flex:1; border: 2px solid var(--accent-violet);">
                                <input type="radio" name="camp_trigger" value="automated" checked onchange="window.updateTriggerUI()">
                                <div><i class="fa-solid fa-robot" style="color:var(--accent-violet);"></i></div>
                                <span>Regla Activa</span>
                                <small>Enviar siempre que se cumpla</small>
                            </label>
                            <label class="radio-card" style="flex:1;">
                                <input type="radio" name="camp_trigger" value="one_time" onchange="window.updateTriggerUI()">
                                <div><i class="fa-solid fa-paper-plane" style="color:var(--text-muted);"></i></div>
                                <span>Disparo Único</span>
                                <small>Enviar ahora a la base actual</small>
                            </label>
                        </div>

                        <!-- SEGMENT FOR MANUAL (HIDDEN BY DEFAULT) -->
                        <div id="manual-segment-selector" style="display:none; margin-bottom:24px;">
                            <h4 style="font-size:14px; margin-bottom:12px; color:var(--text-main);">Filtro de Audiencia</h4>
                            <select class="fidelio-input" id="camp-segment-select">
                                <option value="all">Todos los Clientes</option>
                                <option value="active">Frecuentes (Visitaron < 30 días)</option>
                                <option value="risk">En Riesgo (Sin visitas > 30 días)</option>
                            </select>
                        </div>
                        
                        <!-- AI GENERATOR -->
                        <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:8px;">
                            <h4 style="font-size:14px; margin:0; color:var(--text-main);">Mensaje Omnicanal</h4>
                            <button class="btn" style="background:rgba(139, 92, 246, 0.1); color:var(--accent-violet); padding: 6px 12px; font-size:12px; font-weight:700;" onclick="window.generateAIPush()"><i class="fa-solid fa-wand-magic-sparkles"></i> Optimizar con IA</button>
                        </div>
                        <div class="form-group" style="flex:1; position:relative; overflow: hidden; border-radius:12px;">
                            <textarea id="camp-push-message" class="fidelio-input" style="height: 120px; resize: none; font-size: 1rem; padding: 16px;" placeholder="Escribe tu mensaje o usa la IA..."></textarea>
                            <div id="ai-loading" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(17, 24, 39, 0.8); backdrop-filter:blur(4px); align-items:center; justify-content:center; flex-direction:column; z-index:10;">
                                <i class="fa-solid fa-circle-notch fa-spin" style="color:var(--accent-violet); font-size:32px; margin-bottom:12px;"></i>
                                <span style="font-size:12px; font-weight:700; color:var(--accent-violet);">Optimizando texto para mayor conversión...</span>
                            </div>
                        </div>
                        
                        <button id="btn-save-camp" class="btn btn-primary" style="width:100%; padding: 16px; font-size: 1.1rem; margin-top: 10px; background: linear-gradient(135deg, var(--accent-violet) 0%, #4C1D95 100%);"><i class="fa-solid fa-play"></i> Activar Campaña</button>
                    </div>
                </div>
            </section>"""

if old_marketing in html:
    html = html.replace(old_marketing, new_marketing)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Marketing HTML updated successfully!")
else:
    print("Failed to find old marketing HTML.")
