require('dotenv').config();
const { GoogleGenerativeAI } = require('@google/generative-ai');

async function run() {
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    try {
        const model = genAI.getGenerativeModel({ model: "gemini-3.6-flash" });
        const result = await model.generateContent("Hola");
        console.log("Success 3.6-flash:", result.response.text());
    } catch(e) {
        console.error("Error 3.6-flash:", e.message);
    }
}
run();
