import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The CSS for the animation
logo_css = """
        /* ANIMATED FIDELIO LOGO */
        .fidelio-svg-logo { height: 40px; width: auto; overflow: visible; display: flex; align-items: center; gap: 8px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        
        .fidelio-face { width: 36px; height: 36px; position: relative; }
        
        /* Ojo Izquierdo: Empieza cerrado (arco), se queda cerrado porque es un guiño ;) */
        .f-eye-left { stroke-dasharray: 100; stroke-dashoffset: 0; animation: blink 4s infinite; }
        
        /* Ojo Derecho: Empieza cerrado (arco abajo), luego se abre a un círculo (guiño) y se queda así */
        .f-eye-right-closed { opacity: 1; animation: hideEyeClosed 2s forwards; animation-delay: 1.5s; }
        .f-eye-right-open { opacity: 0; transform-origin: 65px 35px; transform: scale(0); animation: showEyeOpen 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; animation-delay: 1.5s; }
        
        /* Sonrisa: Empieza chiquita y se hace grande */
        .f-smile { stroke-dasharray: 100; stroke-dashoffset: 100; animation: drawSmile 1s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; animation-delay: 0.5s; }
        
        @keyframes hideEyeClosed { 0% { opacity: 1; } 100% { opacity: 0; display: none; } }
        @keyframes showEyeOpen { 0% { opacity: 0; transform: scale(0); } 100% { opacity: 1; transform: scale(1.2); } }
        @keyframes drawSmile { 0% { stroke-dashoffset: 100; } 100% { stroke-dashoffset: 0; } }
        @keyframes blink { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }
        
        /* Logo Text */
        .fidelio-text { font-size: 26px; font-weight: 900; letter-spacing: -1px; background: linear-gradient(135deg, #4c1d95 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: slideIn 1s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; opacity:0; transform: translateX(-10px); animation-delay: 0.8s; }
        @keyframes slideIn { to { opacity: 1; transform: translateX(0); } }
"""

if "ANIMATED FIDELIO LOGO" not in html:
    html = html.replace('/* SIDEBAR */', logo_css + '\n        /* SIDEBAR */')

# The HTML for the logo
animated_logo_html = """            <div class="sidebar-brand" style="cursor: pointer;" onclick="location.reload()">
                <div class="fidelio-svg-logo">
                    <svg class="fidelio-face" viewBox="0 0 100 100">
                        <!-- Left Eye (Always closed) -->
                        <path class="f-eye-left" d="M 20 45 Q 35 30 50 45" fill="none" stroke="#8b5cf6" stroke-width="8" stroke-linecap="round"/>
                        
                        <!-- Right Eye -->
                        <!-- Closed version (disappears) -->
                        <path class="f-eye-right-closed" d="M 50 45 Q 65 30 80 45" fill="none" stroke="#8b5cf6" stroke-width="8" stroke-linecap="round"/>
                        <!-- Open version (appears to wink) -->
                        <circle class="f-eye-right-open" cx="65" cy="40" r="8" fill="#8b5cf6"/>
                        
                        <!-- Smile -->
                        <path class="f-smile" d="M 20 65 Q 50 95 80 65" fill="none" stroke="#8b5cf6" stroke-width="8" stroke-linecap="round"/>
                    </svg>
                    <div class="fidelio-text">Fidelio</div>
                </div>
            </div>"""

target_sidebar_brand = """            <div class="sidebar-brand">
                <img src="./fidelio_logo_purple.png?v=4" alt="Fidelio Logo" style="height: 44px; width: auto;" />
            </div>"""

html = html.replace(target_sidebar_brand, animated_logo_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
