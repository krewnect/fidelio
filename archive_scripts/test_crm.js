require('dotenv').config();
const { GoogleGenerativeAI } = require('@google/generative-ai');
async function run() {
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    try {
        const model = genAI.getGenerativeModel({ model: "gemini-3.7-flash" });
        const systemPrompt = `Eres un analista de CRM AI. El negocio tiene actualmente 0 clientes en su base de datos privada. Dame 1 sola sugerencia audaz y altamente efectiva para monetizar esta base de datos esta semana. Solo responde con la sugerencia, sin saludos ni despedidas, directo al punto.`;
        const result = await model.generateContent(systemPrompt);
        console.log("Success:", await result.response.text());
    } catch(e) {
        console.error("Error:", e.message);
    }
}
run();
