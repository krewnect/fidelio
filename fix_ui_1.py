import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove "Campaña Asociada" entirely
target_camp_assoc = r'<label class="premium-label">CAMPAÑA DE FIDELIZACIÓN ASOCIADA</label>.*?<select id="link-campaign-select" class="premium-input">.*?<option value="">-- Selecciona una campaña --</option>.*?</select>'
html = re.sub(target_camp_assoc, '', html, flags=re.DOTALL)
html = html.replace('<p style="font-size: 13px; color: var(--text-muted); margin-top: 8px;">Asocia este diseño a un programa específico. El diseño será único para la campaña seleccionada.</p>', '')

# 2. Fix the "CONSULTAS SELLOS" bug
# Original: ACUMULA <span id="render-stamps-total-text">10</span> SELLOS<br>Y OBTÉN TU RECOMPENSA
html = html.replace('ACUMULA <span id="render-stamps-total-text">10</span> SELLOS<br>Y OBTÉN TU RECOMPENSA', 
                    'ACUMULA <span id="render-stamps-total-text">10</span><br>Y OBTÉN TU RECOMPENSA')
# But wait, my JS sets renderStampsTotalText.textContent = "10 CONSULTAS". So it will say "ACUMULA 10 CONSULTAS Y OBTEN...". This is perfect!

# 3. Make the pass look incredibly vibrant, not sober!
# Add some background blobs inside the pass!
pass_bg_blobs = """
                                        <!-- Vibrant Background Shapes for the Pass -->
                                        <div style="position:absolute; top:-50px; right:-50px; width:200px; height:200px; background:radial-gradient(circle, var(--pass-primary) 0%, transparent 70%); opacity:0.15; border-radius:50%; z-index:0; pointer-events:none;"></div>
                                        <div style="position:absolute; bottom:-100px; left:-50px; width:250px; height:250px; background:radial-gradient(circle, var(--pass-primary) 0%, transparent 70%); opacity:0.1; border-radius:50%; z-index:0; pointer-events:none;"></div>
"""
# Find the start of the front card content and inject blobs
html = html.replace('<!-- Top row: Logo and "10 SELLOS" -->', pass_bg_blobs + '\n                                            <!-- Top row: Logo and "10 SELLOS" -->')

# Change the text color of "render-name" to be more readable
html = html.replace('id="render-name" style="font-weight: 800; font-size: 20px; color: #111827; letter-spacing: -0.5px;"',
                    'id="render-name" style="font-weight: 800; font-size: 20px; color: var(--text-main); letter-spacing: -0.5px; z-index:1; position:relative;"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
