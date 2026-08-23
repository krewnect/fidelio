with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                        <div style="position: relative; z-index: 2;">
                            <span style="text-transform: uppercase; letter-spacing: 2px; font-size: 12px; opacity: 0.8; font-weight: 700; display:flex; align-items:center; gap:8px;">
                                <i class="fa-solid fa-chart-line"></i> Clientes Activos (Últimos 30 días)
                            </span>
                            <h2 style="font-size: 64px; margin: 8px 0 0 0; color: white; font-weight: 900; letter-spacing:-1px;">
                                <span id="metric-roi" style="animation: numberCounter 1s ease-out forwards;">0%</span>
                            </h2>
                            <p id="metric-roi-desc" style="opacity: 0.9; margin-top: 8px; max-width: 450px; font-size: 15px; line-height: 1.6;">Porcentaje de tu base de datos que ha generado una visita o compra recientemente. Medimos datos 100% reales.</p>
                        </div>"""

replacement = """                        <div style="position: relative; z-index: 2;">
                            <span style="text-transform: uppercase; letter-spacing: 2px; font-size: 12px; opacity: 0.8; font-weight: 700; display:flex; align-items:center; gap:8px;">
                                <i class="fa-solid fa-chart-line"></i> Retorno de Inversión (ROI)
                            </span>
                            <h2 style="font-size: 64px; margin: 8px 0 0 0; color: white; font-weight: 900; letter-spacing:-1px;">
                                <span id="metric-roi" style="animation: numberCounter 1s ease-out forwards;">0%</span>
                            </h2>
                            <p id="metric-roi-desc" style="opacity: 0.9; margin-top: 8px; max-width: 450px; font-size: 15px; line-height: 1.6;">Por cada $1 MXN invertido en tu suscripción Fidelio, tus clientes han generado <strong style="color:white; font-size:16px;">$<span id="metric-roi-ratio">0.00</span></strong> en ingresos atribuibles.</p>
                        </div>"""

html = html.replace(target, replacement)

import re
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target_js = """        // Tasa de Actividad (reemplazo del ROI)
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
        }"""

replacement_js = """        // Retorno de Inversión (ROI) Matemático
        const mRoi = document.getElementById('metric-roi');
        const mRoiRatio = document.getElementById('metric-roi-ratio');
        if(mRoi && mRoiRatio) {
            // Asumimos un costo base del software (ej. Plan Professional a 999/mes)
            const fidelioCost = window.merchantData.tier === 'business' ? 2499 : 999;
            
            if (totalSales === 0) {
                mRoi.textContent = '0%';
                mRoiRatio.textContent = '0.00';
            } else {
                const roiPercent = Math.round(((totalSales - fidelioCost) / fidelioCost) * 100);
                // Si es negativo pero hay ventas, al menos mostramos el avance, si es positivo lo mostramos con +
                mRoi.textContent = (roiPercent > 0 ? '+' : '') + roiPercent + '%';
                
                const ratio = (totalSales / fidelioCost).toFixed(2);
                mRoiRatio.textContent = ratio;
            }
        }"""

js = js.replace(target_js, replacement_js)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
