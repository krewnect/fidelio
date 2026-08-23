import re

with open('index.html', 'r') as f:
    content = f.read()

security_js = """
    <!-- FIDELIO ANTI-TAMPERING & SECURITY -->
    <script>
        // Prevenir Right-Click (Context Menu)
        document.addEventListener('contextmenu', event => event.preventDefault());

        // Prevenir Selección de Texto
        document.addEventListener('selectstart', event => event.preventDefault());

        // Bloquear atajos de teclado de desarrollador (F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U)
        document.addEventListener('keydown', function(e) {
            if (
                e.key === 'F12' || 
                (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'i')) || 
                (e.ctrlKey && e.shiftKey && (e.key === 'J' || e.key === 'j')) || 
                (e.ctrlKey && e.shiftKey && (e.key === 'C' || e.key === 'c')) ||
                (e.ctrlKey && (e.key === 'U' || e.key === 'u')) ||
                (e.metaKey && e.altKey && (e.key === 'I' || e.key === 'i')) || // Mac F12
                (e.metaKey && e.altKey && (e.key === 'J' || e.key === 'j')) ||
                (e.metaKey && (e.key === 'U' || e.key === 'u'))
            ) {
                e.preventDefault();
                return false;
            }
        });

        // Debugger Trap (Dificulta la inspección de código rompiendo el flujo si abren la consola)
        setInterval(function() {
            (function() { return false; }['constructor']('debugger')());
        }, 100);
    </script>
"""

if '<!-- FIDELIO ANTI-TAMPERING & SECURITY -->' not in content:
    content = content.replace('</head>', security_js + '\n</head>')

# Add CSS to prevent selection globally just in case
css_unselectable = """
        /* Anti-Copy Protection */
        body {
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        input, textarea {
            -webkit-user-select: auto;
            -khtml-user-select: auto;
            -moz-user-select: auto;
            -ms-user-select: auto;
            user-select: auto;
        }
"""
content = content.replace('</style>', css_unselectable + '\n    </style>')

with open('index.html', 'w') as f:
    f.write(content)
print("Security patched successfully")
