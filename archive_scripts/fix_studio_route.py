with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

route = """
app.get('/panel', (req, res) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    res.sendFile('index.html', { root: __dirname });
});

// Explicit route for Studio
app.get('/studio/index.html', (req, res) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.sendFile('studio/index.html', { root: __dirname });
});
"""

js = js.replace("""app.get('/panel', (req, res) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    res.sendFile('index.html', { root: __dirname });
});""", route)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Added explicit route for /studio/index.html")
