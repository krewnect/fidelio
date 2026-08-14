import sys

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

error_handler = """<body>
    <script>
        window.addEventListener("error", function(e) {
            var errDiv = document.createElement('div');
            errDiv.style = "position:fixed; z-index:99999; background:red; color:white; top:0; left:0; width:100%; padding:20px; font-size:16px; font-family:monospace; box-sizing:border-box;";
            errDiv.innerHTML = "<b>ERROR:</b> " + e.message + " at " + e.filename + ":" + e.lineno + "<br>" + (e.error && e.error.stack ? e.error.stack.replace(/\\n/g, '<br>') : "");
            document.body.appendChild(errDiv);
        });
        window.addEventListener("unhandledrejection", function(e) {
            var errDiv = document.createElement('div');
            errDiv.style = "position:fixed; z-index:99999; background:orange; color:black; top:50px; left:0; width:100%; padding:20px; font-size:16px; font-family:monospace; box-sizing:border-box;";
            errDiv.innerHTML = "<b>PROMISE REJECTION:</b> " + (e.reason && e.reason.message ? e.reason.message : e.reason) + "<br>" + (e.reason && e.reason.stack ? e.reason.stack.replace(/\\n/g, '<br>') : "");
            document.body.appendChild(errDiv);
        });
    </script>"""

html = html.replace("<body>", error_handler)

with open('/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Injected error handler.")
