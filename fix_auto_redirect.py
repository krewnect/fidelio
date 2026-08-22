import re

def fix_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            js = f.read()
            
        # 1. Update loadCampaigns call
        js = re.sub(r'selectCampaign\(data\.campaigns\[0\]\.id\);', r'selectCampaign(data.campaigns[0].id, true);', js)
        
        # 2. Update selectCampaign signature and logic
        # Find: window.selectCampaign = async function(id) {
        js = re.sub(r'window\.selectCampaign = async function\(id\) \{', 'window.selectCampaign = async function(id, autoInit = false) {', js)
        
        # Find the click and wrap it
        target_click = """        document.getElementById('nav-builder').style.display = 'inline-block';
        document.getElementById('nav-builder').click();"""
        replacement_click = """        document.getElementById('nav-builder').style.display = 'inline-block';
        if (!autoInit) {
            document.getElementById('nav-builder').click();
        }"""
        
        # Another possible variation
        target_click_2 = """    document.getElementById('nav-builder').style.display = 'inline-block';
    document.getElementById('nav-builder').click();"""
        replacement_click_2 = """    document.getElementById('nav-builder').style.display = 'inline-block';
    if (!autoInit) {
        document.getElementById('nav-builder').click();
    }"""
        
        js = js.replace(target_click, replacement_click)
        js = js.replace(target_click_2, replacement_click_2)

        # 3. Aggressive dropdown populate everywhere it might be useful, just in case
        target_dropdown = """        state.campaigns = data.campaigns;"""
        replacement_dropdown = """        state.campaigns = data.campaigns;
        if (!window.state) window.state = {};
        window.state.campaigns = data.campaigns;
        const stripeSel = document.getElementById('stripe-campaign-select');
        if (stripeSel) {
            stripeSel.innerHTML = '<option value="">-- Selecciona una tarjeta/campaña --</option>';
            data.campaigns.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.textContent = c.name || c.type || 'Programa';
                stripeSel.appendChild(opt);
            });
        }"""
        
        js = js.replace(target_dropdown, replacement_dropdown)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"Fixed {filename}")
    except Exception as e:
        print(f"Failed to fix {filename}: {e}")

fix_file('dashboard.js')
fix_file('live_dashboard.js')
