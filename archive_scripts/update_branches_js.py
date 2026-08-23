import re

with open('dashboard.js', 'r') as f:
    js = f.read()

new_branches_js = """    // --- SUCURSALES (GPS & UPSELL) MANAGER ---
    const branchesContainer = document.getElementById('branches-list-container');
    const btnAddBranchModal = document.getElementById('btn-add-branch-modal');
    
    // Modals
    const modalAddBranch = document.getElementById('modal-add-branch');
    const modalUpsell = document.getElementById('modal-upsell-branches');
    
    // Form Inputs
    const bName = document.getElementById('branch-name');
    const bManager = document.getElementById('branch-manager');
    const bPhone = document.getElementById('branch-phone');
    const bMaps = document.getElementById('branch-maps-url');
    const bLat = document.getElementById('branch-lat');
    const bLng = document.getElementById('branch-lng');
    const bNotes = document.getElementById('branch-notes');
    const btnSubmitBranch = document.getElementById('btn-submit-branch');

    function renderBranches() {
        if (!branchesContainer) return;
        
        if (!state.branches || state.branches.length === 0) {
            branchesContainer.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 20px;">No tienes sucursales registradas. Añade la primera.</p>';
            return;
        }
        
        branchesContainer.innerHTML = '';
        state.branches.forEach((b, idx) => {
            const div = document.createElement('div');
            div.style.cssText = "background:white; border:1px solid rgba(0,0,0,0.05); border-radius:12px; padding:20px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 4px 10px rgba(0,0,0,0.02); transition:var(--transition);";
            div.onmouseover = () => { div.style.borderColor = "rgba(139, 92, 246, 0.3)"; div.style.boxShadow = "0 10px 20px rgba(0,0,0,0.05)"; };
            div.onmouseout = () => { div.style.borderColor = "rgba(0,0,0,0.05)"; div.style.boxShadow = "0 4px 10px rgba(0,0,0,0.02)"; };
            
            div.innerHTML = `
                <div>
                    <h3 style="margin:0 0 4px 0; font-size:16px; font-weight:700; color:#111827;">${idx + 1}. ${b.name}</h3>
                    <div style="display:flex; gap:16px; font-size:13px; color:#6b7280; margin-bottom:8px;">
                        <span><i class="fa-solid fa-user"></i> ${b.manager || 'No asignado'}</span>
                        <span><i class="fa-solid fa-phone"></i> ${b.phone || 'Sin número'}</span>
                    </div>
                    <div style="font-size:12px; color:#9ca3af; display:flex; gap:16px;">
                        <span><i class="fa-solid fa-location-crosshairs"></i> GPS: ${parseFloat(b.lat).toFixed(4)}, ${parseFloat(b.lng).toFixed(4)} (Geofence 100m)</span>
                        ${b.mapsUrl ? `<a href="${b.mapsUrl}" target="_blank" style="color:var(--accent-violet); text-decoration:none; font-weight:600;"><i class="fa-solid fa-map"></i> Ver Maps</a>` : ''}
                    </div>
                </div>
                <button class="btn btn-outline" style="padding:8px 12px; border-radius:8px; color:#ef4444; border-color:#fee2e2;" onclick="removeBranch(${b.id})">
                    <i class="fa-solid fa-trash"></i>
                </button>
            `;
            branchesContainer.appendChild(div);
        });
        
        // Update Add Button UI based on limit
        if (btnAddBranchModal) {
            if (state.branches.length >= 20) {
                btnAddBranchModal.innerHTML = '<i class="fa-solid fa-crown"></i> Desbloquear Más Sucursales';
                btnAddBranchModal.style.background = 'linear-gradient(135deg, #1e1b4b 0%, #8b5cf6 100%)';
                btnAddBranchModal.style.border = 'none';
                btnAddBranchModal.style.color = 'white';
            } else {
                btnAddBranchModal.innerHTML = '<i class="fa-solid fa-plus"></i> Añadir Sucursal';
                btnAddBranchModal.style.background = 'var(--text-main)';
                btnAddBranchModal.style.border = 'none';
                btnAddBranchModal.style.color = 'white';
            }
        }
    }

    if (btnAddBranchModal) {
        btnAddBranchModal.addEventListener('click', () => {
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
    }
    
    if (btnSubmitBranch) {
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
            tenantDatabase[currentTenantId].branches = state.branches;
            
            modalAddBranch.style.display = 'none';
            renderBranches();
            showToast(`Sucursal "${newBranch.name}" guardada con éxito.`, "success");
        });
    }

    window.removeBranch = function(id) {
        if(confirm("¿Estás seguro de eliminar esta sucursal de la red de Wallet?")) {
            state.branches = state.branches.filter(b => b.id !== id);
            tenantDatabase[currentTenantId].branches = state.branches;
            renderBranches();
            showToast("Sucursal eliminada. Los clientes ya no recibirán push en esta ubicación.", "info");
        }
    };"""

pattern = r'// --- 20 SUCURSALES MANAGER RENDERING ---.*?window\.removeBranch = function\(id\) \{.*?showToast\("Sucursal eliminada\.", "info"\);\s*\};\s*'
html = re.sub(pattern, new_branches_js, js, flags=re.DOTALL)

with open('dashboard.js', 'w') as f:
    f.write(html)
