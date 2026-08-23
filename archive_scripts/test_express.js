const express = require('express');
const app = express();
const path = require('path');
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});
app.listen(9999, () => {
    console.log("Listening on 9999");
    const http = require('http');
    http.get('http://localhost:9999/', (res) => {
        console.log("Status:", res.statusCode);
        process.exit(0);
    });
});
