import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the Stripe Pro button
html = html.replace(
    '<button class="btn btn-primary" style="background: var(--accent-amber) !important; color: #000 !important; font-weight: 800; border: none;"><i class="fa-solid fa-arrow-up-right-dots"></i> Hacer Upgrade a Pro</button>',
    '<button class="btn btn-primary" onclick="window.location.href=\'professionals.html\'" style="background: var(--accent-amber) !important; color: #000 !important; font-weight: 800; border: none;"><i class="fa-solid fa-arrow-up-right-dots"></i> Hacer Upgrade a Pro</button>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Stripe Pro button linked.")
