import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

target_client = """{ key: "name", label: "SU TARJETA VIRTUAL", value: customer.name || "Invitado" }"""
replacement_client = """{ key: "name", label: "SU TARJETA VIRTUAL", value: customer.full_name || "Invitado" }"""

app_js = app_js.replace(target_client, replacement_client)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
