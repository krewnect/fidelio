with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        // Retorno de Inversión (ROI) Matemático
        const mRoi = document.getElementById('metric-roi');
        const mRoiRatio = document.getElementById('metric-roi-ratio');
        if(mRoi && mRoiRatio) {
            // Asumimos un costo base del software
            const fidelioCost = window.merchantData.tier === 'business' ? 2499 : 999;"""

replacement = """        // Retorno de Inversión (ROI) Matemático
        const mRoi = document.getElementById('metric-roi');
        const mRoiRatio = document.getElementById('metric-roi-ratio');
        if(mRoi && mRoiRatio) {
            // Tabla de Precios Oficial (Mensual, Licencia Founder como baseline para calcular ROI mensual)
            // Professional: $199 (Founder) | $399 (Estandar)
            // Business: $999 (Founder) | $1999 (Estandar)
            // Calculamos asumiendo Licencia Founder Mensual para ser consistentes con los primeros clientes
            const fidelioCost = window.merchantData.tier === 'business' ? 999 : 199;"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'src="dashboard_v2\.js\?v=\d+"', 'src="dashboard_v2.js?v=' + str(__import__('time').time()) + '"', html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

