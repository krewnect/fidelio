import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Hide the program type selector for Professionals
target_select = """<div id="program-type-container">"""
html = html.replace(target_select, """<div id="program-type-container" class="plan-business-only">""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make sure that when a Professional loads a campaign, it defaults to stamps
target_select_campaign = """        state.restaurantName = camp.name || "Campaña";"""
replacement_select_campaign = """        
        // Force stamps for professionals
        if (window.merchantData && window.merchantData.business_type === 'professional') {
            const pType = document.getElementById('program-type-select');
            if (pType) pType.value = 'stamps';
            state.activeMode = 'stamps';
        }
        
        state.restaurantName = camp.name || "Campaña";"""

js = js.replace(target_select_campaign, replacement_select_campaign)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
