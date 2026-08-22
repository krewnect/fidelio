require('dotenv').config();
const { GoogleGenerativeAI } = require('@google/generative-ai');

async function run() {
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    try {
        const model = genAI.getGenerativeModel({ model: "gemini-3.5-flash" });
        const result = await model.generateContent("Hola");
        print(result.response.text());
    } catch(e) {
        console.error("Error 3.5-flash:", e.message);
    }
    try {
        const model2 = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
        const result2 = await model2.generateContent("Hola");
        console.log("Success 2.5-flash:", result2.response.text());
    } catch(e) {
        console.error("Error 2.5-flash:", e.message);
    }
}
run();
