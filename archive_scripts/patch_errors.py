with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make checkRedundancy safe
if "window.checkRedundancy = function() {" in js:
    js = js.replace("""window.checkRedundancy = function() {
    const campSel = document.getElementById('builder-campaign-select');""",
    """window.checkRedundancy = function() {
    try {
        const campSel = document.getElementById('builder-campaign-select');""")
    js = js.replace("""    if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = isCamp ? 'none' : 'block';
    if(programTypeContainer) programTypeContainer.style.display = isCamp ? 'none' : 'block';
};""", """    if(rewardInput && rewardInput.parentElement) rewardInput.parentElement.style.display = isCamp ? 'none' : 'block';
    if(programTypeContainer) programTypeContainer.style.display = isCamp ? 'none' : 'block';
    } catch (e) { console.error("checkRedundancy error:", e); }
};""")

with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Patched checkRedundancy.")
