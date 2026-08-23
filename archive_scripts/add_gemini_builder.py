import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

new_endpoint = """
// --- AI (GEMINI) MAGIC BUILDER ENDPOINT ---
app.post('/api/ai/magic-builder', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) {
        return res.status(503).json({ error: 'La IA no está configurada actualmente (GEMINI_API_KEY).' });
    }

    try {
        const { industry, businessName } = req.body;
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        
        const systemPrompt = `
Eres un experto consultor de marketing especializado en retención de clientes. 
Un negocio llamado "${businessName}" en la industria/categoría "${industry}" quiere crear una tarjeta de lealtad digital (Apple Wallet).

Debes diseñar la mecánica de lealtad perfecta para su industria.
Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta:
{
  "primaryColor": "#CódigoHexadecimal",
  "accentColor": "#CódigoHexadecimal",
  "stampsTotal": un número entero entre 4 y 12 (lo más estratégico para su industria),
  "reward": "El premio final (ej. Masaje Capilar Gratis, Consulta de Seguimiento, etc)",
  "instruction": "Instrucción breve (ej. Acumula 5 visitas para ganar)",
  "tip": "Tu consejo como IA experta explicando por qué elegiste esa cantidad de sellos y ese premio específicamente para su industria."
}
No incluyas markdown, no incluyas texto fuera del JSON.
`;

        const result = await model.generateContent(systemPrompt);
        let text = await result.response.text();
        
        text = text.replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim();
        
        const strategy = JSON.parse(text);
        res.json(strategy);

    } catch (error) {
        console.error('Error en Gemini Magic Builder:', error);
        res.status(500).json({ error: 'Error al generar estrategia con IA.' });
    }
});

"""

# Insert it before the catch-all or error handlers, let's just insert it right before app.post('/api/ai/copilot'
target = r"app\.post\('/api/ai/copilot'"
app_js = re.sub(target, new_endpoint + "app.post('/api/ai/copilot'", app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
