import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

trap = """        // Anti-DevTools Debugger Trap
        setInterval(function() {
            const before = new Date().getTime();
            debugger;
            const after = new Date().getTime();
            if (after - before > 100) {
                // DevTools is open and paused the script
                document.body.innerHTML = '<h1>DevTools Not Allowed</h1>';
                window.location.href = 'about:blank';
            }
        }, 1000);"""

if trap in html:
    html = html.replace(trap, "")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Debugger trap removed.")
else:
    print("Debugger trap not found.")

