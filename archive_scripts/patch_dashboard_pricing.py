import re

filepath = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/dashboard.js'

with open(filepath, 'r') as f:
    content = f.read()

# Add the new updatePricingUI function right before `async function loadDataFromSupabase`
pricing_logic = """
    // --- PRICING & FOUNDER LOGIC ---
    let isFounder = false;
    let isAnnual = false;
    let totalFoundersUsed = 0;

    async function checkPricingStatus() {
        if (!window.supabaseClient || !window.merchantSession) return;
        const merchantId = window.merchantSession.user.id;
        
        // 1. Get total merchants to determine founder meter
        const { count, error } = await window.supabaseClient
            .from('merchants')
            .select('*', { count: 'exact', head: true });
        
        totalFoundersUsed = count || 0;
        
        // 2. Check if current merchant is a founder. 
        // For simplicity: if they registered when there were <= 50 merchants, they are a founder.
        // We can approximate by checking their position.
        const { data: myRankData } = await window.supabaseClient
            .from('merchants')
            .select('created_at')
            .eq('id', merchantId)
            .single();
            
        if (myRankData) {
            const { count: myRank } = await window.supabaseClient
                .from('merchants')
                .select('*', { count: 'exact', head: true })
                .lte('created_at', myRankData.created_at);
            
            isFounder = (myRank <= 50);
        }

        updatePricingUI();
    }

    function updatePricingUI() {
        const toggle = document.getElementById('billing-cycle-toggle');
        if (toggle) isAnnual = toggle.checked;

        // Meter UI
        const meter = document.getElementById('founder-meter-text');
        if (meter) {
            const left = Math.max(0, 50 - totalFoundersUsed);
            meter.innerHTML = `<i class="fa-solid fa-fire"></i> ${left} / 50 Disponibles`;
            if (left === 0) meter.style.color = 'var(--text-muted)';
        }

        const badge = document.getElementById('pricing-tier-badge');
        const amt = document.getElementById('pricing-amount');
        const period = document.getElementById('pricing-period');
        const desc = document.getElementById('pricing-description');

        if (isFounder) {
            if (badge) {
                badge.style.background = 'linear-gradient(135deg, #FFD700 0%, #FDB931 100%)';
                badge.innerHTML = 'LICENCIA FOUNDER (DE POR VIDA)';
            }
            if (amt) amt.textContent = isAnnual ? '9,999' : '999';
            if (desc) desc.textContent = 'Sucursales ilimitadas. Soporte VIP.';
        } else {
            if (badge) {
                badge.style.background = 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)';
                badge.style.color = 'white';
                badge.innerHTML = 'LICENCIA ESTÁNDAR';
            }
            if (amt) amt.textContent = isAnnual ? '19,999' : '1,999';
            if (desc) desc.textContent = 'Hasta 20 sucursales. $99 MXN por extra.';
        }

        if (period) period.textContent = isAnnual ? 'año' : 'mes';
    }

    // Bind toggle
    const toggleCycle = document.getElementById('billing-cycle-toggle');
    const labelMo = document.getElementById('label-monthly');
    const labelYr = document.getElementById('label-annual');
    if (toggleCycle) {
        toggleCycle.addEventListener('change', () => {
            if (labelMo) labelMo.style.color = toggleCycle.checked ? 'var(--text-muted)' : 'white';
            if (labelYr) labelYr.style.color = toggleCycle.checked ? 'white' : 'var(--text-muted)';
            updatePricingUI();
        });
        if (labelMo) labelMo.addEventListener('click', () => { toggleCycle.checked = false; toggleCycle.dispatchEvent(new Event('change')); });
        if (labelYr) labelYr.addEventListener('click', () => { toggleCycle.checked = true; toggleCycle.dispatchEvent(new Event('change')); });
    }

    // --- DATABASE SYNC ---
"""

# Replace `// --- DATABASE SYNC ---` with the new logic
content = content.replace("// --- DATABASE SYNC ---", pricing_logic)

# In `btnPayStripe` listener, we need to pass `billing_cycle` and `tier`
old_stripe_req = """
                const response = await fetch('/api/stripe/checkout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${window.merchantSession?.access_token || ''}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ promoCode })
                });
"""

new_stripe_req = """
                const billingCycle = document.getElementById('billing-cycle-toggle')?.checked ? 'annual' : 'monthly';
                const tier = window.isFounder ? 'founder' : 'standard';

                const response = await fetch('/api/stripe/checkout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${window.merchantSession?.access_token || ''}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ promoCode, billing_cycle: billingCycle, tier: tier })
                });
"""

content = content.replace(old_stripe_req, new_stripe_req.strip())

# Add checkPricingStatus() at the end of loadDataFromSupabase
load_data_end = "updatePassRender();"
content = content.replace(load_data_end, "updatePassRender();\n        await checkPricingStatus();\n        // Expose to window for stripe button\n        window.isFounder = isFounder;")

# Update Sub Status text in loadDataFromSupabase
sub_status_update = "state = {"
content = content.replace(sub_status_update, "document.getElementById('sub-status-text').innerHTML = merchantData.plan_status === 'active' ? '<i class=\"fa-solid fa-check-circle\"></i> Activo' : '<i class=\"fa-solid fa-clock\"></i> Pruebas / Inactivo';\n        state = {")

# Update "metrics-cards-issued"
content = content.replace("document.getElementById('header-business-category').textContent = preset.label;", "document.getElementById('header-business-category').textContent = preset.label;\n        if(document.getElementById('metrics-cards-issued')) document.getElementById('metrics-cards-issued').textContent = custData.length;")

with open(filepath, 'w') as f:
    f.write(content)
