import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace all builderTabBtn logic with direct routing
target_select_bad = """    const builderTabBtn = document.querySelector('.nav-tab[data-tab="tab-builder"]');
    if(builderTabBtn) {
        // We have to manually trigger the tab switch since the button is hidden
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-builder').classList.add('active');
        
        // Also highlight "Mis Campañas" in the sidebar so the user knows where they are
        const campBtn = document.querySelector('.nav-tab[data-tab="tab-campaigns"]');
        if(campBtn) campBtn.classList.add('active');
    }"""

replacement_select_good = """    // FUSION ROUTING
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
    
    const builderTab = document.getElementById('tab-builder');
    if(builderTab) builderTab.classList.add('active');
    
    const campBtn = document.querySelector('.nav-tab[data-tab="tab-campaigns"]');
    if(campBtn) campBtn.classList.add('active');
"""
js = js.replace(target_select_bad, replacement_select_good)

target_wizard = """        const builderTabBtn = document.querySelector('.nav-tab[data-tab="tab-builder"]');
        if(builderTabBtn) builderTabBtn.click();"""

js = js.replace(target_wizard, replacement_select_good)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
