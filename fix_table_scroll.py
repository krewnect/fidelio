import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace table-layout: auto and overflow-x: auto to enforce a strict fixed layout without scrollbars
old_table = """                <div class="content-panel" style="background: #ffffff; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); overflow-x: auto;">
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left; table-layout: auto;">"""

new_table = """                <div class="content-panel" style="background: #ffffff; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left; table-layout: fixed;">"""

html = html.replace(old_table, new_table)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Table layout fixed to prevent horizontal scrolling.")
