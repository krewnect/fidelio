import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

target_client = """                serialNumber: `${customerId}|${campaignId}`,"""
replacement_client = """                serialNumber: `${customerId}|${campaignId}|${Date.now()}`,"""

app_js = app_js.replace(target_client, replacement_client)

target_demo = """                serialNumber: customer.id,"""
replacement_demo = """                serialNumber: `${customer.id}|${Date.now()}`,"""

app_js = app_js.replace(target_demo, replacement_demo)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
