import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_parse = """        let text = await result.response.text();
        
        text = text.replace(/\`\`\`json\\n?/g, '').replace(/\`\`\`\\n?/g, '').trim();
        
        const strategy = JSON.parse(text);"""

good_parse = """        let text = await result.response.text();
        
        // Extract JSON reliably even if Gemini adds conversational text
        const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);
        if (!jsonMatch) {
            throw new Error('El modelo no devolvió un JSON válido: ' + text);
        }
        
        const strategy = JSON.parse(jsonMatch[0]);"""

js = js.replace(bad_parse, good_parse)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
