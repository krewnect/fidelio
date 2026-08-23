import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

error_script = """
    <!-- ERROR CATCHER FOR LOCALHOST DEBUGGING -->
    <script>
    window.addEventListener('error', function(e) {
        let errDiv = document.getElementById('debug-error-overlay');
        if (!errDiv) {
            errDiv = document.createElement('div');
            errDiv.id = 'debug-error-overlay';
            errDiv.style.cssText = 'position:fixed; top:0; left:0; width:100%; padding:20px; background:red; color:white; z-index:999999; font-family:monospace; white-space:pre-wrap; max-height:50vh; overflow-y:auto;';
            document.body.prepend(errDiv);
        }
        errDiv.innerHTML += `\\nERROR: ${e.message} at ${e.filename}:${e.lineno}`;
    });
    window.addEventListener('unhandledrejection', function(e) {
        let errDiv = document.getElementById('debug-error-overlay');
        if (!errDiv) {
            errDiv = document.createElement('div');
            errDiv.id = 'debug-error-overlay';
            errDiv.style.cssText = 'position:fixed; top:0; left:0; width:100%; padding:20px; background:red; color:white; z-index:999999; font-family:monospace; white-space:pre-wrap; max-height:50vh; overflow-y:auto;';
            document.body.prepend(errDiv);
        }
        errDiv.innerHTML += `\\nUNHANDLED PROMISE: ${e.reason}`;
    });
    </script>
</head>"""

if '</head>' in html:
    html = html.replace('</head>', error_script)
    print("Injected error overlay")
else:
    print("Could not find </head>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
