import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the active "Descargar PDF" buttons with disabled "Próximamente" buttons to avoid deceiving the user
html = html.replace(
    '<button class="fidelio-btn-primary" style="width: 100%; justify-content: center; padding: 10px !important;"><i class="fa-solid fa-cloud-arrow-down"></i> Descargar PDF</button>',
    '<button class="fidelio-btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed; width: 100%; justify-content: center; background: #F3F4F6; border: none; color: #9CA3AF; padding: 10px !important;"><i class="fa-solid fa-lock"></i> Próximamente</button>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
