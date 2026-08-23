import re

with open('merchant-public.html', 'r', encoding='utf-8') as f:
    text = f.read()

target_js = """                visibleCampaigns = camps || [];
                if (merch.business_type === 'professional' || (merch.industry && merch.industry.toLowerCase().includes('professional'))) {
                    visibleCampaigns = visibleCampaigns.filter(c => c.type === 'stamps');
                }"""

replacement_js = """                visibleCampaigns = camps || [];
                const isProfessional = merch.business_type === 'professional' || (merch.industry && merch.industry.toLowerCase().includes('professional'));
                
                if (isProfessional && visibleCampaigns.length > 0) {
                    // Force professionals to only use their first campaign to avoid dropdowns
                    visibleCampaigns = [ visibleCampaigns[0] ];
                }"""

text = text.replace(target_js, replacement_js)

with open('merchant-public.html', 'w', encoding='utf-8') as f:
    f.write(text)
