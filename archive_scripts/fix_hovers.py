import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add to the global CSS override:
hover_override = """
/* 7. Unified Card Hovers (Kill the purple borders) */
.tab-content > div[style*="background"]:hover, 
.stat-card:hover, 
.content-panel:hover, 
.settings-card:hover,
.gemini-insight-panel:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025) !important;
    border-color: #E5E7EB !important; /* Force keep grey border */
}
"""

if "Unified Card Hovers" not in html:
    html = html.replace('</style>', hover_override + '\n</style>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
