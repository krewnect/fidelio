import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

anchor = '<div class="apple-section">\n                            <div class="apple-section-header"><i class="fa-solid fa-hourglass-half"></i> Vigencia del Programa</div>'

new_blocks = """
                        <!-- MAGIC ENGINE: AUTOPILOT -->
                        <div class="apple-section plan-business-only">
                            <div class="apple-section-header" style="display:flex; justify-content:space-between; align-items:center;">
                                <span><i class="fa-solid fa-robot"></i> Autopilot (Deep Tech)</span>
                                <span class="menu-badge" style="font-size: 9px; padding: 2px 6px; background: linear-gradient(135deg, #111827, #374151); color: #fff; border-radius: 4px;">BUSINESS</span>
                            </div>
                            <p style="font-size: 13px; color: #64748b; margin-bottom: 16px;">
                                Automatizaciones inteligentes basadas en eventos del mundo real gestionadas por el Magic Engine.
                            </p>
                            <div style="display: flex; flex-direction: column; gap: 16px;">
                                <label style="display: flex; align-items: center; gap: 12px; cursor: pointer; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0;">
                                    <input type="checkbox" id="magic-weather-promo" style="width: 18px; height: 18px; accent-color: #8b5cf6;">
                                    <div>
                                        <span style="font-size: 14px; font-weight: 700; color: #1e293b; display: block;">Activar Promo de Lluvia (Weather API)</span>
                                        <span style="font-size: 12px; color: #64748b;">Lanza notificaciones Push automáticas si empieza a llover cerca de la sucursal.</span>
                                    </div>
                                </label>
                                
                                <button type="button" onclick="testFlashDrop()" class="fidelio-btn-primary" style="background: #ef4444 !important; width: 100%;">
                                    <i class="fa-solid fa-bolt"></i> Disparar Flash Drop Masivo
                                </button>
                                
                                <button type="button" onclick="testMagicIssue()" class="fidelio-btn-primary" style="background: linear-gradient(135deg, #111827, #374151) !important; width: 100%;">
                                    <i class="fa-solid fa-wand-magic-sparkles"></i> Simular Emisión de Tarjeta (Magic Engine)
                                </button>
                            </div>
                        </div>

"""

if anchor in html:
    html = html.replace(anchor, new_blocks + anchor)
    print("Injected Autopilot section")
else:
    print("WARNING: Could not find anchor")

# Also inject the JS handler functions at the end of the file
js_injection = """
    <!-- MAGIC ENGINE TEST HANDLERS -->
    <script>
    window.testFlashDrop = async function() {
        if (!window.MagicEngine) return alert("MagicEngine no está cargado.");
        try {
            window.showToast("Iniciando Flash Drop Masivo vía Magic Engine...", "info");
            const res = await window.MagicEngine.triggerFlashDrop('camp_local_test');
            window.showToast("Flash Drop ejecutado: " + JSON.stringify(res), "success");
        } catch(e) {
            window.showToast("Error en Flash Drop: " + e.message, "error");
        }
    };
    
    window.testMagicIssue = async function() {
        if (!window.MagicEngine) return alert("MagicEngine no está cargado.");
        try {
            window.showToast("Emitiendo tarjeta vía Magic Engine...", "info");
            
            const config = {
                progress: 5,
                tier: 'oro',
                weather: document.getElementById('magic-weather-promo')?.checked ? 'rain' : 'clear',
                mode: document.querySelector('input[name="loyalty_mode"]:checked')?.value || 'stamps'
            };
            
            const res = await window.MagicEngine.issueCard('user_test_123', config);
            console.log("Respuesta binaria del Engine:", res);
            window.showToast("¡Tarjeta emitida exitosamente! (Revisa la consola)", "success");
        } catch(e) {
            window.showToast("Error emitiendo tarjeta: " + e.message, "error");
        }
    };
    </script>
</body>"""

html = html.replace('</body>', js_injection)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
