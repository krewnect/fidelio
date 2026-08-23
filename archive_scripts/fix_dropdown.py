import re

with open('merchant-public.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                const isProfessional = merch.business_type === 'professional' || (merch.industry && merch.industry.toLowerCase().includes('professional'));
                
                if (isProfessional && visibleCampaigns.length > 0) {
                    // Force professionals to only use their newest campaign to avoid dropdowns
                    visibleCampaigns = [ visibleCampaigns[0] ];
                }"""

replacement = """                // const isProfessional = merch.business_type === 'professional';
                // Remove the forced 1-campaign restriction so dropdown works for everyone."""

if target in html:
    html = html.replace(target, replacement)
    with open('merchant-public.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed dropdown restriction")
else:
    print("Target not found")
