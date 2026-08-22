const fs = require('fs');
let code = fs.readFileSync('app.js', 'utf8');

const magicBuilderEndpoint = `
// ==========================================
// GEMINI MAGIC BUILDER
// ==========================================
app.post('/api/ai/magic-builder', apiLimiter, requireMerchantAuth, async (req, res) => {
    if (!genAI) {
        return res.status(503).json({ error: 'La IA no está configurada actualmente.' });
    }

    try {
        const { industry, businessName } = req.body;
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        
        const systemPrompt = \`
Eres un diseñador experto en fidelización de clientes para Apple Wallet.
Un negocio llamado "\${businessName}" en la industria/categoría "\${industry}" quiere crear una tarjeta de lealtad digital.

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
\`;

        const result = await model.generateContent(systemPrompt);
        let text = await result.response.text();
        
        text = text.replace(/\\\`\\\`\\\`json\\n?/g, '').replace(/\\\`\\\`\\\`\\n?/g, '').trim();
        
        const strategy = JSON.parse(text);
        res.json(strategy);

    } catch (error) {
        console.error('Error en Gemini Magic Builder:', error);
        res.status(500).json({ error: 'Error al generar estrategia con IA.' });
    }
});
`;

if (!code.includes('/api/ai/magic-builder')) {
    code = code.replace('app.listen(PORT', magicBuilderEndpoint + '\n\napp.listen(PORT');
    fs.writeFileSync('app.js', code);
    console.log("Endpoint restored successfully.");
} else {
    console.log("Endpoint already exists.");
}
