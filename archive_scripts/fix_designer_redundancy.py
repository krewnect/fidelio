import re

# 1. Update index.html for CSS caching and add an ID to the program-type container
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make CSS dynamic to avoid caching issues during development
if 'href="styles.css?v=44"' in html:
    html = html.replace('<link rel="stylesheet" href="styles.css?v=44">', '<link id="dynamic-styles" rel="stylesheet" href="styles.css?v=44"><script>document.getElementById("dynamic-styles").href = "styles.css?v=" + new Date().getTime();</script>')

# Add an ID to the container of program-type-select so we can hide it easily
html = html.replace('<div>\n                                    <label class="premium-label">Tipo de Programa</label>\n                                    <select id="program-type-select"',
                   '<div id="program-type-container">\n                                    <label class="premium-label">Tipo de Programa</label>\n                                    <select id="program-type-select"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Index.html updated for CSS caching and container ID.")


# 2. Update dashboard.js to hide program-type-container in checkRedundancy
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_redundancy = """window.checkRedundancy = function() {
    const campSel = document.getElementById('builder-campaign-select');
    const isCamp = campSel ? !!campSel.value : !!state.currentCampaignId;
    
    const msgInput = document.getElementById('rest-desc');
    const rewardInput = document.getElementById('stamps-reward');
    
    if(isCamp) {
        if(msgInput && msgInput.parentElement) msgInput.parentElement.style.display = 'none';
        if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = 'none';
    } else {
        if(msgInput && msgInput.parentElement) msgInput.parentElement.style.display = 'block';
        if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = 'block';
    }
};"""

new_redundancy = """window.checkRedundancy = function() {
    const campSel = document.getElementById('builder-campaign-select');
    const isCamp = campSel ? !!campSel.value : !!state.currentCampaignId;
    
    const msgInput = document.getElementById('rest-desc');
    const rewardInput = document.getElementById('stamps-reward');
    const programTypeContainer = document.getElementById('program-type-container');
    
    if(isCamp) {
        if(msgInput && msgInput.parentElement) msgInput.parentElement.style.display = 'none';
        if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = 'none';
        if(programTypeContainer) programTypeContainer.style.display = 'none';
    } else {
        if(msgInput && msgInput.parentElement) msgInput.parentElement.style.display = 'block';
        if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = 'block';
        if(programTypeContainer) programTypeContainer.style.display = 'block';
    }
};"""

if old_redundancy in js:
    js = js.replace(old_redundancy, new_redundancy)
    print("Dashboard.js checkRedundancy updated.")
else:
    print("Could not find exact old_redundancy string in dashboard.js")

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)

