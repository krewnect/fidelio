import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_render = """function renderCRMTable() {
        const crmTableBody = document.getElementById('crm-table-body');
        const crmSearchInput = document.getElementById('crm-search-input');
        const crmFilterTier = document.getElementById('crm-filter-tier');
        const crmFilterStatus = document.getElementById('crm-filter-status');
        const crmFilterMonth = document.getElementById('crm-filter-month');
        const crmCountBadge = document.getElementById('crm-count-badge');
        
        if (!crmTableBody) return;"""

new_render = """function renderCRMTable() {
        const crmTableBody = document.getElementById('crm-table-body');
        const crmSearchInput = document.getElementById('crm-search-input');
        const crmFilterTier = document.getElementById('crm-filter-tier');
        const crmFilterStatus = document.getElementById('crm-filter-status');
        const crmFilterMonth = document.getElementById('crm-filter-month');
        const crmCountBadge = document.getElementById('crm-count-badge');
        
        if (!crmTableBody || !state || !state.customers) return;"""

if old_render in js:
    js = js.replace(old_render, new_render)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v2.js renderCRMTable patched.")
else:
    print("WARNING: Could not find old_render in dashboard_v2.js")

