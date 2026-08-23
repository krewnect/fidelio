import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace legacy buttons
html = re.sub(r'class="btn btn-primary([^"]*)"', r'class="fidelio-btn-primary\1"', html)
html = re.sub(r'class="btn-primary([^"]*)"', r'class="fidelio-btn-primary\1"', html)
html = re.sub(r'class="apple-btn-primary([^"]*)"', r'class="fidelio-btn-primary\1"', html)
html = re.sub(r'class="btn btn-outline([^"]*)"', r'class="fidelio-btn-secondary\1"', html)
html = re.sub(r'class="btn-outline([^"]*)"', r'class="fidelio-btn-secondary\1"', html)
html = re.sub(r'class="btn([^"]*)"', r'class="fidelio-btn-secondary\1"', html) # Fallback for plain btn
html = html.replace('fidelio-fidelio-btn', 'fidelio-btn') # Fix double replacements just in case

# Clean up inputs if they just use <input type="text" style="..."> without a class, or missing fidelio-input
# Actually, looking for input fields without fidelio-input
def add_fidelio_input(match):
    tag = match.group(0)
    if 'class=' not in tag and 'type="checkbox"' not in tag and 'type="radio"' not in tag and 'type="file"' not in tag:
        return tag.replace('<input ', '<input class="fidelio-input" ')
    elif 'class="' in tag and 'fidelio-input' not in tag and 'type="checkbox"' not in tag and 'type="radio"' not in tag and 'type="file"' not in tag:
        return re.sub(r'class="([^"]*)"', r'class="\1 fidelio-input"', tag)
    return tag

html = re.sub(r'<input [^>]+>', add_fidelio_input, html)
html = re.sub(r'<select [^>]+>', add_fidelio_input, html)
html = re.sub(r'<textarea [^>]+>', add_fidelio_input, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Replaced legacy UI classes globally.")
