import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS replacement
old_css_start = "/* ANIMATED FIDELIO LOGO */"
old_css_end = "/* Logo Text */"

new_css = """/* ANIMATED FIDELIO LOGO (REAL) */
        .fidelio-svg-logo { height: 44px; width: auto; overflow: visible; display: flex; align-items: center; gap: 8px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        
        .fidelio-face { width: 44px; height: 44px; position: relative; margin-right: 2px; }
        
        /* Ojo Derecho (Guiño): Siempre cerrado, idéntico al logo original */
        .f-eye-right { stroke-dasharray: 100; stroke-dashoffset: 0; }
        
        /* Ojo Izquierdo: Empieza cerrado (curva), luego se abre a su forma original (óvalo) */
        .f-eye-left-closed { opacity: 1; animation: hideEyeLeft 2s forwards; animation-delay: 1.2s; }
        .f-eye-left-open { opacity: 0; transform-origin: 26px 36px; transform: scaleY(0); animation: openEyeLeft 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; animation-delay: 1.2s; }
        
        /* Sonrisa: Se dibuja desde el centro o de lado a lado */
        .f-smile-real { stroke-dasharray: 150; stroke-dashoffset: 150; animation: drawSmileReal 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards; animation-delay: 0.2s; }
        
        @keyframes hideEyeLeft { 0% { opacity: 1; } 100% { opacity: 0; display: none; } }
        @keyframes openEyeLeft { 0% { opacity: 0; transform: scaleY(0); } 100% { opacity: 1; transform: scaleY(1); } }
        @keyframes drawSmileReal { 0% { stroke-dashoffset: 150; } 100% { stroke-dashoffset: 0; } }
        
        /* Efecto de "parpadeo" ocasional para darle vida despues de abrirse */
        .f-eye-left-open {
            animation: openEyeLeft 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, blinkReal 5s infinite;
            animation-delay: 1.2s, 4s;
        }
        @keyframes blinkReal { 0%, 96%, 100% { transform: scaleY(1); } 98% { transform: scaleY(0.1); } }
        
        /* Logo Text */"""

pattern = re.compile(re.escape(old_css_start) + r'.*?' + re.escape(old_css_end), re.DOTALL)
html = pattern.sub(new_css, html)

# Fix Text CSS color to match real logo (#3200b0)
html = html.replace('background: linear-gradient(135deg, #4c1d95 0%, #8b5cf6 100%);', 'background: #3605a3;')
html = html.replace('.fidelio-text { font-size: 26px;', '.fidelio-text { font-size: 32px; font-weight: 800; letter-spacing: -1.5px;')

# HTML replacement
old_html_start = '<div class="fidelio-svg-logo">'
old_html_end = '</div>\n            </div>'

new_logo_html = """<div class="fidelio-svg-logo">
                    <svg class="fidelio-face" viewBox="0 0 100 100">
                        <!-- Left Eye Container -->
                        <g class="f-left-eye-container">
                            <!-- Closed state (an arch like the wink) -->
                            <path class="f-eye-left-closed" d="M 17 40 Q 25 28 33 40" fill="none" stroke="#3605a3" stroke-width="11" stroke-linecap="round"/>
                            <!-- Open state (The real oval from the logo) -->
                            <line class="f-eye-left-open" x1="25" y1="32" x2="25" y2="42" stroke="#3605a3" stroke-width="13" stroke-linecap="round"/>
                        </g>
                        
                        <!-- Right Eye (The real wink) -->
                        <path class="f-eye-right" d="M 52 40 Q 62 26 71 40" fill="none" stroke="#3605a3" stroke-width="11" stroke-linecap="round"/>
                        
                        <!-- The real Smile -->
                        <!-- Starts under left eye, ends under right eye -->
                        <path class="f-smile-real" d="M 15 57 C 15 88, 70 88, 70 57" fill="none" stroke="#3605a3" stroke-width="11" stroke-linecap="round"/>
                    </svg>
                    <div class="fidelio-text">Fidelio</div>
                </div>
            </div>"""

pattern2 = re.compile(re.escape(old_html_start) + r'.*?' + re.escape(old_html_end), re.DOTALL)
html = pattern2.sub(new_logo_html, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
