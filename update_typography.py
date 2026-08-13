import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add Google Fonts link in <head> if not present
font_links = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">"""

if "fonts.googleapis.com/css2?family=Inter" not in html:
    html = html.replace('</head>', font_links + '\n</head>')

# 2. Update CSS Variables for typography and colors to be more premium
css_vars = """        :root {
            --brand-purple: #1e1b4b;
            --accent-violet: #8b5cf6;
            --bg-main: #f9fafb; /* Lighter, cleaner background */
            --bg-panel: #ffffff;
            --bg-input: #f3f4f6; /* Very subtle gray for inputs */
            --text-main: #111827;
            --text-muted: #6b7280;
            --border-glass: rgba(0,0,0,0.06); /* Softer borders */
            --border-accent: rgba(139, 92, 246, 0.2);
            --radius-lg: 24px;
            --radius-md: 16px;
            --radius-sm: 10px;
            --radius-pill: 9999px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
            --shadow-md: 0 10px 30px rgba(0,0,0,0.03); /* Premium soft shadow */
            --shadow-float: 0 20px 40px rgba(0,0,0,0.08);
            
            --font-main: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-mono: 'SFMono-Regular', Consolas, monospace;
            --transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }"""

pattern_vars = r':root\s*\{.*?\--transition:.*?;.*?\}'
html = re.sub(pattern_vars, css_vars, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
