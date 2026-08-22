import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix selectCampaign
target1 = """        // Show builder tab
        document.getElementById('nav-builder').style.display = 'inline-block';
        if (!autoInit) {
            document.getElementById('nav-builder').click();
        }"""
replacement1 = """        // FUSION ROUTING: Manual Tab Switch because button is hidden
        if (!autoInit) {
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
            
            const builderTab = document.getElementById('tab-builder');
            if(builderTab) builderTab.classList.add('active');
            
            const campBtn = document.querySelector('.nav-tab[data-tab="tab-campaigns"]');
            if(campBtn) campBtn.classList.add('active');
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }"""
js = js.replace(target1, replacement1)


# Check applyQuickTemplate
target2 = """    // FUSION ROUTING
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
    
    const builderTab = document.getElementById('tab-builder');
    if(builderTab) builderTab.classList.add('active');
    
    const campBtn = document.querySelector('.nav-tab[data-tab="tab-campaigns"]');
    if(campBtn) campBtn.classList.add('active');"""

# Wait, I didn't actually inject target2 in applyQuickTemplate because the previous script failed!
# Let's fix applyQuickTemplate properly:
# We know applyQuickTemplate ends with `showToast(... "success");` and maybe some routing?
# Let's search for applyQuickTemplate in dashboard_v2.js
