import re

files = ['index.html', 'scanner.html', 'landing.html']
for filename in files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Remove the CSP tag
        html = re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]+>\n?', '', html)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Removed CSP from {filename}")
    except Exception as e:
        print(f"Error {filename}: {e}")
