import re

with open('index.html', 'r') as f:
    content = f.read()

js_logic = """
<script>
    document.addEventListener('DOMContentLoaded', () => {
        const platformSelect = document.getElementById('booking-platform');
        const linkContainer = document.getElementById('booking-link-container');
        if(platformSelect && linkContainer) {
            platformSelect.addEventListener('change', (e) => {
                if(e.target.value && e.target.value !== '') {
                    linkContainer.style.display = 'block';
                } else {
                    linkContainer.style.display = 'none';
                }
            });
        }
    });
</script>
</body>
"""

content = content.replace('</body>', js_logic)

with open('index.html', 'w') as f:
    f.write(content)
print("Booking JS patched successfully")
