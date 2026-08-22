const express = require('express');
const app = express();
const path = require('path');
app.get('/', (req, res, next) => {
    res.sendFile(path.join(__dirname, 'landing.html'), (err) => {
        if (err) console.error("Error from sendFile:", err.message);
        res.end();
    });
});
app.listen(9996, () => {
    const http = require('http');
    http.get('http://localhost:9996/', (res) => {
        console.log("Status:", res.statusCode);
        process.exit(0);
    });
});
