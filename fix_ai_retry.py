import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Inject the helper function right after genAI initialization
old_init = "const genAI = process.env.GEMINI_API_KEY ? new GoogleGenerativeAI(process.env.GEMINI_API_KEY) : null;"
new_init = """const genAI = process.env.GEMINI_API_KEY ? new GoogleGenerativeAI(process.env.GEMINI_API_KEY) : null;

// Helper with exponential backoff for 503/429 spikes
async function callGeminiWithRetry(prompt, retries = 2) {
    if (!genAI) throw new Error('La IA no está configurada.');
    const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });
    for (let i = 0; i <= retries; i++) {
        try {
            return await model.generateContent(prompt);
        } catch (e) {
            if (i === retries || (!e.message.includes('503') && !e.message.includes('429') && !e.message.includes('overloaded'))) {
                throw new Error("Los servidores de IA están temporalmente saturados. Por favor, intenta de nuevo en unos minutos.");
            }
            await new Promise(r => setTimeout(r, 1500 * (i + 1)));
        }
    }
}"""
js = js.replace(old_init, new_init)

# Replace all occurrences of:
# const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });
# const result = await model.generateContent(promptVariable);
# WITH:
# const result = await callGeminiWithRetry(promptVariable);

# 1. Dashboard Insights
js = js.replace(
    'const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });\n        const systemPrompt = `Eres un Director Financiero AI. Analiza estas métricas en tiempo real del negocio y dame un resumen ejecutivo de máximo 3 oraciones con un tono profesional, alentador y estratégico. Destaca qué métrica es la mejor y da una sugerencia táctica rápida. Métricas: ${JSON.stringify(metrics)}`;\n        \n        const result = await model.generateContent(systemPrompt);',
    'const systemPrompt = `Eres un Director Financiero AI. Analiza estas métricas en tiempo real del negocio y dame un resumen ejecutivo de máximo 3 oraciones con un tono profesional, alentador y estratégico. Destaca qué métrica es la mejor y da una sugerencia táctica rápida. Métricas: ${JSON.stringify(metrics)}`;\n        const result = await callGeminiWithRetry(systemPrompt);'
)

# 2. Metrics Insights
js = js.replace(
    'const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });\n        const prompt = "Eres un estratega de negocios. Analiza estas métricas generales: Tasa de Retorno, Crecimiento mensual, CAC, LTV. Dame un consejo de 2 líneas sobre cómo optimizarlas y retener más clientes.";\n        const result = await model.generateContent(prompt);',
    'const prompt = "Eres un estratega de negocios. Analiza estas métricas generales: Tasa de Retorno, Crecimiento mensual, CAC, LTV. Dame un consejo de 2 líneas sobre cómo optimizarlas y retener más clientes.";\n        const result = await callGeminiWithRetry(prompt);'
)

# 3. Appointments Insights
js = js.replace(
    'const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });\n        const prompt = "Eres un experto en optimización de agendas. Dame un consejo corto (2 líneas) sobre cómo reducir el ausentismo (no-shows) y aumentar la tasa de reservas (upselling de servicios adicionales).";\n        const result = await model.generateContent(prompt);',
    'const prompt = "Eres un experto en optimización de agendas. Dame un consejo corto (2 líneas) sobre cómo reducir el ausentismo (no-shows) y aumentar la tasa de reservas (upselling de servicios adicionales).";\n        const result = await callGeminiWithRetry(prompt);'
)

# 4. CRM Insights
js = js.replace(
    'const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });\n        const systemPrompt = `Eres un analista de CRM AI. El negocio tiene actualmente ${customersCount} clientes en su base de datos privada. Dame 1 sola sugerencia audaz y altamente efectiva para monetizar esta base de datos esta semana. Solo responde con la sugerencia, sin saludos ni despedidas, directo al punto.`;\n        \n        const result = await model.generateContent(systemPrompt);',
    'const systemPrompt = `Eres un analista de CRM AI. El negocio tiene actualmente ${customersCount} clientes en su base de datos privada. Dame 1 sola sugerencia audaz y altamente efectiva para monetizar esta base de datos esta semana. Solo responde con la sugerencia, sin saludos ni despedidas, directo al punto.`;\n        const result = await callGeminiWithRetry(systemPrompt);'
)

# 5. Copilot
js = js.replace(
    'const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });\n        \n        const systemPrompt = `Eres Fidelio AI Copilot...',
    'const systemPrompt = `Eres Fidelio AI Copilot...'
)
js = js.replace(
    'const result = await model.generateContent(systemPrompt);',
    'const result = await callGeminiWithRetry(systemPrompt);'
)

# 6. Magic Builder
js = js.replace(
    'const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });\n\n        const systemPrompt = `Eres un Diseñador UX/UI...',
    'const systemPrompt = `Eres un Diseñador UX/UI...'
)
# Wait, let's just do a regex replace for the ones that might have slightly different spacing
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Initial replacements done. Now cleaning up dangling models.")
