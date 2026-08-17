import re

filepath = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js'

with open(filepath, 'r') as f:
    content = f.read()

replacement = """
        // Meter UI
        const meter = document.getElementById('founder-meter-text');
        if (meter) {
            const left = Math.max(0, 25 - totalFoundersUsed);
            meter.innerHTML = `<i class="fa-solid fa-fire"></i> ${left} / 25 Disponibles`;
            if (left === 0) meter.style.color = 'var(--text-muted)';
        }

        const badge = document.getElementById('pricing-tier-badge');
        const amt = document.getElementById('pricing-amount');
        const period = document.getElementById('pricing-period');
        const desc = document.getElementById('pricing-description');
        
        const hasCustomPrice = window.merchantData && window.merchantData.custom_price !== null && window.merchantData.custom_price !== undefined;

        if (hasCustomPrice) {
            if (badge) {
                badge.style.background = 'linear-gradient(135deg, #10B981 0%, #059669 100%)';
                badge.style.color = 'white';
                badge.innerHTML = 'TARIFA PREFERENCIAL';
            }
            if (amt) amt.textContent = window.merchantData.custom_price.toLocaleString();
            if (desc) desc.textContent = 'Precio especial asignado. Sucursales ilimitadas.';
            if (period) period.textContent = 'mes';
            
            const toggleCycle = document.getElementById('billing-cycle-toggle');
            if (toggleCycle) {
                toggleCycle.disabled = true;
                toggleCycle.parentElement.style.opacity = '0.5';
            }
        }
        else if (isFounder) {
"""

pattern = re.compile(r'        // Meter UI.*?        if \(isFounder\) \{', re.DOTALL)
new_content = pattern.sub(replacement.strip('\n'), content)

# I also need to make sure merchantData is available to window.
# In loadDataFromSupabase:
new_content = new_content.replace('merchantData = newMerchant;', 'merchantData = newMerchant;\n        window.merchantData = merchantData;')
new_content = new_content.replace('merchantData = merchantData;', '') # Just in case

# At the end of loadDataFromSupabase it just assigns state, but I can add window.merchantData = merchantData early on.
new_content = new_content.replace('const { data: custData } = await window.supabaseClient', 'window.merchantData = merchantData;\n        const { data: custData } = await window.supabaseClient')

with open(filepath, 'w') as f:
    f.write(new_content)
