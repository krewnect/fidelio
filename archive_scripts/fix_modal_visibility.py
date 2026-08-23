import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove opacity: 0 and transition from the modal wrapper
html = html.replace(
    'z-index: 100000; opacity: 0; transition: opacity 0.3s;"',
    'z-index: 100000;"'
)

# Remove transform: scale(0.95) and transition from the modal content
html = html.replace(
    'position: relative; transform: scale(0.95); transition: transform 0.3s; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);"',
    'position: relative; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);"'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Modal visibility fixed.")
