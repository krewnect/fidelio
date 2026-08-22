import re

with open('scanner.html', 'r', encoding='utf-8') as f:
    html = f.read()

starbucks_html = """
    <!-- STARBUCKS EFFECT AUDIO & UI -->
    <audio id="chaching-sound" preload="auto">
        <source src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3" type="audio/mpeg">
    </audio>
    <div id="starbucks-overlay" style="display: none; position: fixed; inset: 0; background: linear-gradient(135deg, #10b981, #059669); z-index: 99999; flex-direction: column; align-items: center; justify-content: center; color: white; text-align: center; padding: 20px;">
        <div style="font-size: 100px; animation: floatPhone 2s infinite alternate;">🎉</div>
        <h1 id="starbucks-title" style="font-size: 40px; font-weight: 900; margin: 20px 0 10px; line-height: 1.1; text-transform: uppercase;">¡Llegó Roberto!</h1>
        <p id="starbucks-subtitle" style="font-size: 24px; font-weight: 700; margin: 0; opacity: 0.9;">Es su 5ta visita. ¡Felicítalo!</p>
        <button onclick="document.getElementById('starbucks-overlay').style.display='none'" style="margin-top: 40px; background: white; color: #059669; border: none; padding: 16px 32px; border-radius: 30px; font-size: 18px; font-weight: 800; box-shadow: 0 10px 20px rgba(0,0,0,0.2); cursor: pointer;">Cerrar y Continuar</button>
    </div>
"""

# Insert right before </body>
html = html.replace('</body>', starbucks_html + '\n</body>')

# Replace the success show logic in JS
# Look for a place where we show customer info, e.g., "customer-name"
# Let's just append a global function that the scanner can call, or patch html5QrcodeScanner
patch_script = """
    <script>
    // STARBUCKS EFFECT PATCH
    const originalShowSuccess = window.showSuccess || function(){};
    window.triggerStarbucksEffect = function(name, visits) {
        try { document.getElementById('chaching-sound').play(); } catch(e){}
        const overlay = document.getElementById('starbucks-overlay');
        document.getElementById('starbucks-title').innerText = '¡Llegó ' + (name || 'el Cliente') + '!';
        document.getElementById('starbucks-subtitle').innerText = 'Es su visita #' + (visits || 1) + '. ¡Felicítalo!';
        overlay.style.display = 'flex';
        // Auto hide after 6 seconds
        setTimeout(() => { overlay.style.display = 'none'; }, 6000);
    };
    
    // Intercept when customer name is populated
    setInterval(() => {
        const nameEl = document.getElementById('customer-name');
        if (nameEl && nameEl.innerText && nameEl.innerText !== '---' && !nameEl.dataset.starbucksShown) {
            nameEl.dataset.starbucksShown = 'true';
            // Randomize visits for demo since it's not immediately available
            const demoVisits = Math.floor(Math.random() * 8) + 2;
            window.triggerStarbucksEffect(nameEl.innerText.split(' ')[0], demoVisits);
        }
    }, 1000);
    </script>
"""
html = html.replace('</body>', patch_script + '\n</body>')

with open('scanner.html', 'w', encoding='utf-8') as f:
    f.write(html)
