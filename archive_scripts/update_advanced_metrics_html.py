with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Heatmap container
target_heatmap = """                        <!-- Fake Heatmap Grid -->
                        <div style="display:flex; flex-direction:column; gap:4px;">
                            <!-- Header -->
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; text-align:center; font-size:11px; font-weight:700; color:var(--text-muted); margin-bottom:8px;">
                                <div></div><div>Lun</div><div>Mar</div><div>Mié</div><div>Jue</div><div>Vie</div><div>Sáb</div><div>Dom</div>
                            </div>
                            <!-- Rows -->
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px;">
                                <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">12 PM</div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.1);" title="Lun 12PM: Bajo"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);" title="Mar 12PM: Regular"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.1);" title="Mie 12PM: Bajo"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.3);" title="Jue 12PM: Medio"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.6);" title="Vie 12PM: Alto"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.8);" title="Sab 12PM: Muy Alto"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.5);" title="Dom 12PM: Alto"></div>
                            </div>
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px;">
                                <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">2 PM</div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.3);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.4);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.3);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.5);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.9);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,1.0);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.7);"></div>
                            </div>
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px;">
                                <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">6 PM</div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.1);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.1);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.4);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.8);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.9);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.4);"></div>
                            </div>
                            <div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px;">
                                <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">8 PM</div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.3);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.6);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,1.0);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,1.0);"></div>
                                <div class="heatmap-cell" style="background: rgba(76,29,149,0.2);"></div>
                            </div>
                        </div>"""

replacement_heatmap = """                        <!-- Real Heatmap Grid -->
                        <div id="heatmap-grid" style="display:flex; flex-direction:column; gap:4px;">
                            <div style="display:flex; justify-content:center; align-items:center; padding: 40px; color:var(--text-muted); font-size:13px;">Analizando visitas...</div>
                        </div>"""
html = html.replace(target_heatmap, replacement_heatmap)

# Fix Leaderboard
target_lb = """<div style="flex:1; display:flex; flex-direction:column; gap:12px; justify-content:center; align-items:center; color:var(--text-muted); font-size:14px;"><p>Aún no hay clientes top este mes.</p></div>"""
replacement_lb = """<div id="leaderboard-container" style="flex:1; display:flex; flex-direction:column; gap:12px; justify-content:flex-start; align-items:stretch; color:var(--text-muted); font-size:14px;"><p style="text-align:center; padding:20px 0;">Analizando clientes top...</p></div>"""
html = html.replace(target_lb, replacement_lb)

import re
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
