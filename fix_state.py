import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        const data = await res.json();
        state.campaigns = data.campaigns;
        const list = document.getElementById('campaigns-list');"""

replacement = """        const data = await res.json();
        // Sort newest first
        if (data.campaigns && data.campaigns.length > 0) {
            data.campaigns.sort((a,b) => new Date(b.created_at) - new Date(a.created_at));
            if (!state.currentCampaignId) {
                // Initialize the designer with their newest campaign automatically
                state.currentCampaignId = data.campaigns[0].id;
                selectCampaign(data.campaigns[0].id);
            }
        }
        state.campaigns = data.campaigns;
        const list = document.getElementById('campaigns-list');"""

text = text.replace(target, replacement)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(text)
