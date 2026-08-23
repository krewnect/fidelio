import re

with open('scanner.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add JS-Confetti and the Audio and Modal to the head/body
head_injection = """
    <!-- JS Confetti -->
    <script src="https://cdn.jsdelivr.net/npm/js-confetti@latest/dist/js-confetti.browser.js"></script>
</head>
"""

html = html.replace('</head>', head_injection)

body_injection = """
    <!-- STARBUCKS EFFECT OVERLAY -->
    <div id="starbucks-overlay" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.85); z-index:99999; backdrop-filter:blur(15px); align-items:center; justify-content:center; flex-direction:column; animation: fadeIn 0.3s ease forwards;">
        <div style="background:linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); width:120px; height:120px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:60px; color:white; margin-bottom:24px; box-shadow:0 10px 40px rgba(139,92,246,0.6); animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;">
            <i class="fa-solid fa-bell-concierge"></i>
        </div>
        <h1 style="color:white; font-size:48px; font-weight:900; margin:0 0 16px; text-align:center; text-shadow:0 4px 20px rgba(0,0,0,0.5);">¡Llegó <span id="starbucks-name" style="color:#fde047;">Cliente</span>!</h1>
        <p style="color:rgba(255,255,255,0.8); font-size:24px; font-weight:600; text-align:center; margin:0;">Salúdalo(a) por su nombre 🤝</p>
    </div>
    
    <!-- AUDIO PRELOAD (Using a clean, synthesized base64 chime to avoid cross-origin/loading issues) -->
    <audio id="chime-sound" preload="auto">
        <source src="data:audio/mp3;base64,//NExAAAAANIAAAAAExBTUUzLjEwMKqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq//NExAAAAANIAAAAAExBTUUzLjEwMKqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq" type="audio/mpeg">
    </audio>
    
    <div class="app-container">"""

html = html.replace('<div class="app-container">', body_injection)

# 2. Trigger it in renderClientProfile
target_js = "document.getElementById('c-name').textContent = data.full_name || data.name || 'Cliente';"
replacement_js = """
            const cName = data.full_name || data.name || 'Cliente';
            document.getElementById('c-name').textContent = cName;
            
            // THE STARBUCKS EFFECT
            try {
                // Play Sound
                // Note: We'll use the browser's speech synthesis for an even more magical effect!
                const msg = new SpeechSynthesisUtterance("Bienvenido " + cName.split(' ')[0]);
                msg.lang = 'es-MX';
                msg.rate = 1.1;
                window.speechSynthesis.speak(msg);
                
                // Show Overlay
                const overlay = document.getElementById('starbucks-overlay');
                document.getElementById('starbucks-name').textContent = cName.split(' ')[0];
                overlay.style.display = 'flex';
                
                // Confetti
                if (window.JSConfetti) {
                    const jsConfetti = new window.JSConfetti();
                    jsConfetti.addConfetti({ emojis: ['✨', '🌟', '🎉', '🔥'], confettiNumber: 60 });
                }
                
                // Hide after 3.5 seconds
                setTimeout(() => {
                    overlay.style.opacity = '0';
                    setTimeout(() => overlay.style.display = 'none', 400);
                }, 3500);
                
            } catch(e) { console.error("Starbucks effect failed:", e); }
"""

html = html.replace(target_js, replacement_js)

with open('scanner.html', 'w', encoding='utf-8') as f:
    f.write(html)
