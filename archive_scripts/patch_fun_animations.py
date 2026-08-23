import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Flip card automatically when selecting QR location
old_qr_location = """                                        <label class="fidelio-btn-primary" style="flex: 1; margin: 0; cursor: pointer; background: #f8fafc !important; color: #111827 !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 12px !important;">
                                            <input type="radio" name="magic_qr_location" value="traditional" checked style="margin-right: 8px;">
                                            Modo Tradicional (Frente)
                                        </label>
                                        <label class="fidelio-btn-primary" style="flex: 1; margin: 0; cursor: pointer; background: #f8fafc !important; color: #111827 !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 12px !important;">
                                            <input type="radio" name="magic_qr_location" value="clean_nfc" style="margin-right: 8px;">
                                            Modo Limpio (Reverso)
                                        </label>"""

new_qr_location = """                                        <label class="fidelio-btn-primary" style="flex: 1; margin: 0; cursor: pointer; background: #f8fafc !important; color: #111827 !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 12px !important;" onclick="document.getElementById('pass-render').style.transform = 'rotateY(0deg)';">
                                            <input type="radio" name="magic_qr_location" value="traditional" checked style="margin-right: 8px;">
                                            Modo Tradicional (Frente)
                                        </label>
                                        <label class="fidelio-btn-primary" style="flex: 1; margin: 0; cursor: pointer; background: #f8fafc !important; color: #111827 !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 12px !important;" onclick="document.getElementById('pass-render').style.transform = 'rotateY(180deg)';">
                                            <input type="radio" name="magic_qr_location" value="clean_nfc" style="margin-right: 8px;">
                                            Modo Limpio (Reverso)
                                        </label>"""

if "rotateY" not in old_qr_location:
    html = html.replace(old_qr_location, new_qr_location)

# 2. Add Apple Wallet Success Overlay to the iPhone Screen
old_iphone_screen = """                                <!-- THE PASS -->"""
new_iphone_screen = """                                <!-- APPLE WALLET SUCCESS OVERLAY -->
                                <div id="wallet-success-overlay" style="position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); backdrop-filter:blur(10px); z-index:999; display:flex; flex-direction:column; align-items:center; justify-content:center; opacity:0; pointer-events:none; transition: opacity 0.4s ease;">
                                    <div style="background: white; border-radius: 50%; width: 80px; height: 80px; display:flex; align-items:center; justify-content:center; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); transform: scale(0.5); transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);" id="wallet-check-icon">
                                        <i class="fa-solid fa-check" style="font-size: 40px; color: #10b981;"></i>
                                    </div>
                                    <h3 style="color:white; font-size: 24px; font-weight: 700; margin:0; text-align:center;">Agregada a<br>Apple Wallet</h3>
                                </div>
                                
                                <!-- THE PASS -->"""

if "wallet-success-overlay" not in html:
    html = html.replace(old_iphone_screen, new_iphone_screen)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 3. Update testMagicIssue in index.html to trigger the animation
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_magic_issue = """    window.testMagicIssue = async function() {
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
            window.showToast("¡Tarjeta emitida exitosamente!", "success");
            alert("¡Simulación Exitosa! El Magic Engine procesó la orden correctamente.\\n\\nEsto significa que si hubiera un iPhone conectado, la tarjeta se instalaría en este momento con las funciones Deep Tech activadas.");
        } catch(e) {
            window.showToast("Error emitiendo tarjeta: " + e.message, "error");
        }
    };"""

new_magic_issue = """    window.testMagicIssue = async function() {
        if (!window.MagicEngine) return alert("MagicEngine no está cargado.");
        try {
            // Animar el botón
            const btn = document.querySelector('button[onclick="testMagicIssue()"]');
            const originalHtml = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generando criptografía Apple...';
            btn.disabled = true;
            
            const config = {
                progress: 5,
                tier: 'oro',
                weather: document.getElementById('magic-weather-promo')?.checked ? 'rain' : 'clear',
                mode: document.querySelector('input[name="loyalty_mode"]:checked')?.value || 'stamps'
            };
            
            const res = await window.MagicEngine.issueCard('user_test_123', config);
            
            // Animación Apple Wallet en el mockup
            const overlay = document.getElementById('wallet-success-overlay');
            const icon = document.getElementById('wallet-check-icon');
            
            // Efecto de brinco en el iPhone
            const iphone = document.querySelector('.iphone-pro-mockup');
            iphone.style.transition = 'transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            iphone.style.transform = 'scale(0.8) perspective(1000px) rotateY(0deg) rotateX(0deg)';
            
            setTimeout(() => {
                overlay.style.opacity = '1';
                setTimeout(() => {
                    icon.style.transform = 'scale(1)';
                    // Play a soft "ding" sound using Web Audio API to simulate Apple Pay success
                    try {
                        const ctx = new (window.AudioContext || window.webkitAudioContext)();
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(880, ctx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(1760, ctx.currentTime + 0.1);
                        gain.gain.setValueAtTime(0, ctx.currentTime);
                        gain.gain.linearRampToValueAtTime(0.5, ctx.currentTime + 0.05);
                        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
                        osc.start(ctx.currentTime);
                        osc.stop(ctx.currentTime + 0.5);
                    } catch(e) { console.log("Audio not supported"); }
                }, 100);
            }, 300);
            
            setTimeout(() => {
                overlay.style.opacity = '0';
                icon.style.transform = 'scale(0.5)';
                // Restaurar el iPhone a su inclinación CSS original
                iphone.style.transform = '';
            }, 3000);
            
            btn.innerHTML = originalHtml;
            btn.disabled = false;
        } catch(e) {
            window.showToast("Error emitiendo tarjeta: " + e.message, "error");
        }
    };"""

if "wallet-success-overlay" in html and "Animación Apple Wallet" not in html:
    html = html.replace(old_magic_issue, new_magic_issue)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected fun animations.")
else:
    print("Already injected or failed.")
