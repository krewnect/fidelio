import sys

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix the missing cashback-example paragraph
old_cashback = """                                <input type="range" id="cashback-slider" min="1" max="25" value="10" style="flex:1; accent-color: #10B981;">
                                <span id="cashback-percent-display" style="font-size:18px; font-weight:700; color:#10B981; min-width:50px;">10%</span>
                            </div>
                        </div>
                    </div>"""

new_cashback = """                                <input type="range" id="cashback-slider" min="1" max="25" value="10" style="flex:1; accent-color: #10B981;">
                                <span id="cashback-percent-display" style="font-size:18px; font-weight:700; color:#10B981; min-width:50px;">10%</span>
                            </div>
                            <p style="font-size:12px; color:var(--text-muted); margin-top:8px;">Por cada $100 gastados, el cliente recibe $<span id="cashback-example">10</span> en su saldo.</p>
                        </div>
                    </div>"""

html = html.replace(old_cashback, new_cashback)

# 2. Add 3 new role-cards to the loyalty-mode selector
old_role_cards = """                        <label class="role-card" id="loyalty-mode-stamps">
                            <input type="radio" name="loyalty_mode" value="stamps" style="display:none;">
                            <div class="role-icon" style="color:#F59E0B; background:rgba(245, 158, 11, 0.1);"><i class="fa-solid fa-stamp"></i></div>
                            <div class="role-info">
                                <h4>Solo Sellos</h4>
                                <p>Clientes acumulan visitas por un premio.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>
                    </div>"""

new_role_cards = """                        <label class="role-card" id="loyalty-mode-stamps">
                            <input type="radio" name="loyalty_mode" value="stamps" style="display:none;">
                            <div class="role-icon" style="color:#F59E0B; background:rgba(245, 158, 11, 0.1);"><i class="fa-solid fa-stamp"></i></div>
                            <div class="role-info">
                                <h4>Solo Sellos</h4>
                                <p>Clientes acumulan visitas por un premio.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>

                        <label class="role-card" id="loyalty-mode-membership">
                            <input type="radio" name="loyalty_mode" value="membership" style="display:none;">
                            <div class="role-icon" style="color:#3B82F6; background:rgba(59, 130, 246, 0.1);"><i class="fa-solid fa-id-card-clip"></i></div>
                            <div class="role-info">
                                <h4>Membresía VIP</h4>
                                <p>Suscripción recurrente para acceso a descuentos y beneficios fijos.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>
                        
                        <label class="role-card" id="loyalty-mode-prepaid">
                            <input type="radio" name="loyalty_mode" value="prepaid" style="display:none;">
                            <div class="role-icon" style="color:#EC4899; background:rgba(236, 72, 153, 0.1);"><i class="fa-solid fa-money-bill-transfer"></i></div>
                            <div class="role-info">
                                <h4>Monedero Prepago</h4>
                                <p>El cliente carga saldo por adelantado a cambio de una bonificación.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>
                        
                        <label class="role-card" id="loyalty-mode-custom">
                            <input type="radio" name="loyalty_mode" value="custom" style="display:none;">
                            <div class="role-icon" style="color:var(--text-main); background:var(--bg-input);"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
                            <div class="role-info">
                                <h4>Personalizado</h4>
                                <p>Diseña tu propia mecánica, métricas y recompensas 100% a tu gusto.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>
                    </div>"""

html = html.replace(old_role_cards, new_role_cards)

# 3. Add Custom Settings Panel
old_settings = """                <!-- VIP TIERS SETTINGS -->"""
new_settings = """                <!-- CUSTOM / MEMBERSHIP SETTINGS (DYNAMIC) -->
                <div id="panel-loyalty-custom" class="accordion-card" style="display:none; margin-bottom: 24px; border-left: 4px solid var(--accent-violet);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <div>
                            <h3 style="font-size: 16px; margin:0;" id="custom-panel-title"><i class="fa-solid fa-sliders" style="color:var(--accent-violet); margin-right:8px;"></i> Configuración del Programa</h3>
                            <p style="font-size:12px; color:var(--text-muted); margin-top:4px;" id="custom-panel-desc">Ajusta las variables de tu modelo seleccionado.</p>
                        </div>
                    </div>
                    
                    <div id="settings-membership" style="display:none;">
                        <div class="form-group" style="margin-bottom: 16px;">
                            <label>Precio de la Membresía (Mensual)</label>
                            <input type="number" id="mem-price" class="fidelio-input" placeholder="Ej. 199" value="199">
                        </div>
                        <div class="form-group">
                            <label>Beneficio Principal (Lo que ven en Wallet)</label>
                            <input type="text" id="mem-perk" class="fidelio-input" placeholder="Ej. 20% OFF en todo el menú" value="20% OFF en Tienda">
                        </div>
                    </div>
                    
                    <div id="settings-prepaid" style="display:none;">
                        <div class="form-group" style="margin-bottom: 16px;">
                            <label>Monto de Recarga Sugerido (MXN)</label>
                            <input type="number" id="pre-amount" class="fidelio-input" placeholder="Ej. 500" value="500">
                        </div>
                        <div class="form-group">
                            <label>Bono de Regalo al Recargar (MXN)</label>
                            <input type="number" id="pre-bonus" class="fidelio-input" placeholder="Ej. 100" value="100">
                            <p style="font-size:12px; color:var(--text-muted); margin-top:8px;">Al recargar, el cliente recibe <strong style="color:#10B981;" id="pre-total-display">$600</strong> en total.</p>
                        </div>
                    </div>
                    
                    <div id="settings-custom-prog" style="display:none;">
                        <div class="form-group" style="margin-bottom: 16px;">
                            <label>Nombre de tu Programa</label>
                            <input type="text" id="cus-name" class="fidelio-input" placeholder="Ej. Club de Lectores" value="Mi Programa VIP">
                        </div>
                        <div class="form-group">
                            <label>Regla de Recompensa (Texto libre)</label>
                            <textarea id="cus-rules" class="fidelio-input" rows="3" placeholder="Ej. Compra 3 libros y llévate un marcapáginas gratis."></textarea>
                        </div>
                    </div>
                </div>

                <!-- VIP TIERS SETTINGS -->"""
html = html.replace(old_settings, new_settings)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Updated HTML with slider fix and new loyalty options.")
