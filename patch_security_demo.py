import re

with open('sales_demo.html', 'r') as f:
    content = f.read()

security_js = """
    <!-- FIDELIO ANTI-TAMPERING & SECURITY -->
    <script>
        document.addEventListener('contextmenu', event => event.preventDefault());
        document.addEventListener('selectstart', event => event.preventDefault());
        document.addEventListener('keydown', function(e) {
            if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) || (e.ctrlKey && e.key === 'U') || (e.metaKey && e.altKey && (e.key === 'I' || e.key === 'J')) || (e.metaKey && e.key === 'U')) {
                e.preventDefault(); return false;
            }
        });
        setInterval(function() { (function() { return false; }['constructor']('debugger')()); }, 100);
    </script>
"""
content = content.replace('</head>', security_js + '\n</head>')

with open('sales_demo.html', 'w') as f:
    f.write(content)
print("Demo security patched successfully")
