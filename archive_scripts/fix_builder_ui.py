import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the boring builder CSS
old_css_start = "/* Premium Clean Builder */"
old_css_end = "/* PHOTOREALISTIC IPHONE PRO MOCKUP */"

new_css = """/* Premium Clean Builder Redesigned */
                    .tab-builder-container { display: flex; height: calc(100vh - 100px); overflow: hidden; background: #f8fafc; margin: -24px; }
                    
                    .builder-sidebar { 
                        width: 55%; 
                        max-width: 750px; 
                        background: #f8fafc; 
                        overflow-y: auto; 
                        padding: 40px; 
                        display:flex; 
                        flex-direction:column; 
                        gap:32px; 
                        z-index:10; 
                        border-right: 1px solid rgba(0,0,0,0.05);
                    }
                    
                    /* The magical card groups */
                    .builder-card {
                        background: #ffffff;
                        border-radius: 24px;
                        padding: 32px;
                        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05);
                        border: 1px solid rgba(0,0,0,0.02);
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }
                    .builder-card:hover {
                        box-shadow: 0 15px 50px -10px rgba(0,0,0,0.08);
                    }
                    
                    .premium-label { 
                        font-size: 13px; 
                        font-weight: 700; 
                        color: #475569; 
                        margin-bottom: 10px; 
                        display: flex; 
                        align-items: center;
                        gap: 8px;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }
                    
                    .premium-input { 
                        width: 100%; 
                        padding: 16px 20px; 
                        border: 2px solid transparent; 
                        background: #f1f5f9;
                        border-radius: 16px; 
                        font-family: var(--font-main); 
                        font-size: 15px; 
                        font-weight: 500;
                        color: #1e293b;
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
                    }
                    .premium-input:focus { 
                        outline: none; 
                        background: #ffffff;
                        border-color: #8b5cf6; 
                        box-shadow: 0 0 0 4px rgba(139,92,246,0.1); 
                        transform: translateY(-2px);
                    }
                    .premium-input::placeholder { color: #94a3b8; font-weight:400; }
                    
                    .premium-section-title { 
                        font-size: 22px; 
                        font-weight: 800; 
                        color: #0f172a; 
                        margin-bottom: 8px; 
                        letter-spacing:-0.5px;
                        display: flex;
                        align-items: center;
                        gap: 12px;
                    }
                    .premium-section-desc { 
                        font-size: 14px; 
                        color: #64748b; 
                        margin-bottom: 24px; 
                        line-height: 1.5; 
                    }
                    
                    /* Hide old dividers */
                    .premium-divider { display: none; }
                    
                    /* Modern File Dropzone */
                    .file-dropzone {
                        background: #f8fafc;
                        border: 2px dashed #cbd5e1;
                        border-radius: 20px;
                        padding: 40px 20px;
                        transition: all 0.3s;
                    }
                    .file-dropzone:hover {
                        background: #f1f5f9;
                        border-color: #8b5cf6;
                        transform: scale(1.02);
                    }
                    
                    /* Modern Color Pickers */
                    .color-picker-wrapper { 
                        display:flex; 
                        gap:16px; 
                        align-items:center; 
                        background: #f8fafc;
                        padding: 12px 20px;
                        border-radius: 16px;
                    }
                    .premium-color-input { 
                        -webkit-appearance: none; 
                        border: none; 
                        width: 48px; 
                        height: 48px; 
                        border-radius: 50%; 
                        cursor: pointer; 
                        padding: 0; 
                        box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
                        transition: transform 0.2s;
                    }
                    .premium-color-input:hover { transform: scale(1.1); }
                    .premium-color-input::-webkit-color-swatch-wrapper { padding: 0; }
                    .premium-color-input::-webkit-color-swatch { border: none; border-radius: 50%; border: 3px solid white; }
                    
                    """

# Find and replace the CSS
pattern = re.compile(re.escape(old_css_start) + r'.*?' + re.escape(old_css_end), re.DOTALL)
html = pattern.sub(new_css + old_css_end, html)

# Now, wrap the sections in .builder-card
# 1. Reglas
html = html.replace('<div style="background: rgba(139, 92, 246, 0.05); padding: 24px; border-radius: 16px; border: 1px dashed rgba(139, 92, 246, 0.3);">', '<div class="builder-card" style="position:relative; overflow:hidden;"><div style="position:absolute; top:0; left:0; width:6px; height:100%; background:linear-gradient(to bottom, #8b5cf6, #3b82f6);"></div>')
html = html.replace('<div class="premium-section-title" style="color: var(--accent-violet);">1. Reglas de Recompensa</div>', '<div class="premium-section-title"><i class="fa-solid fa-gift" style="color:#8b5cf6;"></i> 1. El Premio</div>')

# 2. Identidad
html = html.replace('<!-- 1. Identidad -->\n                        <div>', '<!-- 1. Identidad -->\n                        <div class="builder-card">')
html = html.replace('<div class="premium-section-title">Identidad de Marca</div>', '<div class="premium-section-title"><i class="fa-solid fa-store" style="color:#f59e0b;"></i> 2. Identidad del Negocio</div>')

# 3. Apariencia Visual
html = html.replace('<!-- 2. Apariencia -->\n                        <div>', '<!-- 2. Apariencia -->\n                        <div class="builder-card">')
html = html.replace('<div class="premium-section-title">Apariencia Visual</div>', '<div class="premium-section-title"><i class="fa-solid fa-palette" style="color:#ec4899;"></i> 3. Colores y Apariencia</div>')

# 4. Texto e Instrucciones
html = html.replace('<!-- 3. Textos -->\n                        <div>', '<!-- 3. Textos -->\n                        <div class="builder-card">')
html = html.replace('<div class="premium-section-title">Texto e Instrucciones</div>', '<div class="premium-section-title"><i class="fa-solid fa-align-left" style="color:#10b981;"></i> 4. Instrucciones del Pase</div>')

# 5. Enlaces
html = html.replace('<!-- 4. Botón de Wallet -->\n                        <div>', '<!-- 4. Botón de Wallet -->\n                        <div class="builder-card" style="margin-bottom:60px;">')
html = html.replace('<div class="premium-section-title">Enlaces (Dorso de Tarjeta)</div>', '<div class="premium-section-title"><i class="fa-solid fa-link" style="color:#3b82f6;"></i> 5. Enlaces Rápidos</div>')

# Make inputs more modern
html = html.replace('<label class="premium-label">Nombre de la Campaña / Tarjeta</label>', '<label class="premium-label"><i class="fa-solid fa-tag text-muted"></i> Nombre de la Campaña</label>')
html = html.replace('<label class="premium-label">Giro o Categoría (Opcional)</label>', '<label class="premium-label"><i class="fa-solid fa-briefcase text-muted"></i> Categoría del Negocio</label>')
html = html.replace('<label class="premium-label">¿Qué premio van a ganar?</label>', '<label class="premium-label"><i class="fa-solid fa-trophy text-muted"></i> ¿Qué premio van a ganar?</label>')
html = html.replace('<label class="premium-label">Instrucciones Breves</label>', '<label class="premium-label"><i class="fa-solid fa-comment-dots text-muted"></i> Instrucciones Breves</label>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
