with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

btn_html = """
<div style="margin-top: 20px; background: linear-gradient(135deg, #4c1d95, #8b5cf6); padding: 20px; border-radius: 12px; text-align: center; color: white;">
    <h2 style="color: white; margin-bottom: 10px;">¡El Magic Engine ya está conectado!</h2>
    <p style="margin-bottom: 15px;">Para configurar las automatizaciones de clima y los Flash Drops, haz clic en el siguiente botón:</p>
    <button onclick="
        document.querySelectorAll('.tab-content').forEach(c => { c.classList.remove('active'); c.style.display = 'none'; });
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        const tb = document.getElementById('tab-builder');
        if(tb) { tb.classList.add('active'); tb.style.display = 'block'; }
        setTimeout(() => {
            const bot = document.getElementById('magic-weather-promo');
            if (bot) {
                bot.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }, 100);
    " style="background: #10b981; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <i class="fa-solid fa-wand-magic-sparkles"></i> Ir al Panel del Magic Engine
    </button>
</div>
"""

# Insert it at the top of the dashboard main view
if "Ir al Panel del Magic Engine" not in html:
    html = html.replace('<!-- REVENUE GRAPH -->', btn_html + '\n<!-- REVENUE GRAPH -->')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
