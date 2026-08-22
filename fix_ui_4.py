with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

force_light_css = """
        /* Force light theme on the wallet pass to prevent Dark Mode inversions that make it look cut off */
        #pass-render, .pass-preview-card {
            color-scheme: light !important;
        }
        .premium-white-card {
            background-color: #ffffff !important;
            color: #111827 !important;
        }
"""
html = html.replace('</style>', force_light_css + '</style>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
