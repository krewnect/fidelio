import re

with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update the tab interception logic in dashboard_v3.js
old_tab_logic = """            const targetTab = tab.getAttribute('data-tab');
            if (targetTab) {
                const targetElement = document.getElementById(targetTab);"""

new_tab_logic = """            const targetTab = tab.getAttribute('data-tab');
            if (targetTab) {
                // --- FIDELIO SOFT-PAYWALL INTERCEPTOR ---
                const proTabs = ['tab-autopilot', 'tab-crm', 'tab-settings']; // Agrega aquí las pestañas PRO
                const plan = window.merchantData ? (window.merchantData.business_type || 'basic').toLowerCase() : 'basic';
                const isPro = ['business', 'pro', 'enterprise'].includes(plan);
                
                if (proTabs.includes(targetTab) && !isPro) {
                    // Block access and show Upsell Modal
                    document.getElementById('upsell-modal-container').style.display = 'flex';
                    // Re-activate previous tab visually if needed, but for simplicity we just return
                    return;
                }
                // ----------------------------------------
                
                const targetElement = document.getElementById(targetTab);"""

js = js.replace(old_tab_logic, new_tab_logic)

# 2. Update visual plan label in UI
old_plan_logic = """    if (window.merchantData && (window.merchantData.business_type === 'professional' || window.merchantData.business_type === 'business' || window.merchantData.business_type === 'enterprise')) {
        document.getElementById('plan-badge').textContent = 'PRO';"""
# It seems this might exist or maybe not. Let's just do a generic replace if it exists.
if "document.getElementById('plan-badge')" not in js:
    js = js.replace("""window.merchantData = merchantData;""", """window.merchantData = merchantData;
        const planBadge = document.getElementById('plan-badge');
        if(planBadge) {
            const isProPlan = ['business', 'pro', 'enterprise'].includes((merchantData.business_type || '').toLowerCase());
            planBadge.textContent = isProPlan ? 'PRO' : 'Basic';
            planBadge.style.background = isProPlan ? 'linear-gradient(135deg, #8b5cf6, #d946ef)' : '#94a3b8';
        }""")

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 3. Inject Upsell Modal in index.html
modal_html = """
    <!-- UPSELL MODAL (Soft-Paywall) -->
    <div id="upsell-modal-container" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(15, 23, 42, 0.8); backdrop-filter:blur(10px); z-index:999999; align-items:center; justify-content:center;">
        <div style="background:white; border-radius:24px; width:90%; max-width:450px; padding:40px; text-align:center; box-shadow:0 25px 50px -12px rgba(0,0,0,0.5); position:relative; overflow:hidden;">
            <div style="position:absolute; top:0; left:0; right:0; height:8px; background:linear-gradient(135deg, #8b5cf6, #d946ef);"></div>
            <button onclick="document.getElementById('upsell-modal-container').style.display='none'" style="position:absolute; top:20px; right:20px; background:none; border:none; color:#94a3b8; font-size:20px; cursor:pointer; transition:0.2s;"><i class="fa-solid fa-times hover:text-zinc-900"></i></button>
            
            <div style="width:80px; height:80px; background:linear-gradient(135deg, #f3e8ff, #fae8ff); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 24px;">
                <i class="fa-solid fa-crown text-3xl" style="background:-webkit-linear-gradient(135deg, #8b5cf6, #d946ef); -webkit-background-clip:text; -webkit-text-fill-color:transparent;"></i>
            </div>
            
            <h2 style="font-size:24px; font-weight:800; color:#0f172a; margin-bottom:12px; font-family:var(--font-main);">Función Exclusiva PRO</h2>
            <p style="color:#64748b; font-size:15px; margin-bottom:32px; line-height:1.5;">Esta herramienta avanzada de inteligencia artificial y automatización solo está disponible en el plan Fidelio PRO. Desbloquea todo el potencial de tu negocio.</p>
            
            <button onclick="window.location.href='https://billing.stripe.com/p/login/test_YOUR_STRIPE_LINK'" style="width:100%; padding:16px; border-radius:12px; border:none; background:linear-gradient(135deg, #8b5cf6, #d946ef); color:white; font-size:16px; font-weight:700; cursor:pointer; box-shadow:0 10px 15px -3px rgba(139, 92, 246, 0.3); transition:transform 0.2s, box-shadow 0.2s; font-family:var(--font-main);" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'"><i class="fa-solid fa-bolt mr-2"></i> Actualizar a PRO</button>
            <p style="margin-top:16px; font-size:12px; color:#94a3b8;">Prueba de 14 días incluida. Cancela cuando quieras.</p>
        </div>
    </div>
</body>
"""

html = html.replace('</body>', modal_html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Injected soft-paywall interceptor and modal.")
