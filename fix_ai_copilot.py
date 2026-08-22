import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """window.triggerAIMagicDesign = function() {
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
        
        setTimeout(() => { if(iphone) iphone.style.animation = ""; }, 800);
    }, 400);
};"""

replacement = """window.triggerAIMagicDesign = function() {
    if (typeof showToast === 'function') showToast("IA Analizando tu industria...", "info");
    
    const iphone = document.querySelector('.iphone-pro-mockup');
    if(iphone) iphone.style.animation = "spinY 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
    
    setTimeout(() => {
        let aiTip = "";
        let newStamps = 10;
        
        if (state.category === 'medico') {
            state.colorPrimary = '#064e3b'; // Medical Green
            state.colorAccent = '#10b981';
            state.stampsReward = 'Consulta de Seguimiento Gratis';
            state.dynamicDesc = 'Tu salud es lo más importante. Premia tu constancia.';
            newStamps = 5;
            aiTip = "💡 Tip MKT IA: En el sector médico, las metas largas frustran al paciente. Reduje la meta a 5 consultas. ¡Esto aumenta el retorno un 42%!";
        } else if (state.category === 'belleza') {
            state.colorPrimary = '#4c1d95'; // Purple
            state.colorAccent = '#d946ef'; // Pink
            state.stampsReward = 'Masaje Capilar o Tratamiento VIP';
            state.dynamicDesc = 'Mantén tu estilo perfecto y obtén recompensas exclusivas.';
            newStamps = 8;
            aiTip = "💡 Tip MKT IA: En estética, es mejor regalar servicios complementarios (como un masaje) en lugar de descuentos. Aumenta el ticket promedio.";
        } else if (state.category === 'clases') {
            state.colorPrimary = '#1e3a8a'; // Sport Blue
            state.colorAccent = '#ef4444'; // Red
            state.stampsReward = 'Sesión Personalizada Extra';
            state.dynamicDesc = 'No te rindas. Cada clase te acerca a tu meta.';
            newStamps = 10;
            aiTip = "💡 Tip MKT IA: En deportes, la constancia se premia con más valor. Regalar una sesión personalizada fortalece la retención a largo plazo.";
        } else {
            state.colorPrimary = '#0f172a';
            state.colorAccent = '#8b5cf6';
            state.stampsReward = 'Cupón de $500 MXN';
            state.dynamicDesc = 'Acumula compras y desbloquea nivel VIP.';
            newStamps = 10;
            aiTip = "💡 Tip MKT IA: Para retail/general, el cashback directo en cupones genera compras impulsivas un 25% más rápido.";
        }
        
        if (document.getElementById('color-primary')) document.getElementById('color-primary').value = state.colorPrimary;
        if (document.getElementById('color-accent')) document.getElementById('color-accent').value = state.colorAccent;
        if (document.getElementById('unified-reward')) document.getElementById('unified-reward').value = state.stampsReward;
        if (document.getElementById('unified-desc')) document.getElementById('unified-desc').value = state.dynamicDesc;
        if (document.getElementById('stamps-total')) document.getElementById('stamps-total').value = newStamps;
        
        if (typeof updatePassRender === 'function') updatePassRender();
        
        // Show AI Tip in a beautiful alert or toast
        if (typeof showToast === 'function') {
            showToast("✨ Estrategia de Marketing Aplicada", "success");
        }
        
        // Inject Tip into UI
        let tipBox = document.getElementById('ai-mkt-tip');
        if (!tipBox) {
            tipBox = document.createElement('div');
            tipBox.id = 'ai-mkt-tip';
            tipBox.style.marginTop = '16px';
            tipBox.style.padding = '16px';
            tipBox.style.background = 'rgba(139, 92, 246, 0.1)';
            tipBox.style.border = '1px solid rgba(139, 92, 246, 0.3)';
            tipBox.style.borderRadius = '12px';
            tipBox.style.color = '#4c1d95';
            tipBox.style.fontSize = '13px';
            tipBox.style.fontWeight = '600';
            tipBox.style.lineHeight = '1.5';
            tipBox.style.animation = 'fadeInUp 0.5s';
            
            // Find the copilot card and append it
            const magicButton = document.querySelector('button[onclick="triggerAIMagicDesign()"]');
            if (magicButton && magicButton.parentElement && magicButton.parentElement.parentElement) {
                magicButton.parentElement.parentElement.appendChild(tipBox);
            }
        }
        tipBox.innerHTML = aiTip;
        
        try {
            if (window.JSConfetti) {
                const jsConfetti = new window.JSConfetti();
                jsConfetti.addConfetti({ emojis: ['📈', '💡', '🧠'], confettiNumber: 30 });
            }
        } catch(e) {}
        
        setTimeout(() => { if(iphone) iphone.style.animation = ""; }, 800);
    }, 600);
};"""

if target in js:
    js = js.replace(target, replacement)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("SUCCESS")
else:
    print("TARGET NOT FOUND. FALLING BACK TO RE.SUB")
    # Backup replace just in case exact match fails
    js = re.sub(r'window\.triggerAIMagicDesign = function\(\) \{.*?\};', replacement, js, flags=re.DOTALL)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
