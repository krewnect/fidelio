import re

with open('dashboard.js', 'r') as f:
    js = f.read()

old_listener = """    if (btnSubmitBranch) {
        btnSubmitBranch.addEventListener('click', () => {
            if (!bName.value || !bLat.value || !bLng.value) {
                showToast("El nombre y coordenadas son obligatorios", "warning");
                return;
            }
            
            const newBranch = {
                id: Date.now(),
                name: bName.value,
                manager: bManager.value,
                phone: bPhone.value,
                mapsUrl: bMaps.value,
                lat: parseFloat(bLat.value),
                lng: parseFloat(bLng.value),
                notes: bNotes.value
            };
            
            state.branches.push(newBranch);
            
            
            modalAddBranch.style.display = 'none';
            renderBranches();
            showToast(`Sucursal "${newBranch.name}" guardada con éxito.`, "success");
        });
    }"""

new_listener = """    // BULLETPROOF EVENT DELEGATION DYNAMIC FOR SUBMIT
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('#btn-submit-branch');
        if (btn) {
            e.preventDefault();
            console.log("Btn submit branch clicked!");
            
            const dynName = document.getElementById('branch-name');
            const dynManager = document.getElementById('branch-manager');
            const dynPhone = document.getElementById('branch-phone');
            const dynMaps = document.getElementById('branch-maps-url');
            const dynLat = document.getElementById('branch-lat');
            const dynLng = document.getElementById('branch-lng');
            const dynNotes = document.getElementById('branch-notes');
            const addModal = document.getElementById('modal-add-branch');
            
            if (!dynName.value || !dynLat.value || !dynLng.value) {
                showToast("El nombre y coordenadas son obligatorios", "warning");
                return;
            }
            
            const newBranch = {
                id: Date.now(),
                name: dynName.value,
                manager: dynManager ? dynManager.value : '',
                phone: dynPhone ? dynPhone.value : '',
                mapsUrl: dynMaps ? dynMaps.value : '',
                lat: parseFloat(dynLat.value),
                lng: parseFloat(dynLng.value),
                notes: dynNotes ? dynNotes.value : ''
            };
            
            if (!state.branches) state.branches = [];
            state.branches.push(newBranch);
            
            if (addModal) addModal.style.display = 'none';
            renderBranches();
            showToast(`Sucursal "${newBranch.name}" agregada con éxito a la lista local. Recuerda darle a Guardar y Actualizar Tarjetas al final.`, "success");
        }
    });"""

js = js.replace(old_listener, new_listener)

with open('dashboard.js', 'w') as f:
    f.write(js)
