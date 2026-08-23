import re

# 1. ADD ENDPOINTS TO APP.JS
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

endpoints = """
// ==========================================
// GEMINI METRICS INSIGHTS
// ==========================================
app.post('/api/ai/metrics-insights', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) return res.status(503).json({ insight: 'La IA no está configurada.' });
    try {
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const prompt = "Eres un estratega de negocios. Analiza estas métricas generales: Tasa de Retorno, Crecimiento mensual, CAC, LTV. Dame un consejo de 2 líneas sobre cómo optimizarlas y retener más clientes.";
        const result = await model.generateContent(prompt);
        res.json({ success: true, insight: result.response.text().replace(/\*/g, '') });
    } catch (e) {
        res.status(500).json({ success: false, error: e.message });
    }
});

// ==========================================
// GEMINI APPOINTMENTS INSIGHTS
// ==========================================
app.post('/api/ai/appointments-insights', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) return res.status(503).json({ insight: 'La IA no está configurada.' });
    try {
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const prompt = "Eres un experto en optimización de agendas. Dame un consejo corto (2 líneas) sobre cómo reducir el ausentismo (no-shows) y aumentar la tasa de reservas (upselling de servicios adicionales).";
        const result = await model.generateContent(prompt);
        res.json({ success: true, insight: result.response.text().replace(/\*/g, '') });
    } catch (e) {
        res.status(500).json({ success: false, error: e.message });
    }
});
"""

if "/api/ai/metrics-insights" not in app_js:
    app_js = app_js.replace("app.post('/api/ai/crm-insights'", endpoints + "\napp.post('/api/ai/crm-insights'")
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)


# 2. INJECT HTML PANELS IN INDEX.HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make CRM Panel clickable
crm_panel_old = r'<p id="gemini-crm-text" style="margin: 0; font-size: 14px; color: #475569; line-height: 1\.6;">[\s\S]*?</p>'
crm_panel_new = """<p id="gemini-crm-text" style="margin: 0; font-size: 14px; color: #475569; line-height: 1.6; margin-bottom:12px;">
                        Descubre patrones de consumo en tu base de datos para vender más.
                    </p>
                    <button class="fidelio-btn-primary" onclick="if(window.fetchGeminiCRMInsights) window.fetchGeminiCRMInsights()" style="background:#7C3AED; color:white; border:none; border-radius:12px; padding:10px 20px; font-weight:600; font-size:14px; cursor:pointer; display:flex; align-items:center; gap:8px;">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Ejecutar Análisis CRM
                    </button>"""
if "Ejecutar Análisis CRM" not in html:
    html = re.sub(crm_panel_old, crm_panel_new, html)


# Inject Metrics Panel
metrics_html = """
                <div class="workspace-header">
                    <div>
                        <div class="workspace-eyebrow">Rendimiento</div>
                        <h1>Métricas y Analytics</h1>
                        <p>Analiza el retorno de inversión y el desempeño de tus campañas.</p>
                    </div>
                </div>

                <!-- GEMINI METRICS INSIGHTS -->
                <div class="gemini-insight-panel" style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 24px; padding: 32px; margin-bottom: 24px; position: relative; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                    <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; opacity: 0.05; filter: grayscale(1);">🤖</div>
                    <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 800; color: #111827; display: flex; align-items: center; gap: 8px;">
                        <i class="fa-solid fa-chart-line" style="color: #7C3AED;"></i> Análisis Financiero (Gemini IA)
                    </h3>
                    <p id="gemini-metrics-text" style="margin: 0; font-size: 15px; color: #4B5563; line-height: 1.6; margin-bottom: 16px;">
                        Gemini puede analizar la rentabilidad de tus premios y sugerirte formas de aumentar tu Ticket Promedio.
                    </p>
                    <button class="fidelio-btn-primary" onclick="if(window.fetchGeminiMetricsInsights) window.fetchGeminiMetricsInsights()" style="background:#7C3AED; color:white; border:none; border-radius:12px; padding:10px 20px; font-weight:600; font-size:14px; cursor:pointer; display:flex; align-items:center; gap:8px;">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Generar Reporte de IA
                    </button>
                </div>
"""
if "Generar Reporte de IA" not in html:
    html = re.sub(r'<div class="workspace-header">\s*<div>\s*<div class="workspace-eyebrow">Rendimiento</div>\s*<h1>Métricas y Analytics</h1>\s*<p>Analiza el retorno de inversión y el desempeño de tus campañas.</p>\s*</div>\s*</div>', metrics_html, html)

# Inject Appointments Panel
appt_html = """
                            <div class="workspace-header">
                                <div>
                                    <div class="workspace-eyebrow">Gestión</div>
                                    <h1>Citas y Servicios</h1>
                                    <p>Controla la agenda de tu equipo y reduce el ausentismo.</p>
                                </div>
                            </div>
                            
                            <!-- GEMINI APPOINTMENTS INSIGHTS -->
                            <div class="gemini-insight-panel" style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 24px; padding: 32px; margin-bottom: 24px; position: relative; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                                <div style="position: absolute; top: -20px; right: -20px; font-size: 100px; opacity: 0.05; filter: grayscale(1);">🤖</div>
                                <h3 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 800; color: #111827; display: flex; align-items: center; gap: 8px;">
                                    <i class="fa-solid fa-calendar-check" style="color: #7C3AED;"></i> Optimización de Agenda (Gemini IA)
                                </h3>
                                <p id="gemini-appointments-text" style="margin: 0; font-size: 15px; color: #4B5563; line-height: 1.6; margin-bottom: 16px;">
                                    Recibe consejos accionables de Gemini sobre cómo disminuir los "No-Shows" y cobrar anticipos.
                                </p>
                                <button class="fidelio-btn-primary" onclick="if(window.fetchGeminiAppointmentsInsights) window.fetchGeminiAppointmentsInsights()" style="background:#7C3AED; color:white; border:none; border-radius:12px; padding:10px 20px; font-weight:600; font-size:14px; cursor:pointer; display:flex; align-items:center; gap:8px;">
                                    <i class="fa-solid fa-wand-magic-sparkles"></i> Optimizar mi Agenda
                                </button>
                            </div>
"""
if "Optimizar mi Agenda" not in html:
    html = re.sub(r'<div class="workspace-header">\s*<div>\s*<div class="workspace-eyebrow">Gestión</div>\s*<h1>Citas y Servicios</h1>\s*<p>Controla la agenda de tu equipo y reduce el ausentismo.</p>\s*</div>\s*</div>', appt_html, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 3. JS LOGIC IN DASHBOARD_V2.JS
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    dash = f.read()

js_endpoints = """
window.fetchGeminiMetricsInsights = async function() {
    const textEl = document.getElementById('gemini-metrics-text');
    if (!textEl) return;
    textEl.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin" style="color:#7C3AED;"></i> Evaluando retornos de inversión y ticket promedio...';
    try {
        const token = localStorage.getItem('merchant_token');
        const reqOpts = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;
        const res = await fetch('/api/ai/metrics-insights', reqOpts);
        if (!res.ok) throw new Error('Error al conectar con Gemini');
        const data = await res.json();
        textEl.innerHTML = `<b>Reporte de Optimización:</b> ${data.insight}`;
    } catch (err) {
        textEl.innerHTML = '<i style="color:#ef4444;">No se pudo conectar con Gemini. Reintenta más tarde.</i>';
    }
};

window.fetchGeminiAppointmentsInsights = async function() {
    const textEl = document.getElementById('gemini-appointments-text');
    if (!textEl) return;
    textEl.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin" style="color:#7C3AED;"></i> Diseñando tácticas para reducir el ausentismo...';
    try {
        const token = localStorage.getItem('merchant_token');
        const reqOpts = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;
        const res = await fetch('/api/ai/appointments-insights', reqOpts);
        if (!res.ok) throw new Error('Error al conectar con Gemini');
        const data = await res.json();
        textEl.innerHTML = `<b>Táctica Sugerida:</b> ${data.insight}`;
    } catch (err) {
        textEl.innerHTML = '<i style="color:#ef4444;">No se pudo conectar con Gemini. Reintenta más tarde.</i>';
    }
};
"""

if "fetchGeminiMetricsInsights" not in dash:
    dash += "\n" + js_endpoints
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(dash)

