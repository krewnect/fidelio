import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove .gemini-insight-panel from the pure white background css
old_css = """/* 2. Unified Cards (Pure White, Soft Shadow, 24px Radius) */
.tab-content > div[style*="background"], 
.stat-card, 
.content-panel, 
.settings-card,
.apple-section,
.stats-grid > div,
.gemini-insight-panel,
.accordion-card {
    background: #FFFFFF !important;"""

new_css = """/* 2. Unified Cards (Pure White, Soft Shadow, 24px Radius) */
.tab-content > div[style*="background"], 
.stat-card, 
.content-panel, 
.settings-card,
.apple-section,
.stats-grid > div,
.accordion-card {
    background: #FFFFFF !important;"""

html = html.replace(old_css, new_css)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
