import re

files_to_update = ['index.html', 'scanner.html', 'landing.html']

anti_copy_script = """
    <!-- SECURITY: Anti-Copy & Anti-DevTools Protection -->
    <style>
        /* Disable text selection globally */
        body {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        /* Allow selection in inputs and textareas */
        input, textarea {
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }
    </style>
    <script>
        // Disable Right Click
        document.addEventListener('contextmenu', event => event.preventDefault());

        // Disable Keyboard Shortcuts (F12, Ctrl+Shift+I, Ctrl+U, Ctrl+S, etc.)
        document.onkeydown = function(e) {
            if (e.keyCode == 123) return false; // F12
            if (e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) return false; // Ctrl+Shift+I
            if (e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)) return false; // Ctrl+Shift+C
            if (e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) return false; // Ctrl+Shift+J
            if (e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) return false; // Ctrl+U
            if (e.ctrlKey && e.keyCode == 'S'.charCodeAt(0)) return false; // Ctrl+S
            // Mac shortcuts
            if (e.metaKey && e.altKey && e.keyCode == 'I'.charCodeAt(0)) return false; // Cmd+Opt+I
            if (e.metaKey && e.altKey && e.keyCode == 'C'.charCodeAt(0)) return false; // Cmd+Opt+C
            if (e.metaKey && e.altKey && e.keyCode == 'U'.charCodeAt(0)) return false; // Cmd+Opt+U
        };

        // Anti-DevTools Debugger Trap
        // This will freeze the browser's developer tools if they manage to open them
        setInterval(function() {
            const before = new Date().getTime();
            debugger;
            const after = new Date().getTime();
            if (after - before > 100) {
                // DevTools is open and paused the execution
                document.body.innerHTML = "<div style='display:flex; height:100vh; width:100vw; background:#111; color:white; align-items:center; justify-content:center; font-family:monospace; font-size:24px;'>Modo de depuración no permitido. Acceso restringido.</div>";
                window.location.href = "about:blank";
            }
        }, 1000);
    </script>
"""

for filename in files_to_update:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Insert before </head> if not already there
        if '</head>' in html and 'Anti-Copy & Anti-DevTools' not in html:
            html = html.replace('</head>', anti_copy_script + '\n</head>')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Added Anti-Copy to {filename}")
    except Exception as e:
        print(f"Error updating {filename}: {e}")
