import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 3D Floating Apple Wallet preview and Siri Orb loading
wow_css = """
/* PROJECT WOW: ULTRA PREMIUM STYLING */
body {
    background-color: #f8fafc;
    background-image: 
        radial-gradient(at 40% 20%, hsla(250,100%,74%,0.15) 0px, transparent 50%),
        radial-gradient(at 80% 0%, hsla(189,100%,56%,0.15) 0px, transparent 50%),
        radial-gradient(at 0% 50%, hsla(355,100%,93%,0.1) 0px, transparent 50%);
    background-attachment: fixed;
}

/* Glassmorphism Cards */
.stats-grid > div, .gemini-insight-panel, .content-panel, .settings-card {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(20px) saturate(1.5) !important;
    -webkit-backdrop-filter: blur(20px) saturate(1.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.8) !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.03), inset 0 1px 0 rgba(255,255,255,1) !important;
}

/* 3D Wallet Preview */
.iphone-pro-mockup {
    transform: scale(0.65) perspective(1000px) rotateY(-10deg) rotateX(5deg) !important;
    box-shadow: 
        -20px 20px 40px rgba(0,0,0,0.3), 
        -40px 40px 80px rgba(0,0,0,0.15),
        inset 0 0 10px rgba(255,255,255,0.2),
        inset -5px 0 15px rgba(0,0,0,0.5) !important;
    transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.iphone-pro-mockup:hover {
    transform: scale(0.68) perspective(1000px) rotateY(0deg) rotateX(0deg) !important;
}

/* Glowing Siri/Gemini Orb */
.ai-orb-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
}
.ai-orb {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6, #ec4899, #3b82f6);
    background-size: 200% 200%;
    animation: orbPulse 3s ease-in-out infinite, gradientShift 5s linear infinite;
    box-shadow: 0 0 40px #8b5cf6, 0 0 80px #ec4899, inset 0 0 20px #fff;
    margin-bottom: 24px;
}

@keyframes orbPulse {
    0% { transform: scale(0.95); box-shadow: 0 0 30px #8b5cf6, 0 0 60px #ec4899; }
    50% { transform: scale(1.05); box-shadow: 0 0 60px #8b5cf6, 0 0 100px #ec4899; }
    100% { transform: scale(0.95); box-shadow: 0 0 30px #8b5cf6, 0 0 60px #ec4899; }
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.ai-status-text {
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: pulseGlow 2s infinite;
}

/* Premium Inputs */
.apple-input, .fidelio-input {
    background: rgba(255,255,255,0.8) !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
    backdrop-filter: blur(10px) !important;
}
.apple-input:focus, .fidelio-input:focus {
    background: #fff !important;
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 4px rgba(139,92,246,0.1), inset 0 2px 4px rgba(0,0,0,0.02) !important;
}
"""

if "/* PROJECT WOW: ULTRA PREMIUM STYLING */" not in html:
    html = html.replace('</style>', wow_css + '\n</style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Add magical AI loading sequence to dashboard_v2.js
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

ai_loading_old = r"textEl\.innerHTML = '<i class=\"fa-solid fa-circle-notch fa-spin\"></i> Analizando industria y diseñando estrategia\.\.\.';[\s\S]*?textEl\.scrollIntoView\(\{ behavior: 'smooth', block: 'center' \}\);"

ai_loading_new = """
    // PROJECT WOW: Apple-Siri Style Loading Sequence
    textEl.innerHTML = `
        <div class="ai-orb-container">
            <div class="ai-orb"></div>
            <div class="ai-status-text" id="ai-loading-step">Iniciando motor cognitivo...</div>
            <p style="color:#64748b; font-size:14px; margin-top:8px;">Gemini 1.5 Flash está diseñando tu campaña.</p>
        </div>
    `;
    textEl.scrollIntoView({ behavior: 'smooth', block: 'center' });

    const steps = [
        "Analizando comportamiento en tu industria...",
        "Diseñando psicología de recompensas...",
        "Seleccionando pantones de color óptimos...",
        "Compilando renderizado para Apple Wallet..."
    ];
    let stepIdx = 0;
    const stepInterval = setInterval(() => {
        const stepEl = document.getElementById('ai-loading-step');
        if(stepEl && stepIdx < steps.length) {
            stepEl.innerText = steps[stepIdx];
            stepIdx++;
        }
    }, 1200);
"""

if "PROJECT WOW: Apple-Siri Style Loading Sequence" not in js:
    # We find the trigger function for real AI
    js = re.sub(r"textEl\.innerHTML = '<i class=\"fa-solid fa-circle-notch fa-spin\"></i> Analizando industria.*?\n.*?(?=\n)", ai_loading_new, js, flags=re.DOTALL)
    
    # We also inject the clear interval at the bottom of the try/catch
    clear_interval = "\n        if(typeof stepInterval !== 'undefined') clearInterval(stepInterval);\n"
    js = js.replace("const data = await res.json();", clear_interval + "        const data = await res.json();")
    js = js.replace("console.error(err);", clear_interval + "        console.error(err);")


# 3. Create fireworks/confetti on success to give that dopamine hit
success_magic = """
        // DO WOW CONFETTI
        if(typeof confetti === 'function') {
            confetti({ particleCount: 150, spread: 100, origin: { y: 0.6 }, colors: [cPri, cAcc, '#ffffff'] });
        } else {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js';
            script.onload = () => confetti({ particleCount: 150, spread: 100, origin: { y: 0.6 }, colors: [strategy.primaryColor||'#8b5cf6', strategy.accentColor||'#3b82f6', '#ffffff'] });
            document.head.appendChild(script);
        }
"""
if "// DO WOW CONFETTI" not in js:
    js = js.replace("showToast(\"¡Campaña Mágica generada con éxito!\", \"success\");", "showToast(\"¡Campaña Mágica generada con éxito!\", \"success\");\n" + success_magic)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

