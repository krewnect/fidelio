import re

with open('pass.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We are going to replace everything from "let customer = null;" down to "merchant = realMerchant;"
# Wait, my previous script changed that part. Let's just do a regex replace from "let customer = null;" to "merchant = realMerchant;\\s*\\}"

pattern = re.compile(r'let customer = null;.*?merchant = realMerchant;\s*\}', re.DOTALL)

replacement = """
                const apiRes = await fetch(`/api/wallet/data?c=${customerId}&camp=${campaignId}`);
                const apiData = await apiRes.json();
                
                if (!apiData.success) {
                    throw new Error(apiData.error || "Pase inválido");
                }
                
                let customer = apiData.customer;
                let campaign = apiData.campaign;
                let merchant = apiData.merchant;
"""

html = pattern.sub(replacement, html)

with open('pass.html', 'w', encoding='utf-8') as f:
    f.write(html)
