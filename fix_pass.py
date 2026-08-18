import re

with open('pass.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix 1: Scope of customerId and campaignId
target_scope_1 = """    <script>
        document.addEventListener('DOMContentLoaded', async () => {"""
replacement_scope_1 = """    <script>
        let globalCustomerId = null;
        let globalCampaignId = null;
        document.addEventListener('DOMContentLoaded', async () => {"""
text = text.replace(target_scope_1, replacement_scope_1)

target_scope_2 = """                const customerId = urlParams.get('id') || urlParams.get('c');
                const campaignId = urlParams.get('campaign');"""
replacement_scope_2 = """                const customerId = urlParams.get('id') || urlParams.get('c');
                const campaignId = urlParams.get('campaign');
                globalCustomerId = customerId;
                globalCampaignId = campaignId;"""
text = text.replace(target_scope_2, replacement_scope_2)

target_scope_3 = """        function downloadAppleWallet() {
            if (!customerId || !campaignId) {"""
replacement_scope_3 = """        function downloadAppleWallet() {
            if (!globalCustomerId || !globalCampaignId) {"""
text = text.replace(target_scope_3, replacement_scope_3)

target_scope_4 = """            const url = `/api/wallet/apple/${customerId}/${campaignId}`;"""
replacement_scope_4 = """            const url = `/api/wallet/apple/${globalCustomerId}/${globalCampaignId}`;"""
text = text.replace(target_scope_4, replacement_scope_4)

# Fix 2: VIP visibility for professionals
target_vip = """                if (merchant && merchant.business_type === 'professional') {"""
replacement_vip = """                const isProfessional = merchant && (merchant.business_type === 'professional' || (merchant.industry && merchant.industry.toLowerCase().includes('professional')));
                if (isProfessional) {"""
text = text.replace(target_vip, replacement_vip)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(text)
