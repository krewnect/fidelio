import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX THE BUTTON CSS (ADD .fidelio-btn-primary)
css_fix = """
/* CRITICAL BUTTON FIX */
.fidelio-btn-primary, button.fidelio-btn-primary {
    background: #7C3AED !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    box-shadow: 0 2px 4px rgba(124, 58, 237, 0.15) !important;
    transition: all 0.2s ease !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    cursor: pointer !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif !important;
}
.fidelio-btn-primary:hover {
    background: #6D28D9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
}
"""
if "/* CRITICAL BUTTON FIX */" not in html:
    html = html.replace('</style>', css_fix + '\n</style>', 1)

# 2. FIX THE DARK BANNER IN DASHBOARD (Change #111827 to White/Purple)
dark_banner = 'class="content-panel" style="background: #111827 !important; border: none !important; color: white !important; margin-bottom: 32px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px;"'
light_banner = 'class="content-panel" style="background: #FFFFFF !important; border: 1px solid #C4B5FD !important; margin-bottom: 32px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px; box-shadow: 0 4px 20px rgba(139,92,246,0.08) !important;"'
html = html.replace(dark_banner, light_banner)

# Fix the texts inside that banner from white/grey to purple/black
html = html.replace('color: #FFFFFF; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-earth-americas" style="color: #8B5CF6;"></i> Tu Portal Público', 'color: #4C1D95; display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-earth-americas" style="color: #8B5CF6;"></i> Tu Portal Público')
html = html.replace('<p style="color: #9CA3AF; font-size: 14px; margin: 0; max-width: 500px; line-height:1.6;">Comparte este enlace', '<p style="color: #6B7280; font-size: 14px; margin: 0; max-width: 500px; line-height:1.6;">Comparte este enlace')
html = html.replace('background: rgba(255,255,255,0.05); padding: 8px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);', 'background: #F9FAFB; padding: 8px; border-radius: 12px; border: 1px solid #E5E7EB;')
html = html.replace('color: #E5E7EB;" id="landing-link-display"', 'color: #6D28D9; font-weight: 600;" id="landing-link-display"')

# 3. FIX THE "ACTUALIZAR" AND "VER TODO" BUTTONS
# The inline styles were overriding the CSS or breaking it. Replace them with pure secondary classes.
html = html.replace('<button class="fidelio-btn-primary" style="background: #F3F4F6 !important; color: #111827 !important;" onclick="window.location.reload()"><i class="fa-solid fa-rotate-right"></i> Actualizar</button>', '<button class="fidelio-btn-secondary" onclick="window.location.reload()"><i class="fa-solid fa-rotate-right"></i> Actualizar</button>')
html = html.replace('<button class="fidelio-btn-primary" style="background:#F3F4F6 !important; color:#111827 !important; padding:6px 12px; font-size:12px; border-radius:8px;">Ver todo</button>', '<button class="fidelio-btn-secondary" style="padding:6px 12px; font-size:12px;">Ver todo</button>')

# 4. FIX LOGO CLICK JS
html = html.replace('onclick="document.querySelector(\'.nav-tab[data-tab=\\\'tab-home\\\']\').click()"', 'onclick="if(typeof switchTab === \'function\'){switchTab(\'home\')}else{location.reload()}"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
