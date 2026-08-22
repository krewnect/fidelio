const fs = require('fs');
let code = fs.readFileSync('app.js', 'utf8');

// The problematic string has literal newlines inside the regex.
// We will replace the entire block that parses the gemini response.
const newParsing = `
        const result = await model.generateContent(systemPrompt);
        let text = await result.response.text();
        
        text = text.replace(/\`\`\`json\\n?/g, '').replace(/\`\`\`\\n?/g, '').trim();
        
        const strategy = JSON.parse(text);
        res.json(strategy);
`;

// regex to match the bad block
code = code.replace(/const result = await model\.generateContent\(systemPrompt\);[\s\S]*?res\.json\(strategy\);/g, newParsing.trim());

fs.writeFileSync('app.js', code);
