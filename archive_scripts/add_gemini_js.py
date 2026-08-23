with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_js = """
window.triggerRealAIMagicDesign = async function() {
    const btn = document.getElementById('btn-real-ai');
    const originalText = btn.innerHTML;
    
    // UI Loading state
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Analizando...';
    btn.style.opacity = '0.8';
    btn.style.pointerEvents = 'none';
    
    const iphone = document.querySelector('.iphone-pro-mockup');
    if(iphone) iphone.style.animation = "spinY 1.5s infinite cubic-bezier(0.175, 0.885, 0.32, 1.275)";
    
    if (typeof showToast === 'function') showToast("Gemini AI está analizando tu negocio...", "info");

    const industry = document.getElementById('business-category-input') ? document.getElementById('business-category-input').value : 'General';
    const businessName = document.getElementById('rest-name') ? document.getElementById('rest-name').value : 'Mi Negocio';

    try {
        const token = localStorage.getItem('merchant_token');
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ industry, businessName })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('/api/ai/magic-builder', reqOpts);
        
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.error || 'Error al conectar con Gemini API');
        }
        
        const strategy = await res.json();
        
        // Update DOM inputs
        if (document.getElementById('color-primary')) document.getElementById('color-primary').value = strategy.primaryColor || '#1e1b4b';
        if (document.getElementById('color-accent')) document.getElementById('color-accent').value = strategy.accentColor || '#8b5cf6';
        if (document.getElementById('unified-reward')) document.getElementById('unified-reward').value = strategy.reward || 'Premio Sorpresa';
        if (document.getElementById('stamps-reward')) document.getElementById('stamps-reward').value = strategy.reward || 'Premio Sorpresa';
        if (document.getElementById('unified-desc')) document.getElementById('unified-desc').value = strategy.instruction || 'Acumula visitas para ganar.';
        if (document.getElementById('stamps-total')) document.getElementById('stamps-total').value = strategy.stampsTotal || 5;
        if (document.getElementById('program-type-select')) document.getElementById('program-type-select').value = 'stamps';

        // Show Tip
        let tipBox = document.getElementById('ai-mkt-tip');
        if (!tipBox) {
            tipBox = document.createElement('div');
            tipBox.id = 'ai-mkt-tip';
            tipBox.style = 'margin-top:20px; background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.3); border-radius:12px; padding:16px; color:#4c1d95; font-size:13px; font-weight:600; line-height:1.5; animation:fadeIn 0.5s;';
            if (btn && btn.parentElement && btn.parentElement.parentElement) {
                btn.parentElement.parentElement.appendChild(tipBox);
            }
        }
        tipBox.innerHTML = `🤖 <b>Gemini AI:</b> ${strategy.tip}`;

        // Force UI update
        if (typeof updatePassRender === 'function') updatePassRender();

        if (typeof showToast === 'function') showToast("¡Estrategia Gemini Aplicada!", "success");
        
        try {
            if (window.JSConfetti) {
                const jsConfetti = new window.JSConfetti();
                jsConfetti.addConfetti({ emojis: ['🧠', '✨', '⚡️'], confettiNumber: 40 });
            }
        } catch(e) {}

    } catch (err) {
        console.error("Gemini Error:", err);
        if (typeof showToast === 'function') showToast(err.message || "Error al generar estrategia con Gemini.", "error");
    } finally {
        btn.innerHTML = originalText;
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
        if(iphone) iphone.style.animation = "";
    }
};
"""

js += new_js

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
