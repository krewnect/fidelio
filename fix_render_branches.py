import re

with open('dashboard.js', 'r') as f:
    js = f.read()

old_render = """    function renderBranches() {
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
                btnAddBranchModal.style.background = 'var(--accent-violet)';
                btnAddBranchModal.style.border = 'none';
                btnAddBranchModal.style.color = 'white';
            }
        }
    }"""

new_render = """    function renderBranches() {
        try {
            const dynBranchesContainer = document.getElementById('branches-list-container');
            const dynBtnAddBranchModal = document.getElementById('btn-add-branch-modal');
            
            if (!dynBranchesContainer) return;
            
            if (!state.branches || state.branches.length === 0) {
                dynBranchesContainer.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding: 20px;">No tienes sucursales registradas. Añade la primera.</p>';
            } else {
                dynBranchesContainer.innerHTML = '';
                state.branches.forEach((b, idx) => {
                    const div = document.createElement('div');
                    div.style.cssText = "background:white; border:1px solid rgba(0,0,0,0.05); border-radius:12px; padding:20px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 4px 10px rgba(0,0,0,0.02); transition:var(--transition);";
                    div.onmouseover = () => { div.style.borderColor = "rgba(139, 92, 246, 0.3)"; div.style.boxShadow = "0 10px 20px rgba(0,0,0,0.05)"; };
                    div.onmouseout = () => { div.style.borderColor = "rgba(0,0,0,0.05)"; div.style.boxShadow = "0 4px 10px rgba(0,0,0,0.02)"; };
                    
                    const latNum = parseFloat(b.lat);
                    const lngNum = parseFloat(b.lng);
                    const safeLat = isNaN(latNum) ? '0.0000' : latNum.toFixed(4);
                    const safeLng = isNaN(lngNum) ? '0.0000' : lngNum.toFixed(4);
                    
                    div.innerHTML = `
                        <div>
                            <h3 style="margin:0 0 4px 0; font-size:16px; font-weight:700; color:#111827;">${idx + 1}. ${b.name || 'Sucursal sin nombre'}</h3>
                            <div style="display:flex; gap:16px; font-size:13px; color:#6b7280; margin-bottom:8px;">
                                <span><i class="fa-solid fa-user"></i> ${b.manager || 'No asignado'}</span>
                                <span><i class="fa-solid fa-phone"></i> ${b.phone || 'Sin número'}</span>
                            </div>
                            <div style="font-size:12px; color:#9ca3af; display:flex; gap:16px;">
                                <span><i class="fa-solid fa-location-crosshairs"></i> GPS: ${safeLat}, ${safeLng} (Geofence 100m)</span>
                                ${b.mapsUrl ? `<a href="${b.mapsUrl}" target="_blank" style="color:var(--accent-violet); text-decoration:none; font-weight:600;"><i class="fa-solid fa-map"></i> Ver Maps</a>` : ''}
                            </div>
                        </div>
                        <button class="btn btn-outline" style="padding:8px 12px; border-radius:8px; color:#ef4444; border-color:#fee2e2;" onclick="removeBranch(${b.id})">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    `;
                    dynBranchesContainer.appendChild(div);
                });
            }
            
            // Update Add Button UI based on limit
            if (dynBtnAddBranchModal) {
                if (state.branches.length >= 20) {
                    dynBtnAddBranchModal.innerHTML = '<i class="fa-solid fa-crown"></i> Desbloquear Más Sucursales';
                    dynBtnAddBranchModal.style.background = 'linear-gradient(135deg, #1e1b4b 0%, #8b5cf6 100%)';
                    dynBtnAddBranchModal.style.border = 'none';
                    dynBtnAddBranchModal.style.color = 'white';
                } else {
                    dynBtnAddBranchModal.innerHTML = '<i class="fa-solid fa-plus"></i> Añadir Sucursal';
                    dynBtnAddBranchModal.style.background = 'var(--accent-violet)';
                    dynBtnAddBranchModal.style.border = 'none';
                    dynBtnAddBranchModal.style.color = 'white';
                }
            }
        } catch(e) {
            console.error("Error en renderBranches:", e);
        }
    }"""

js = js.replace(old_render, new_render)

with open('dashboard.js', 'w') as f:
    f.write(js)
