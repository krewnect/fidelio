import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                        <div>
                            <h1 style="font-size: 24px; font-weight: 800; letter-spacing: -1px; color: #111827;">✨ Creador de Tarjetas Mágico</h1>
                            <p style="font-size: 14px; color: #6b7280; margin-top: 8px;">Configura la tarjeta digital que tus clientes instalarán en sus teléfonos. Todo cambio se refleja al instante.</p>
                        </div>"""

magical_header = """                        <div>
                            <h1 style="font-size: 24px; font-weight: 800; letter-spacing: -1px; color: #111827;">✨ Creador de Tarjetas Mágico</h1>
                            <p style="font-size: 14px; color: #6b7280; margin-top: 8px;">Configura la tarjeta digital que tus clientes instalarán en sus teléfonos. Todo cambio se refleja al instante.</p>
                            
                            <div style="margin-top:20px; background: linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%); padding:20px; border-radius:16px; color:white; display:flex; align-items:center; gap:16px; box-shadow:0 10px 30px rgba(76,29,149,0.3); border:1px solid rgba(255,255,255,0.1);">
                                <div style="font-size:32px; filter:drop-shadow(0 0 10px rgba(255,255,255,0.5)); animation: float 3s ease-in-out infinite;">🤖</div>
                                <div style="flex:1;">
                                    <h4 style="margin:0 0 4px; font-size:16px; font-weight:800;">Copiloto de Diseño IA</h4>
                                    <p style="margin:0; font-size:12px; opacity:0.8;">¿Sin inspiración? Deja que la IA configure los colores, textos y reglas por ti.</p>
                                </div>
                                <button onclick="triggerAIMagicDesign()" style="background:white; color:#4c1d95; border:none; padding:10px 16px; border-radius:12px; font-weight:800; cursor:pointer; transition:transform 0.2s; box-shadow:0 4px 15px rgba(0,0,0,0.2);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                                    ¡Haz Magia! ✨
                                </button>
                            </div>
                        </div>"""

html = html.replace(target, magical_header)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

magic_js = """
window.triggerAIMagicDesign = function() {
    if (typeof showToast === 'function') showToast("IA generando diseño...", "info");
    
    const iphone = document.querySelector('.iphone-pro-mockup');
    if(iphone) iphone.style.animation = "spinY 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
    
    setTimeout(() => {
        const palettes = [
            { primary: '#0f172a', accent: '#3b82f6', name: 'Tech / Moderno', reward: '50% Off en tu Próxima Compra' },
            { primary: '#451a03', accent: '#d97706', name: 'Café Artesanal', reward: 'Bebida Grande Gratis' },
            { primary: '#831843', accent: '#ec4899', name: 'Beauty Spa', reward: 'Manicure de Cortesía' }
        ];
        const randomPalette = palettes[Math.floor(Math.random() * palettes.length)];
        
        state.colorPrimary = randomPalette.primary;
        state.colorAccent = randomPalette.accent;
        state.stampsReward = randomPalette.reward;
        state.restaurantName = randomPalette.name;
        
        if (document.getElementById('color-primary')) document.getElementById('color-primary').value = state.colorPrimary;
        if (document.getElementById('color-accent')) document.getElementById('color-accent').value = state.colorAccent;
        if (document.getElementById('unified-reward')) document.getElementById('unified-reward').value = state.stampsReward;
        if (document.getElementById('rest-name')) document.getElementById('rest-name').value = state.restaurantName;
        
        if (typeof updatePassRender === 'function') updatePassRender();
        if (typeof showToast === 'function') showToast("¡Diseño Mágico Aplicado!", "success");
        
        try {
            if (window.JSConfetti) {
                const jsConfetti = new window.JSConfetti();
                jsConfetti.addConfetti({ emojis: ['✨', '🎨', '🚀'], confettiNumber: 40 });
            }
        } catch(e) {}
        
        if(iphone) setTimeout(() => iphone.style.animation = "none", 800);
    }, 800);
};
"""

if "window.triggerAIMagicDesign =" not in js:
    js = js.replace('function updatePassRender() {', magic_js + '\nfunction updatePassRender() {')

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
