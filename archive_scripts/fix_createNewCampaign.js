const fs = require('fs');
let code = fs.readFileSync('dashboard_v2.js', 'utf8');

code = code.replace(`document.querySelector('.nav-tab[data-tab="tab-builder"]').click();`, `
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    const builderTab = document.getElementById('tab-builder');
    if (builderTab) builderTab.classList.add('active');
    else console.error("tab-builder not found");
`);

// CACHE BUSTER for index.html
let html = fs.readFileSync('index.html', 'utf8');
const ts = new Date().getTime();
html = html.replace(/src="dashboard_v2\.js\?v=\d+"/g, `src="dashboard_v2.js?v=${ts}"`);
fs.writeFileSync('index.html', html);

fs.writeFileSync('dashboard_v2.js', code);
