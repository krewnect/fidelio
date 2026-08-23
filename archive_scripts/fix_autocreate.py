import re

with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_insert = """                .insert([{
                    id: merchantId,
                    business_name: "Mi Negocio",
                    industry: "restaurant",
                    color_primary: "#090d16",
                    color_accent: "#5b0eb8","""

new_insert = """                .insert([{
                    id: merchantId,
                    business_name: "Mi Negocio",
                    industry: "restaurant",
                    business_type: "business",
                    color_primary: "#090d16",
                    color_accent: "#5b0eb8","""

if old_insert in js:
    js = js.replace(old_insert, new_insert)
    with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v3.js auto-create patched.")
else:
    print("WARNING: Could not find old_insert in dashboard_v3.js")

