import re

with open('merchant-public.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                visibleCampaigns = camps || [];
                const isProfessional = merch.business_type === 'professional' || (merch.industry && merch.industry.toLowerCase().includes('professional'));
                
                if (isProfessional && visibleCampaigns.length > 0) {
                    // Force professionals to only use their first campaign to avoid dropdowns
                    visibleCampaigns = [ visibleCampaigns[0] ];
                }"""

replacement = """                visibleCampaigns = camps || [];
                // Sort campaigns so the most recently created/edited one is first
                visibleCampaigns.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                
                const isProfessional = merch.business_type === 'professional' || (merch.industry && merch.industry.toLowerCase().includes('professional'));
                
                if (isProfessional && visibleCampaigns.length > 0) {
                    // Force professionals to only use their newest campaign to avoid dropdowns
                    visibleCampaigns = [ visibleCampaigns[0] ];
                }"""

text = text.replace(target, replacement)

with open('merchant-public.html', 'w', encoding='utf-8') as f:
    f.write(text)
