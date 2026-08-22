import re

with open('merchant-public.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                // If multiple campaigns, show dropdown
                if (visibleCampaigns.length > 1) {"""

replacement = """                // DEBUG: Show exactly what was fetched
                console.log("FETCHED CAMPAIGNS:", visibleCampaigns);
                const subtitle = document.getElementById('business-subtitle');
                if (subtitle) subtitle.innerHTML += `<br><span style="font-size:10px; color:red;">DEBUG: Campaigns found: ${visibleCampaigns.length}</span>`;

                // If multiple campaigns, show dropdown
                if (visibleCampaigns.length > 1) {"""

if target in html:
    html = html.replace(target, replacement)
    with open('merchant-public.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected DEBUG script")
else:
    print("Target not found")
