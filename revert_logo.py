import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the custom CSS for the animated logo
css_start = "/* ANIMATED FIDELIO LOGO (REAL) */"
css_end = "/* BUTTON HOVER FX */"

pattern = re.compile(re.escape(css_start) + r'.*?' + re.escape(css_end), re.DOTALL)
html = pattern.sub("/* BUTTON HOVER FX */", html)

# 2. Replace the HTML logo block with the original static image
html_start = '<div class="sidebar-brand"'
html_end = '</div>\n            </div>'

static_logo_html = """<div class="sidebar-brand" style="cursor: pointer;" onclick="location.reload()">
                <img src="./fidelio_logo_purple.png?v=5" alt="Fidelio Logo" style="height: 44px; width: auto; object-fit: contain;" />
            </div>"""

pattern2 = re.compile(re.escape(html_start) + r'.*?' + re.escape(html_end), re.DOTALL)
html = pattern2.sub(static_logo_html, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
