import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix ROI text
target_roi = """<p style="opacity: 0.9; margin-top: 8px; max-width: 450px; font-size: 15px; line-height: 1.6;">Por cada $1 invertido en Fidelio, tus clientes han generado $3.42 en ventas adicionales y retención comprobada.</p>"""
replacement_roi = """<p id="metric-roi-desc" style="opacity: 0.9; margin-top: 8px; max-width: 450px; font-size: 15px; line-height: 1.6;">Monitoreando el impacto económico real de tus programas de lealtad.</p>"""
html = html.replace(target_roi, replacement_roi)

# Fix Live Ticker
target_ticker = """                            <div style="display:flex; flex-direction:column; gap:12px; padding: 10px 0;">
                                <div style="display:flex; align-items:center; gap:12px; font-size:13px; opacity:0.6;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:var(--bg-input); display:flex; align-items:center; justify-content:center; font-size:12px;"><i class="fa-solid fa-wallet"></i></div>
                                    <div style="flex:1;"><strong>Roberto O.</strong> usó $45 cashback</div>
                                    <div style="font-size:11px; color:var(--text-muted);">Hace 2m</div>
                                </div>
                                <div style="display:flex; align-items:center; gap:12px; font-size:13px;">
                                    <div style="width:32px; height:32px; border-radius:50%; background: var(--bg-input); color:var(--accent-violet); display:flex; align-items:center; justify-content:center; font-size:12px;"><i class="fa-solid fa-qrcode"></i></div>
                                    <div style="flex:1;"><strong>Ana G.</strong> escaneó mesa #4 (+120 pts)</div>
                                    <div style="font-size:11px; color:var(--text-muted);">Hace 5m</div>
                                </div>
                                <div style="display:flex; align-items:center; gap:12px; font-size:13px; opacity:0.8;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:rgba(245, 158, 11, 0.1); color:var(--accent-violet); display:flex; align-items:center; justify-content:center; font-size:12px;"><i class="fa-solid fa-crown"></i></div>
                                    <div style="flex:1;"><strong>Carlos R.</strong> subió a VIP Oro</div>
                                    <div style="font-size:11px; color:var(--text-muted);">Hace 14m</div>
                                </div>
                                <div style="display:flex; align-items:center; gap:12px; font-size:13px; opacity:0.5;">
                                    <div style="width:32px; height:32px; border-radius:50%; background:var(--bg-input); display:flex; align-items:center; justify-content:center; font-size:12px;"><i class="fa-solid fa-envelope-open"></i></div>
                                    <div style="flex:1;">24 clientes abrieron promo Cumpleaños</div>
                                    <div style="font-size:11px; color:var(--text-muted);">Hace 30m</div>
                                </div>
                            </div>"""

replacement_ticker = """                            <div id="live-activity-feed" style="display:flex; flex-direction:column; gap:12px; padding: 10px 0;">
                                <div style="text-align: center; color: var(--text-muted); font-size: 13px; padding: 20px 0;">No hay actividad reciente.</div>
                            </div>"""
html = html.replace(target_ticker, replacement_ticker)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
