const express = require('express');
const app = express();
const path = require('path');
app.get('/', (req, res) => {
    res.sendFile('index.html', { root: __dirname });
});
app.listen(9998, () => {
    const http = require('http');
    http.get('http://localhost:9998/', (res) => {
        console.log("Status with root:", res.statusCode);
        process.exit(0);
    });
});
