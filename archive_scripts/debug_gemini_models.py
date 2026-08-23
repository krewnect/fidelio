import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_catch = """        // Attempt to fetch available models to show in the error message
        let availableModels = '';
        try {
            if (process.env.GEMINI_API_KEY) {
                const fetch = require('node-fetch'); // or use native fetch in node 18+
                const r = await globalThis.fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${process.env.GEMINI_API_KEY}`);
                const d = await r.json();
                if (d && d.models) {
                    availableModels = ' Modelos válidos en tu API Key: ' + d.models.map(m => m.name).join(', ');
                }
            }
        } catch(e) {}
        
        res.status(500).json({ error: `Fallo de Modelo: ${error.message}.${availableModels}` });"""

good_catch = """        // Attempt to fetch available models to show in the error message
        let availableModels = '';
        try {
            if (process.env.GEMINI_API_KEY) {
                const r = await globalThis.fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${process.env.GEMINI_API_KEY}`);
                const d = await r.json();
                if (d && d.models) {
                    availableModels = ' Modelos Permitidos: ' + d.models.map(m => m.name.replace('models/', '')).join(', ');
                } else if (d && d.error) {
                    availableModels = ' Error de API Key: ' + d.error.message;
                }
            }
        } catch(e) {}
        
        res.status(500).json({ error: `[DIAGNÓSTICO] ${error.message}. ${availableModels}` });"""

js = js.replace(bad_catch, good_catch)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
