const fs = require('fs');
const path = require('path');
console.log("__dirname:", __dirname);
console.log("index.html exists:", fs.existsSync(path.join(__dirname, 'index.html')));
