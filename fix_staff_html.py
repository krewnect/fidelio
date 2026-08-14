import re

with open('index.html', 'r') as f:
    html = f.read()

old_staff_start = '<!-- STAFF TAB -->'
old_staff_end = '</section>'
start_idx = html.find(old_staff_start)
end_idx = html.find(old_staff_end, start_idx) + len(old_staff_end)

if start_idx != -1 and end_idx != -1:
    old_staff = html[start_idx:end_idx]
    
    new_staff = """<!-- STAFF TAB -->
            <section id="tab-staff" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">SEGURIDAD Y ROLES</span>
                        <h1>Cajeros y Equipo</h1>
                        <p>Gestiona quién tiene acceso al escáner de la sucursal o al panel central.</p>
                    </div>
                </div>
                
                <div class="accordion-card" style="margin-bottom: 24px;">
                    <h3 style="margin-bottom:20px; font-size: 16px;"><i class="fa-solid fa-user-plus" style="color:var(--accent-violet); margin-right:8px;"></i> Invitar Nuevo Miembro</h3>
                    
                    <div style="display:flex; gap: 20px; flex-wrap: wrap;">
                        <!-- Role Selection -->
                        <div style="flex: 1; min-width: 300px;">
                            <label style="display:block; margin-bottom:12px; font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">1. Selecciona el Rol</label>
                            
                            <div class="role-selector">
                                <label class="role-card active" id="role-scanner-card">
                                    <input type="radio" name="staff_role" value="scanner" checked style="display:none;">
                                    <div class="role-icon" style="color:#059669; background:rgba(16, 185, 129, 0.1);"><i class="fa-solid fa-mobile-screen"></i></div>
                                    <div class="role-info">
                                        <h4>Usuario Escáner</h4>
                                        <p>Solo pueden abrir el lector QR para cobrar y dar puntos. No ven el panel.</p>
                                    </div>
                                    <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                                </label>

                                <label class="role-card" id="role-system-card">
                                    <input type="radio" name="staff_role" value="system" style="display:none;">
                                    <div class="role-icon" style="color:var(--accent-violet); background:rgba(139, 92, 246, 0.1);"><i class="fa-solid fa-laptop-code"></i></div>
                                    <div class="role-info">
                                        <h4>Acceso Sistema</h4>
                                        <p>Acceso al dashboard y métricas. Pueden añadir escáneres, pero no otros admins.</p>
                                    </div>
                                    <div class="role-check"><i class="fa-solid fa-circle-check"></i></div>
                                </label>
                            </div>
                        </div>

                        <!-- User Details Form -->
                        <div style="flex: 1; min-width: 300px;">
                            <label style="display:block; margin-bottom:12px; font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">2. Datos de Acceso</label>
                            
                            <div class="form-group">
                                <input type="text" id="staff-name" class="fidelio-input" placeholder="Nombre completo (Ej. Roberto Cajero 1)">
                            </div>
                            <div class="form-group">
                                <input type="email" id="staff-email" class="fidelio-input" placeholder="Correo electrónico de acceso">
                            </div>
                            <div class="form-group" style="margin-bottom: 24px;">
                                <input type="password" id="staff-password" class="fidelio-input" placeholder="Contraseña temporal (mínimo 6 caracteres)">
                            </div>
                            
                            <button id="btn-create-staff" class="btn-primary" style="width:100%; justify-content:center; padding: 14px;">
                                Enviar Invitación
                            </button>
                            <p style="font-size:11px; color:var(--text-muted); text-align:center; margin-top:12px;">
                                <i class="fa-solid fa-shield-halved"></i> La creación de roles de Sistema será verificada por seguridad.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Staff Table -->
                <div class="accordion-card">
                    <div class="card-title-bar" style="margin-bottom: 20px;">
                        <h3 style="font-size: 16px;"><i class="fa-solid fa-users-gear" style="color:var(--text-muted); margin-right:8px;"></i> Directorio de Equipo</h3>
                    </div>
                    
                    <div style="overflow-x: auto;">
                        <table class="crm-table">
                            <thead>
                                <tr>
                                    <th>Usuario</th>
                                    <th>Contacto</th>
                                    <th>Rol de Acceso</th>
                                    <th>Estado</th>
                                    <th style="text-align:right;">Acciones</th>
                                </tr>
                            </thead>
                            <tbody id="staff-table-body">
                                <tr><td colspan="5" style="text-align:center; color: var(--text-muted); padding: 30px;">Cargando equipo...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>"""
    
    html = html.replace(old_staff, new_staff)
    
    with open('index.html', 'w') as f:
        f.write(html)
    print("HTML updated")
else:
    print("Could not find STAFF section")
