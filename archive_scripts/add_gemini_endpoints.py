import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

new_endpoints = """
// --- AI (GEMINI) DASHBOARD INSIGHTS ---
app.post('/api/ai/dashboard-insights', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) return res.status(503).json({ error: 'La IA no está configurada.' });
    try {
        const { metrics } = req.body;
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const systemPrompt = `Eres un Director Financiero AI. Analiza estas métricas en tiempo real del negocio y dame un resumen ejecutivo de máximo 3 oraciones con un tono profesional, alentador y estratégico. Destaca qué métrica es la mejor y da una sugerencia táctica rápida. Métricas: ${JSON.stringify(metrics)}`;
        
        const result = await model.generateContent(systemPrompt);
        const text = await result.response.text();
        res.json({ insight: text.trim() });
    } catch (error) {
        res.status(500).json({ error: 'Error al generar insights del dashboard.' });
    }
});

// --- AI (GEMINI) CRM ANALYZER ---
app.post('/api/ai/crm-insights', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) return res.status(503).json({ error: 'La IA no está configurada.' });
    try {
        const { customersCount } = req.body;
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const systemPrompt = `Eres un experto en CRM. El negocio tiene actualmente ${customersCount} clientes registrados en su base de datos. Dame un consejo de 2 oraciones sobre cómo segmentar esta base de datos o qué tipo de campaña (ej. Winback, VIP) ejecutar para maximizar el retorno. Se directo y accionable.`;
        
        const result = await model.generateContent(systemPrompt);
        const text = await result.response.text();
        res.json({ insight: text.trim() });
    } catch (error) {
        res.status(500).json({ error: 'Error al generar insights del CRM.' });
    }
});
"""

target = r"app\.post\('/api/ai/magic-builder'"
app_js = re.sub(target, new_endpoints + "\napp.post('/api/ai/magic-builder'", app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
