import sys

html_content = """
            <!-- LOYALTY TAB (FIDELIZACIÓN) -->
            <section id="tab-loyalty" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">ESTRATEGIA Y CRECIMIENTO</span>
                        <h1>Reglas de Fidelización</h1>
                        <p>Configura las mecánicas exactas para premiar y retener a tus clientes. Puedes combinar múltiples mecánicas.</p>
                    </div>
                    <div>
                        <button id="btn-save-loyalty" class="btn btn-primary" style="background: linear-gradient(135deg, var(--accent-violet) 0%, #4C1D95 100%);">
                            <i class="fa-solid fa-floppy-disk"></i> Guardar Reglas
                        </button>
                    </div>
                </div>

                <div class="accordion-card" style="margin-bottom: 24px;">
                    <h3 style="margin-bottom:20px; font-size: 16px;"><i class="fa-solid fa-gears" style="color:var(--accent-violet); margin-right:8px;"></i> Motor Principal de Recompensas</h3>
                    
                    <div class="role-selector" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
                        <label class="role-card" id="loyalty-mode-hybrid">
                            <input type="radio" name="loyalty_mode" value="hybrid" checked style="display:none;">
                            <div class="role-icon" style="color:var(--accent-violet); background:rgba(139, 92, 246, 0.1);"><i class="fa-solid fa-layer-group"></i></div>
                            <div class="role-info">
                                <h4>Modalidad Híbrida (Recomendado)</h4>
                                <p>Activa Cashback, Sellos y Niveles VIP simultáneamente.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>

                        <label class="role-card" id="loyalty-mode-cashback">
                            <input type="radio" name="loyalty_mode" value="cashback" style="display:none;">
                            <div class="role-icon" style="color:#10B981; background:rgba(16, 185, 129, 0.1);"><i class="fa-solid fa-wallet"></i></div>
                            <div class="role-info">
                                <h4>Solo Cashback</h4>
                                <p>Clientes acumulan saldo por compras.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>
                        
                        <label class="role-card" id="loyalty-mode-stamps">
                            <input type="radio" name="loyalty_mode" value="stamps" style="display:none;">
                            <div class="role-icon" style="color:#F59E0B; background:rgba(245, 158, 11, 0.1);"><i class="fa-solid fa-stamp"></i></div>
                            <div class="role-info">
                                <h4>Solo Sellos</h4>
                                <p>Clientes acumulan visitas por un premio.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>
                    </div>
                </div>

                <div style="display:flex; gap: 24px; flex-wrap: wrap; margin-bottom: 24px;">
                    <!-- CASHBACK SETTINGS -->
                    <div class="accordion-card" style="flex: 1; min-width: 300px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                            <h3 style="font-size: 16px; margin:0;"><i class="fa-solid fa-wallet" style="color:#10B981; margin-right:8px;"></i> Configuración de Cashback</h3>
                            <label class="toggle-switch">
                                <input type="checkbox" id="toggle-cashback" checked>
                                <span class="toggle-slider"></span>
                            </label>
                        </div>
                        
                        <div class="form-group">
                            <label>Porcentaje Base de Retorno (%)</label>
                            <div style="display:flex; align-items:center; gap: 12px;">
                                <input type="range" id="cashback-slider" min="1" max="25" value="10" style="flex:1; accent-color: #10B981;">
                                <span id="cashback-percent-display" style="font-size:18px; font-weight:700; color:#10B981; min-width:50px;">10%</span>
                            </div>
                        </div>
                    </div>

                    <!-- STAMPS SETTINGS -->
                    <div class="accordion-card" style="flex: 1; min-width: 300px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                            <h3 style="font-size: 16px; margin:0;"><i class="fa-solid fa-stamp" style="color:#F59E0B; margin-right:8px;"></i> Configuración de Sellos</h3>
                            <label class="toggle-switch">
                                <input type="checkbox" id="toggle-stamps" checked>
                                <span class="toggle-slider"></span>
                            </label>
                        </div>
                        
                        <div class="form-group" style="margin-bottom: 16px;">
                            <label>Cantidad Total de Sellos</label>
                            <input type="number" id="stamps-total" class="fidelio-input" value="5" min="3" max="12" style="text-align:center;">
                        </div>
                        
                        <div class="form-group">
                            <label>Premio al Completar (Ej. Bebida Gratis)</label>
                            <input type="text" id="stamps-reward" class="fidelio-input" placeholder="Ej. 1 Capuchino Gratis" value="Premio Gratis">
                        </div>
                    </div>
                </div>

                <!-- VIP TIERS SETTINGS -->
                <div class="accordion-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <div>
                            <h3 style="font-size: 16px; margin:0;"><i class="fa-solid fa-crown" style="color:var(--accent-violet); margin-right:8px;"></i> Niveles VIP Automáticos</h3>
                            <p style="font-size:12px; color:var(--text-muted); margin-top:4px;">Incentiva a tus clientes a gastar más subiéndolos de categoría automáticamente.</p>
                        </div>
                        <label class="toggle-switch">
                            <input type="checkbox" id="toggle-vip" checked>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                    
                    <div style="overflow-x: auto;">
                        <table class="crm-table">
                            <thead>
                                <tr>
                                    <th>Nivel VIP</th>
                                    <th>Gasto Acumulado (Mínimo)</th>
                                    <th>% Cashback VIP</th>
                                    <th>Beneficio Extra (Opcional)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong style="color: #B87333;">Bronce (Base)</strong></td>
                                    <td><input type="number" id="vip-bronce-min" class="fidelio-input" value="0" disabled style="width:100px; background:var(--bg-card); cursor:not-allowed;"> MXN</td>
                                    <td><input type="number" id="vip-bronce-cb" class="fidelio-input" value="5" style="width:80px;"> %</td>
                                    <td><input type="text" id="vip-bronce-perk" class="fidelio-input" placeholder="Ej. Ninguno" value="Beneficio Base"></td>
                                </tr>
                                <tr>
                                    <td><strong style="color: #C0C0C0;">Plata VIP</strong></td>
                                    <td><input type="number" id="vip-plata-min" class="fidelio-input" value="1000" style="width:100px;"> MXN</td>
                                    <td><input type="number" id="vip-plata-cb" class="fidelio-input" value="10" style="width:80px;"> %</td>
                                    <td><input type="text" id="vip-plata-perk" class="fidelio-input" placeholder="Ej. Refill Gratis" value="Beneficio Plata"></td>
                                </tr>
                                <tr>
                                    <td><strong style="color: #FFD700;">Oro VIP</strong></td>
                                    <td><input type="number" id="vip-oro-min" class="fidelio-input" value="3000" style="width:100px;"> MXN</td>
                                    <td><input type="number" id="vip-oro-cb" class="fidelio-input" value="15" style="width:80px;"> %</td>
                                    <td><input type="text" id="vip-oro-perk" class="fidelio-input" placeholder="Ej. Postre Gratis" value="Beneficio Oro"></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>
"""

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
insert_idx = -1
for i, line in enumerate(lines):
    if "<!-- ACCOUNT SETTINGS TAB -->" in line:
        insert_idx = i
        break
        
if insert_idx != -1:
    lines.insert(insert_idx, html_content)
    with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Injected tab-loyalty successfully.")
else:
    print("Could not find ACCOUNT SETTINGS TAB.")
