import re

with open('landing.html', 'r') as f:
    content = f.read()

# Replace onclick="document.getElementById('X').classList.add('active')"
# with data-modal-open="X"
content = re.sub(
    r'onclick="document\.getElementById\(\'([a-zA-Z0-9_-]+)\'\)\.classList\.add\(\'active\'\)[^"]*"',
    r'data-modal-open="\1"',
    content
)

# Replace onclick="document.getElementById('X').classList.remove('active')"
# with data-modal-close="X"
content = re.sub(
    r'onclick="document\.getElementById\(\'([a-zA-Z0-9_-]+)\'\)\.classList\.remove\(\'active\'\)[^"]*"',
    r'data-modal-close="\1"',
    content
)

# Add the script just before </body>
script_to_add = """
    <script>
        // Manejo de Modales (Evita bloqueos de CSP por onclick en línea)
        document.querySelectorAll('[data-modal-open]').forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = el.getAttribute('data-modal-open');
                const modal = document.getElementById(modalId);
                if (modal) modal.classList.add('active');
            });
        });

        document.querySelectorAll('[data-modal-close]').forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = el.getAttribute('data-modal-close');
                const modal = document.getElementById(modalId);
                if (modal) modal.classList.remove('active');
            });
        });
    </script>
</body>
"""

content = content.replace('</body>', script_to_add)

with open('landing.html', 'w') as f:
    f.write(content)

print("Done")
