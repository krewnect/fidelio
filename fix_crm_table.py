import re
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add min-width to .crm-table
css = css.replace('.crm-table {\n    width: 100%;', '.crm-table {\n    width: 100%;\n    min-width: 1200px;')

# Add white-space: nowrap to th and td
css = css.replace('.crm-table th {\n    background: transparent;', '.crm-table th {\n    white-space: nowrap;\n    background: transparent;')
css = css.replace('.crm-table td {\n    padding: 16px 24px !important;', '.crm-table td {\n    white-space: nowrap;\n    padding: 16px 24px !important;')

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
