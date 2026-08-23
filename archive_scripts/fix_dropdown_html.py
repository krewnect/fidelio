import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure we don't have multiple elements with id="stripe-campaign-select"
matches = re.findall(r'id="stripe-campaign-select"', html)
print("Occurrences of stripe-campaign-select in index.html:", len(matches))
