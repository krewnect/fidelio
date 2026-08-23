import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

anchor = '<label class="role-card plan-business-only" id="loyalty-mode-custom">'

new_modes = """
                        <!-- MAGIC ENGINE MODES -->
                        <label class="role-card plan-business-only" id="loyalty-mode-monedero" style="position: relative;">
                            <span class="menu-badge" style="position: absolute; top: 12px; right: 12px; font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff;">MAGIC ENGINE</span>
                            <input type="radio" name="loyalty_mode" value="monedero" style="display:none;">
                            <div class="role-icon" style="color:var(--accent-violet); background: rgba(255, 255, 255, 0.1);"><i class="fa-solid fa-coins"></i></div>
                            <div class="role-info">
                                <h4>Monedero Digital</h4>
                                <p>Dinero recargable o puntos que el cliente usa como efectivo.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>

                        <label class="role-card plan-business-only" id="loyalty-mode-multipass" style="position: relative;">
                            <span class="menu-badge" style="position: absolute; top: 12px; right: 12px; font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff;">MAGIC ENGINE</span>
                            <input type="radio" name="loyalty_mode" value="multipass" style="display:none;">
                            <div class="role-icon" style="color:var(--accent-violet); background: rgba(255, 255, 255, 0.1);"><i class="fa-solid fa-ticket"></i></div>
                            <div class="role-info">
                                <h4>Multipass (Visitas)</h4>
                                <p>Paquetes prepagados de clases o visitas que se van ponchando.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>

                        <label class="role-card plan-business-only" id="loyalty-mode-membresia" style="position: relative;">
                            <span class="menu-badge" style="position: absolute; top: 12px; right: 12px; font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff;">MAGIC ENGINE</span>
                            <input type="radio" name="loyalty_mode" value="membresia" style="display:none;">
                            <div class="role-icon" style="color:var(--accent-violet); background: rgba(255, 255, 255, 0.1);"><i class="fa-solid fa-id-card-clip"></i></div>
                            <div class="role-info">
                                <h4>Membresía</h4>
                                <p>Acceso por vigencia de tiempo (Mensual/Anual) con estatus.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>

                        <label class="role-card plan-business-only" id="loyalty-mode-giftcard" style="position: relative;">
                            <span class="menu-badge" style="position: absolute; top: 12px; right: 12px; font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff;">MAGIC ENGINE</span>
                            <input type="radio" name="loyalty_mode" value="giftcard" style="display:none;">
                            <div class="role-icon" style="color:var(--accent-violet); background: rgba(255, 255, 255, 0.1);"><i class="fa-solid fa-gift"></i></div>
                            <div class="role-info">
                                <h4>Gift Card Oculta</h4>
                                <p>Tarjeta de regalo transferible con esteganografía offline.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>

                        <label class="role-card plan-business-only" id="loyalty-mode-streak" style="position: relative;">
                            <span class="menu-badge" style="position: absolute; top: 12px; right: 12px; font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff;">MAGIC ENGINE</span>
                            <input type="radio" name="loyalty_mode" value="streak" style="display:none;">
                            <div class="role-icon" style="color:var(--accent-violet); background: rgba(255, 255, 255, 0.1);"><i class="fa-solid fa-fire"></i></div>
                            <div class="role-info">
                                <h4>Rachas (Streaks)</h4>
                                <p>Modo supervivencia: Premia a clientes por compras consecutivas.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>

                        <label class="role-card plan-business-only" id="loyalty-mode-lootbox" style="position: relative;">
                            <span class="menu-badge" style="position: absolute; top: 12px; right: 12px; font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff;">MAGIC ENGINE</span>
                            <input type="radio" name="loyalty_mode" value="lootbox" style="display:none;">
                            <div class="role-icon" style="color:var(--accent-violet); background: rgba(255, 255, 255, 0.1);"><i class="fa-solid fa-box-open"></i></div>
                            <div class="role-info">
                                <h4>Cajas Botín (Random)</h4>
                                <p>Entrega premios variables y aleatorios para maximizar dopamina.</p>
                            </div>
                            <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                        </label>

"""

if anchor in html:
    html = html.replace(anchor, new_modes + anchor)
    print("Injected new loyalty modes")
else:
    print("WARNING: Could not find anchor")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
