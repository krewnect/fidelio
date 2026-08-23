import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace legacy buttons in template strings
js = re.sub(r'class="btn btn-primary([^"]*)"', r'class="fidelio-btn-primary\1"', js)
js = re.sub(r'class="btn-primary([^"]*)"', r'class="fidelio-btn-primary\1"', js)
js = re.sub(r'class="apple-btn-primary([^"]*)"', r'class="fidelio-btn-primary\1"', js)
js = re.sub(r'class="btn btn-outline([^"]*)"', r'class="fidelio-btn-secondary\1"', js)
js = re.sub(r'class="btn-outline([^"]*)"', r'class="fidelio-btn-secondary\1"', js)
js = re.sub(r'class="btn([^"]*)"', r'class="fidelio-btn-secondary\1"', js) 
js = js.replace('fidelio-fidelio-btn', 'fidelio-btn')

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Replaced legacy UI classes in dashboard_v2.js.")
