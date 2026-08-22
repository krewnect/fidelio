import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Let's check for any SQL injection vulnerabilities or missing auth
print("Missing requireMerchantAuth:")
for line in js.splitlines():
    if "app.post" in line or "app.get" in line:
        if "/api/" in line and "requireMerchantAuth" not in line and "webhook" not in line and "generateContent" not in line and "test-models" not in line:
            print(line)
