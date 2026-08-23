const fs = require('fs');
let js = fs.readFileSync('dashboard_v2.js', 'utf8');

// Remove jsConfetti block
const p1 = js.indexOf('if (typeof jsConfetti !== \\'undefined\\') {');
if(p1 !== -1) {
    const endP1 = js.indexOf('}', js.indexOf('jsConfetti.addConfetti', p1)) + 1;
    js = js.substring(0, js.lastIndexOf('try {', p1)) + js.substring(js.indexOf('} catch(e) {}', endP1) + 13);
}

// Remove DO WOW CONFETTI block
const p2 = js.indexOf('// DO WOW CONFETTI');
if (p2 !== -1) {
    const endP2 = js.indexOf('}', js.indexOf('document.head.appendChild(script);', p2)) + 1;
    js = js.substring(0, p2) + js.substring(endP2);
}

fs.writeFileSync('dashboard_v2.js', js);
console.log("Confetti removed!");
