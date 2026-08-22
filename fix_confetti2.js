const fs = require('fs');
let js = fs.readFileSync('dashboard_v2.js', 'utf8');

js = js.replace(/\/\/ DO WOW CONFETTI[\s\S]*?document\.head\.appendChild\(script\);\s+\}/g, '');
js = js.replace(/try\s*\{\s*if\s*\(typeof jsConfetti !== 'undefined'\)[\s\S]*?\} catch\(e\) \{\}/g, '');

fs.writeFileSync('dashboard_v2.js', js);
console.log("Confetti removed!");
