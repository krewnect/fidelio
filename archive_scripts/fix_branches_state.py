import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Fix 1: Ensure state.branches is initialized in loadDataFromSupabase
patch1 = """            vipTiers: {
                bronce: { name: "Bronce", minSpent: 0, cashbackPercent: 5, perk: "Beneficio Base" },
                plata: { name: "Plata VIP", minSpent: 1000, cashbackPercent: 10, perk: "Beneficio Plata" },
                oro: { name: "Oro Elite", minSpent: 5000, cashbackPercent: 15, perk: "Beneficio Oro" }
            },
            branches: tenantDatabase[merchantData.id]?.branches || []"""

js = re.sub(r'vipTiers:\s*\{.*?\},', patch1 + ',', js, flags=re.DOTALL, count=1)

# Fix 2: Safety check in the click listener just in case
patch2 = """    if (btnAddBranchModal) {
        btnAddBranchModal.addEventListener('click', () => {
            if (!state.branches) state.branches = [];
            
            if (state.branches.length >= 20) {"""
js = js.replace("""    if (btnAddBranchModal) {
        btnAddBranchModal.addEventListener('click', () => {
            if (state.branches.length >= 20) {""", patch2)

with open('dashboard.js', 'w') as f:
    f.write(js)
