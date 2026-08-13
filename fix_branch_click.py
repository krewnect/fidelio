import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Replace the direct event listener with an event delegation just to be 100% sure it fires
old_listener = """    if (btnAddBranchModal) {
        btnAddBranchModal.addEventListener('click', () => {
            if (!state.branches) state.branches = [];
            
            if (state.branches.length >= 20) {
                // Upsell Wall
                if (modalUpsell) modalUpsell.style.display = 'flex';
            } else {
                // Open Add Form
                if (modalAddBranch) modalAddBranch.style.display = 'flex';
                // Clear inputs
                bName.value = ''; bManager.value = ''; bPhone.value = ''; 
                bMaps.value = ''; bLat.value = ''; bLng.value = ''; bNotes.value = '';
            }
        });
    }"""

new_listener = """    // BULLETPROOF EVENT DELEGATION
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('#btn-add-branch-modal');
        if (btn) {
            e.preventDefault();
            console.log("Btn add branch clicked!");
            if (!state.branches) state.branches = [];
            
            if (state.branches.length >= 20) {
                if (modalUpsell) modalUpsell.style.display = 'flex';
            } else {
                if (modalAddBranch) modalAddBranch.style.display = 'flex';
                if (bName) bName.value = '';
                if (bManager) bManager.value = '';
                if (bPhone) bPhone.value = '';
                if (bMaps) bMaps.value = '';
                if (bLat) bLat.value = '';
                if (bLng) bLng.value = '';
                if (bNotes) bNotes.value = '';
            }
        }
    });"""

js = js.replace(old_listener, new_listener)

with open('dashboard.js', 'w') as f:
    f.write(js)
