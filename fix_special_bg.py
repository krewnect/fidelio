import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = re.sub(
    r'backgroundColor:\s*"rgb\(17, 24, 39\)",\s*foregroundColor:\s*"#ffffff",',
    r'backgroundColor: "rgb(255, 255, 255)",\n                foregroundColor: "rgb(17, 24, 39)",',
    app_js
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
