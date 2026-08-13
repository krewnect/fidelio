import re

with open('index.html', 'r') as f:
    html = f.read()

# Add toast container right after <body>
html = html.replace(
    "<body style=",
    '<div id="toast-container" class="toast-container"></div>\n<body style='
)

with open('index.html', 'w') as f:
    f.write(html)
