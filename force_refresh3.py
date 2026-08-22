import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = re.sub(r'serialNumber: `\$\{customerId\}\|\$\{campaignId\}\|v3_\$\{Date\.now\(\)\}`', r'serialNumber: `${customerId}|${campaignId}|v4_${Date.now()}`', app_js)
app_js = re.sub(r'serialNumber: `\$\{customer\.id\}\|v3_\$\{Date\.now\(\)\}`', r'serialNumber: `${customer.id}|v4_${Date.now()}`', app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
