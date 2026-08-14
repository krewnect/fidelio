import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Add mock team to state
state_match = re.search(r'const state = \{.*?\};', js, re.DOTALL)
if state_match:
    old_state = state_match.group(0)
    if 'team:' not in old_state:
        new_state = old_state.replace(
            "customers: [],", 
            "customers: [],\n    team: [\n        { id: 'usr-001', name: 'Roberto Ordoñez', email: 'hola@fideliorewards.com', role: 'system', status: 'activo' },\n        { id: 'usr-002', name: 'Caja Principal', email: 'caja1@fideliorewards.com', role: 'scanner', status: 'activo' }\n    ],"
        )
        js = js.replace(old_state, new_state)

# Add renderTeamTable function
render_team_func = """
    function renderTeamTable() {
        const tbody = document.getElementById('staff-table-body');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        if (!state.team || state.team.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: var(--text-muted); padding: 30px;">No hay personal registrado.</td></tr>`;
            return;
        }
        
        state.team.forEach(member => {
            const tr = document.createElement('tr');
            
            const roleBadge = member.role === 'system' 
                ? `<span class="badge-status activo" style="background: rgba(139, 92, 246, 0.1); color: var(--accent-violet); border-color: rgba(139, 92, 246, 0.3);"><i class="fa-solid fa-laptop-code"></i> Sistema</span>`
                : `<span class="badge-status" style="background: rgba(16, 185, 129, 0.1); color: #059669; border-color: rgba(16, 185, 129, 0.3);"><i class="fa-solid fa-mobile-screen"></i> Escáner</span>`;
                
            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${member.name.charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${member.name}</strong>
                            <small style="display:block; color:var(--text-muted);">ID: ${member.id}</small>
                        </div>
                    </div>
                </td>
                <td>
                    <strong>${member.email}</strong>
                </td>
                <td>${roleBadge}</td>
                <td><span class="badge-status activo">Activo</span></td>
                <td style="text-align:right;">
                    <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:#ef4444; border-color:rgba(239, 68, 68, 0.2);" title="Revocar Acceso" onclick="alert('Funcionalidad de revocación disponible al conectar backend')">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }
"""

# Find where to insert it (after renderCRMTable)
end_crm_idx = js.find("function renderCRMTable")
end_crm_idx = js.find("}", end_crm_idx)
# Keep looking for the end of the function properly (crude way for python script)
while js[end_crm_idx:end_crm_idx+8] != "function" and js[end_crm_idx:end_crm_idx+1] != "":
    end_crm_idx = js.find("function", end_crm_idx+1)
    if end_crm_idx == -1:
        break

if end_crm_idx != -1:
    js = js[:end_crm_idx] + render_team_func + js[end_crm_idx:]
else:
    js += render_team_func

# Add JS bindings for the form
bindings = """
    // --- TEAM MANAGEMENT (RBAC) ---
    renderTeamTable();
    
    // Role selector UI
    const roleCards = document.querySelectorAll('.role-card');
    roleCards.forEach(card => {
        card.addEventListener('click', () => {
            roleCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            card.querySelector('input').checked = true;
        });
    });
    
    // Create button mockup
    const btnCreateStaff = document.getElementById('btn-create-staff');
    if (btnCreateStaff) {
        btnCreateStaff.addEventListener('click', () => {
            const name = document.getElementById('staff-name').value;
            const email = document.getElementById('staff-email').value;
            const pwd = document.getElementById('staff-password').value;
            const role = document.querySelector('input[name="staff_role"]:checked').value;
            
            if (!name || !email || !pwd) {
                alert('Por favor completa todos los campos.');
                return;
            }
            
            // Check permissions mockup
            if (role === 'system' && window.merchantSession?.user?.email !== 'hola@fideliorewards.com') {
                alert('ACCESO DENEGADO: Solo la cuenta Master Admin puede crear otros usuarios de Acceso Sistema.');
                return;
            }
            
            state.team.push({
                id: 'usr-' + Math.floor(Math.random() * 10000),
                name, email, role, status: 'activo'
            });
            renderTeamTable();
            
            document.getElementById('staff-name').value = '';
            document.getElementById('staff-email').value = '';
            document.getElementById('staff-password').value = '';
            alert('¡Invitación enviada y usuario ' + role + ' registrado exitosamente!');
        });
    }
"""

init_idx = js.find("renderCRMTable();")
if init_idx != -1:
    js = js[:init_idx] + bindings + js[init_idx:]

with open('dashboard.js', 'w') as f:
    f.write(js)
print("Dashboard JS updated for RBAC")
