import re

with open('dashboard.js', 'r') as f:
    js = f.read()

old_listener = """    // BULLETPROOF EVENT DELEGATION
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

new_listener = """    // BULLETPROOF EVENT DELEGATION DYNAMIC
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('#btn-add-branch-modal');
        if (btn) {
            e.preventDefault();
            console.log("Btn add branch clicked!");
            if (!state.branches) state.branches = [];
            
            if (state.branches.length >= 20) {
                const upsell = document.getElementById('modal-upsell-branches');
                if (upsell) upsell.style.display = 'flex';
            } else {
                const addModal = document.getElementById('modal-add-branch');
                if (addModal) addModal.style.display = 'flex';
                
                const dynName = document.getElementById('branch-name');
                const dynManager = document.getElementById('branch-manager');
                const dynPhone = document.getElementById('branch-phone');
                const dynMaps = document.getElementById('branch-maps-url');
                const dynLat = document.getElementById('branch-lat');
                const dynLng = document.getElementById('branch-lng');
                const dynNotes = document.getElementById('branch-notes');
                
                if (dynName) dynName.value = '';
                if (dynManager) dynManager.value = '';
                if (dynPhone) dynPhone.value = '';
                if (dynMaps) dynMaps.value = '';
                if (dynLat) dynLat.value = '';
                if (dynLng) dynLng.value = '';
                if (dynNotes) dynNotes.value = '';
            }
        }
    });"""

js = js.replace(old_listener, new_listener)

with open('dashboard.js', 'w') as f:
    f.write(js)
