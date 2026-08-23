const express = require('express');
const app = express();
const path = require('path');
app.get('/', (req, res, next) => {
    res.sendFile(path.join(__dirname, 'index.html'), (err) => {
        if (err) {
            console.error("Error from sendFile:", err.message);
        }
        res.end();
    });
});
app.listen(9997, () => {
    const http = require('http');
    http.get('http://localhost:9997/', (res) => {
        process.exit(0);
    });
});
