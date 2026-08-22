import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

app_js = re.sub(r'serialNumber: `\$\{customerId\}\|\$\{campaignId\}\|\$\{Date\.now\(\)\}`', r'serialNumber: `${customerId}|${campaignId}|v2_${Date.now()}`', app_js)
app_js = re.sub(r'serialNumber: `\$\{customer\.id\}\|\$\{Date\.now\(\)\}`', r'serialNumber: `${customer.id}|v2_${Date.now()}`', app_js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
