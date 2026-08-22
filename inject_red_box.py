with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Only inject if not already there
if "GLOBAL_ERROR_CATCHER_V2" not in html:
    script = """
    <!-- GLOBAL_ERROR_CATCHER_V2 -->
    <script>
    window.fidelioErrors = [];
    function showGlobalError(msg) {
        window.fidelioErrors.push(msg);
        let box = document.getElementById('fatal-error-box');
        if (!box) {
            box = document.createElement('div');
            box.id = 'fatal-error-box';
            box.style.cssText = 'position:fixed;top:10px;left:50%;transform:translateX(-50%);background:red;color:white;padding:20px;z-index:99999999;border:3px solid yellow;font-family:monospace;font-size:16px;max-width:90vw;overflow:auto;max-height:80vh;';
            document.body.appendChild(box);
        }
        box.innerHTML = '<b>JS ERROR TRAPPED:</b><br><br>' + window.fidelioErrors.join('<br><hr><br>');
    }
    window.onerror = function(msg, url, lineNo, columnNo, error) {
        showGlobalError(`${msg}<br>Line: ${lineNo}<br>File: ${url}<br>Stack: ${error ? error.stack : 'N/A'}`);
        return false;
    };
    window.addEventListener('unhandledrejection', function(event) {
        showGlobalError(`Unhandled Promise Rejection:<br>${event.reason ? (event.reason.stack || event.reason) : event}`);
    });
    
    // Also trap console.error
    const originalConsoleError = console.error;
    console.error = function(...args) {
        showGlobalError('Console Error:<br>' + args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' '));
        originalConsoleError.apply(console, args);
    };
    </script>
    """
    html = html.replace('<head>', '<head>\n' + script)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected global error catcher.")
else:
    print("Already injected.")
