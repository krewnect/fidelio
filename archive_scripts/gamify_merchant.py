import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                        <small id="header-business-category">Profesional</small>"""
replacement = """                        <small id="header-business-category" style="display:flex; align-items:center; gap:6px;">
                            <span>Profesional</span>
                            <span style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 2px 6px; border-radius: 8px; font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 0 10px rgba(245,158,11,0.4); animation: pulseGlow 2s infinite;">Lv. 1 Maestro</span>
                        </small>"""

html = html.replace(target, replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
