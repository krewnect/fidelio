import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix dashboard insights by replacing the bad block
bad_dashboard = r'''app\.post\('/api/ai/dashboard-insights'[\s\S]*?res\.status\(500\)\.json\(\{ error: 'Error al generar estrategia con IA\.' \}\);\s*\}\s*\}\);'''

good_dashboard = """app.post('/api/ai/dashboard-insights', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) return res.status(503).json({ error: 'La IA no está configurada.' });
    try {
        const { metrics } = req.body;
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const systemPrompt = `Eres un Director Financiero AI. Analiza estas métricas en tiempo real del negocio y dame un resumen ejecutivo de máximo 3 oraciones con un tono profesional, alentador y estratégico. Destaca qué métrica es la mejor y da una sugerencia táctica rápida. Métricas: ${JSON.stringify(metrics)}`;
        
        const result = await model.generateContent(systemPrompt);
        let text = await result.response.text();
        res.json({ insight: text });
    } catch (error) {
        console.error('Error en Gemini Dashboard Insights:', error);
        res.status(500).json({ error: 'Error al generar insight con IA.' });
    }
});

// ==========================================
// GEMINI CRM INSIGHTS
// ==========================================
app.post('/api/ai/crm-insights', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) return res.status(503).json({ error: 'La IA no está configurada.' });
    try {
        const { customersCount } = req.body;
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const systemPrompt = `Eres un analista de CRM AI. El negocio tiene actualmente ${customersCount} clientes en su base de datos privada. Dame 1 sola sugerencia audaz y altamente efectiva para monetizar esta base de datos esta semana. Solo responde con la sugerencia, sin saludos ni despedidas, directo al punto.`;
        
        const result = await model.generateContent(systemPrompt);
        let text = await result.response.text();
        res.json({ insight: text });
    } catch (error) {
        console.error('Error en Gemini CRM Insights:', error);
        res.status(500).json({ error: 'Error al generar insight con IA.' });
    }
});"""

js = re.sub(bad_dashboard, good_dashboard, js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
