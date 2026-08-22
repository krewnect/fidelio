with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                        <div style="position: relative; z-index: 2;">
                            <span style="text-transform: uppercase; letter-spacing: 2px; font-size: 12px; opacity: 0.8; font-weight: 700; display:flex; align-items:center; gap:8px;">
                                <i class="fa-solid fa-chart-line"></i> Retorno de Inversión Estimado
                            </span>
                            <h2 style="font-size: 64px; margin: 8px 0 0 0; color: white; font-weight: 900; letter-spacing:-1px;">
                                <span id="metric-roi" style="animation: numberCounter 1s ease-out forwards;">0%</span>
                            </h2>
                            <p id="metric-roi-desc" style="opacity: 0.9; margin-top: 8px; max-width: 450px; font-size: 15px; line-height: 1.6;">Monitoreando el impacto económico real de tus programas de lealtad.</p>
                        </div>"""

replacement = """                        <div style="position: relative; z-index: 2;">
                            <span style="text-transform: uppercase; letter-spacing: 2px; font-size: 12px; opacity: 0.8; font-weight: 700; display:flex; align-items:center; gap:8px;">
                                <i class="fa-solid fa-chart-line"></i> Clientes Activos (Últimos 30 días)
                            </span>
                            <h2 style="font-size: 64px; margin: 8px 0 0 0; color: white; font-weight: 900; letter-spacing:-1px;">
                                <span id="metric-roi" style="animation: numberCounter 1s ease-out forwards;">0%</span>
                            </h2>
                            <p id="metric-roi-desc" style="opacity: 0.9; margin-top: 8px; max-width: 450px; font-size: 15px; line-height: 1.6;">Porcentaje de tu base de datos que ha generado una visita o compra recientemente. Medimos datos 100% reales.</p>
                        </div>"""

html = html.replace(target, replacement)

import re
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target_js = """        // Loyalty Revenue (ROI panel)
        const mLoyaltyRev = document.getElementById('metric-loyalty-revenue');
        if(mLoyaltyRev) {
            mLoyaltyRev.innerHTML = `+$${totalSales.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})} <span style="font-size:16px; font-weight:600; opacity:0.8; color:white;">MXN</span>`;
        }"""

replacement_js = """        // Tasa de Actividad (reemplazo del ROI)
        const mActiveRate = document.getElementById('metric-roi');
        if(mActiveRate) {
            if(totalCustomers === 0) {
                mActiveRate.textContent = '0%';
            } else {
                const now = new Date();
                const thirtyDaysAgo = new Date(now.getTime() - (30 * 24 * 60 * 60 * 1000));
                
                const activeCustomerIds = new Set();
                state.transactions.forEach(t => {
                    if(new Date(t.created_at) >= thirtyDaysAgo) {
                        activeCustomerIds.add(t.customer_id);
                    }
                });
                
                const activeRate = Math.round((activeCustomerIds.size / totalCustomers) * 100);
                mActiveRate.textContent = `${activeRate}%`;
            }
        }
        
        // Loyalty Revenue (ROI panel)
        const mLoyaltyRev = document.getElementById('metric-loyalty-revenue');
        if(mLoyaltyRev) {
            mLoyaltyRev.innerHTML = `+$${totalSales.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})} <span style="font-size:16px; font-weight:600; opacity:0.8; color:white;">MXN</span>`;
        }"""

js = js.replace(target_js, replacement_js)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
