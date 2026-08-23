import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Clear the 3 rows in Rendimiento de Campañas
# Using regex to replace the content of the flex column containing the rows
start_camp = '<div style="display:flex; flex-direction:column; gap:8px;">'
end_camp = '</div>\n                </div>\n\n                <!-- 5. BOTTOM CHARTS ROW -->'

if start_camp in html and end_camp in html:
    # Find the block between start_camp and end_camp
    block_start_idx = html.find(start_camp) + len(start_camp)
    block_end_idx = html.find(end_camp)
    
    empty_camps = """
                        <div style="display:grid; grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr; align-items:center; padding:12px 16px; background:var(--bg-input); border-radius:8px; font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px;">
                            <div>Campaña (Push a Wallet)</div>
                            <div>Audiencia</div>
                            <div style="text-align:right;">Apertura</div>
                            <div style="text-align:right;">Conversión</div>
                            <div style="text-align:right;">Retorno ($)</div>
                        </div>
                        <div style="display: flex; justify-content: center; align-items: center; padding: 40px 0; color: var(--text-muted); font-size: 14px;">
                            <p style="margin: 0;">Aún no has enviado campañas.</p>
                        </div>
                    """
    
    html = html[:block_start_idx] + empty_camps + html[block_end_idx:]

# Zero out the charts (Adquisición vs Retención)
chart_container_start = '<div id="acquisition-chart-container"'
# We just need to find the container and empty its children
if chart_container_start in html:
    html = re.sub(
        r'<div id="acquisition-chart-container".*?</div>\s*</div>\s*</div>',
        """<div id="acquisition-chart-container" style="height: 250px; background: repeating-linear-gradient(0deg, transparent, transparent 49px, var(--border-glass) 49px, var(--border-glass) 50px); display:flex; align-items:center; justify-content:center; padding-top:20px; padding-bottom:0; overflow:hidden;">
            <p style="color:var(--text-muted); font-size:14px; margin:0;">No hay datos de ventas recientes.</p>
        </div>
    </div>""",
        html,
        flags=re.DOTALL
    )

# Zero out the Rewards Distribution
if "Premios Más Solicitados" in html:
    html = re.sub(
        r'<div style="flex:1; display:flex; flex-direction:column; gap:20px; justify-content:center;">.*?</div>\s*</div>\s*</div>\s*</section>',
        """<div style="flex:1; display:flex; flex-direction:column; gap:20px; justify-content:center; align-items:center; color:var(--text-muted);">
            <p style="margin:0; font-size:14px;">Aún no se han redimido premios.</p>
        </div>
    </div>
</section>""",
        html,
        flags=re.DOTALL
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Bottom half of Metrics zeroed out.")
