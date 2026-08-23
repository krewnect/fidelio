import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- 2. MICRO METRICS GRID -->'
end_marker = '<!-- 3. BEHAVIOR & CAMPAIGNS (Advanced Data) -->'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

new_grid = """<!-- 2. MICRO METRICS GRID -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px;" class="stagger-2">
                    
                    <div class="stat-card" style="padding: 20px !important;">
                        <div style="font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                            <span style="white-space: nowrap;">Base de Lealtad</span>
                            <i class="fa-solid fa-users" style="color: #7C3AED;"></i>
                        </div>
                        <div id="metric-adv-loyalty" style="font-size: 28px; font-weight: 800; color: #111827; letter-spacing:-1px;">0</div>
                        <div style="font-size: 12px; color: #10B981; font-weight: 600; margin-top: 8px; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
                            <i class="fa-solid fa-arrow-trend-up"></i> Calculando...
                        </div>
                    </div>

                    <div class="stat-card" style="padding: 20px !important;">
                        <div style="font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                            <span style="white-space: nowrap;">Ticket Promedio</span>
                            <i class="fa-solid fa-receipt" style="color: #7C3AED;"></i>
                        </div>
                        <div id="metric-adv-ticket" style="font-size: 28px; font-weight: 800; color: #111827; letter-spacing:-1px;">$0.00</div>
                        <div style="font-size: 12px; color: #6B7280; font-weight: 500; margin-top: 8px; white-space: nowrap;">
                            Basado en historial
                        </div>
                    </div>

                    <div class="stat-card" style="padding: 20px !important;">
                        <div style="font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                            <span style="white-space: nowrap;">Tasa Redención</span>
                            <i class="fa-solid fa-fire" style="color: #F59E0B;"></i>
                        </div>
                        <div id="metric-adv-redemption" style="font-size: 28px; font-weight: 800; color: #111827; letter-spacing:-1px;">0%</div>
                        <div style="font-size: 12px; color: #6B7280; font-weight: 500; margin-top: 8px; white-space: nowrap;">
                            Basado en premios
                        </div>
                    </div>

                    <div class="stat-card" style="padding: 20px !important;">
                        <div style="font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                            <span style="white-space: nowrap;">Frecuencia</span>
                            <i class="fa-solid fa-rotate-right" style="color: #06B6D4;"></i>
                        </div>
                        <div id="metric-adv-freq" style="font-size: 28px; font-weight: 800; color: #111827; letter-spacing:-1px;">0x<span style="font-size:16px; color:#6B7280; font-weight:500;">/mes</span></div>
                        <div style="font-size: 12px; color: #6B7280; font-weight: 500; margin-top: 8px; white-space: nowrap;">
                            Últimos 30 días
                        </div>
                    </div>
                </div>

                """

new_html = html[:start_idx] + new_grid + html[end_idx:]

# Remove the CSS fix from earlier since we don't need it now that we rebuilt the cards inline
new_html = new_html.replace("""
/* Fix padding squish in micro metrics grid */
.stagger-2 .stat-card {
    padding: 20px !important;
}
.stagger-2 .stat-label {
    font-size: 12px !important;
    white-space: nowrap !important;
}
""", "")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

