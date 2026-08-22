import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add the missing CSS class for builder-preview-area to force it to the right
target_css = r'\.tab-builder-container \{ display: flex; height: calc\(100vh - 100px\); overflow: hidden; background: #f8fafc; margin: -24px; \}'
replacement_css = """.tab-builder-container { display: flex; height: calc(100vh - 100px); overflow: hidden; background: #f8fafc; margin: -24px; }
                    .builder-preview-area { flex: 1; display: flex; align-items: center; justify-content: center; position: relative; background: #f1f5f9; height: 100%; border-left: 1px solid #e2e8f0; overflow: hidden; }
                    .builder-sidebar { overflow-y: auto; padding-right: 12px; }"""
html = re.sub(target_css, replacement_css, html)

# Fix the iPhone Mockup bottom cutoff properly
target_iphone = r'\.iphone-pro-mockup \{ width: 380px; height: 820px; border-radius: 55px; background: #000; position: relative; box-shadow: 0 0 0 4px #1a1a1a, 0 0 0 5px #2a2a2a, 0 0 0 6px #3a3a3a, 0 30px 60px rgba\(0,0,0,0\.4\), inset 0 0 8px rgba\(255,255,255,0\.2\); transform: scale\(0\.65\); transform-origin: center; display:flex; flex-direction:column; overflow:hidden; \}'
replacement_iphone = """.iphone-pro-mockup { width: 380px; min-height: 850px; padding-bottom: 30px; border-radius: 55px; background: #000; position: relative; box-shadow: 0 0 0 4px #1a1a1a, 0 0 0 5px #2a2a2a, 0 0 0 6px #3a3a3a, 0 30px 60px rgba(0,0,0,0.4), inset 0 0 8px rgba(255,255,255,0.2); transform: scale(0.65); transform-origin: center; display:flex; flex-direction:column; overflow:hidden; }"""
html = html.replace(target_iphone, replacement_iphone)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
