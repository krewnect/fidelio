import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    content = f.read()

# The spam string to remove
spam_string = """        checkPricingStatus();
        // Expose to window for stripe button
        window.isFounder = isFounder;"""

# Count occurrences
count = content.count(spam_string)
print(f"Found {count} occurrences of spam string.")

# Remove them all
content = content.replace(spam_string, "")

# We still need to call checkPricingStatus() on init, so we will inject it correctly inside DOMContentLoaded or initDashboard later if it's missing.

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed spam from dashboard.js")
