import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- 2. MICRO METRICS GRID -->'
end_marker = '<!-- 3. BEHAVIOR & CAMPAIGNS (Advanced Data) -->'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

new_grid = """<!-- 2. MICRO METRICS GRID -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px;" class="stagger-2">
                    
                    <div class="stat-card" style="padding: 24px !important; display: flex !important; flex-direction: column !important; align-items: flex-start !important; justify-content: center !important;">
                        <div style="font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important; width: 100% !important;">
                            <span style="white-space: nowrap !important;">Base de Lealtad</span>
                            <i class="fa-solid fa-users" style="color: #7C3AED;"></i>
                        </div>
                        <div id="metric-adv-loyalty" style="font-size: 32px !important; font-weight: 800 !important; color: #111827 !important; letter-spacing: -1px !important; margin-bottom: 4px !important; width: 100% !important; text-align: left !important;">0</div>
                        <div style="font-size: 12px !important; color: #10B981 !important; font-weight: 600 !important; white-space: nowrap !important; display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: flex-start !important; gap: 4px !important; width: 100% !important;">
                            <i class="fa-solid fa-arrow-trend-up"></i> Calculando...
                        </div>
                    </div>

                    <div class="stat-card" style="padding: 24px !important; display: flex !important; flex-direction: column !important; align-items: flex-start !important; justify-content: center !important;">
                        <div style="font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important; width: 100% !important;">
                            <span style="white-space: nowrap !important;">Ticket Promedio</span>
                            <i class="fa-solid fa-receipt" style="color: #7C3AED;"></i>
                        </div>
                        <div id="metric-adv-ticket" style="font-size: 32px !important; font-weight: 800 !important; color: #111827 !important; letter-spacing: -1px !important; margin-bottom: 4px !important; width: 100% !important; text-align: left !important;">$0.00</div>
                        <div style="font-size: 12px !important; color: #6B7280 !important; font-weight: 500 !important; white-space: nowrap !important; display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: flex-start !important; width: 100% !important;">
                            Basado en historial
                        </div>
                    </div>

                    <div class="stat-card" style="padding: 24px !important; display: flex !important; flex-direction: column !important; align-items: flex-start !important; justify-content: center !important;">
                        <div style="font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important; width: 100% !important;">
                            <span style="white-space: nowrap !important;">Tasa Redención</span>
                            <i class="fa-solid fa-fire" style="color: #F59E0B;"></i>
                        </div>
                        <div id="metric-adv-redemption" style="font-size: 32px !important; font-weight: 800 !important; color: #111827 !important; letter-spacing: -1px !important; margin-bottom: 4px !important; width: 100% !important; text-align: left !important;">0%</div>
                        <div style="font-size: 12px !important; color: #6B7280 !important; font-weight: 500 !important; white-space: nowrap !important; display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: flex-start !important; width: 100% !important;">
                            Basado en premios
                        </div>
                    </div>

                    <div class="stat-card" style="padding: 24px !important; display: flex !important; flex-direction: column !important; align-items: flex-start !important; justify-content: center !important;">
                        <div style="font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-bottom: 8px; display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: space-between !important; width: 100% !important;">
                            <span style="white-space: nowrap !important;">Frecuencia</span>
                            <i class="fa-solid fa-rotate-right" style="color: #06B6D4;"></i>
                        </div>
                        <div id="metric-adv-freq" style="font-size: 32px !important; font-weight: 800 !important; color: #111827 !important; letter-spacing: -1px !important; margin-bottom: 4px !important; width: 100% !important; text-align: left !important;">0x<span style="font-size:16px; color:#6B7280; font-weight:500;">/mes</span></div>
                        <div style="font-size: 12px !important; color: #6B7280 !important; font-weight: 500 !important; white-space: nowrap !important; display: flex !important; flex-direction: row !important; align-items: center !important; justify-content: flex-start !important; width: 100% !important;">
                            Últimos 30 días
                        </div>
                    </div>
                </div>

                """

new_html = html[:start_idx] + new_grid + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

