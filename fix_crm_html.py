import re

with open('index.html', 'r') as f:
    html = f.read()

# Locate the old CRM tab
old_crm_start = '<!-- CRM TAB (Mock content to satisfy JS if needed) -->'
old_crm_end = '</section>'
start_idx = html.find(old_crm_start)
end_idx = html.find(old_crm_end, start_idx) + len(old_crm_end)

if start_idx != -1 and end_idx != -1:
    old_crm = html[start_idx:end_idx]
    
    new_crm = """<!-- CRM TAB -->
            <section id="tab-crm" class="tab-content">
                <div class="workspace-header">
                    <div>
                        <span class="workspace-eyebrow">BASE DE DATOS PRIVADA</span>
                        <h1>Clientes Fidelizados</h1>
                        <p>Gestión avanzada de retención, hábitos de consumo y recompensas de tu cartera.</p>
                    </div>
                    <div style="display:flex; gap:10px;">
                        <button class="btn btn-outline" onclick="alert('Exportación CSV/Excel se activará en la próxima actualización de backend')"><i class="fa-solid fa-download"></i> Exportar</button>
                        <button class="btn btn-primary" onclick="document.getElementById('modal-add-customer').classList.remove('hidden')"><i class="fa-solid fa-plus"></i> Añadir Cliente Manual</button>
                    </div>
                </div>
                
                <!-- KPI Dashboard -->
                <div class="stats-grid" style="margin-bottom: 24px;">
                    <div class="stat-card">
                        <div class="stat-icon" style="background: rgba(139, 92, 246, 0.1); color: var(--accent-violet);"><i class="fa-solid fa-users"></i></div>
                        <div class="stat-info">
                            <span class="stat-label">Total Clientes</span>
                            <span class="stat-value" id="kpi-total-customers">0</span>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon" style="background: rgba(16, 185, 129, 0.1); color: #10b981;"><i class="fa-solid fa-sack-dollar"></i></div>
                        <div class="stat-info">
                            <span class="stat-label">Gasto Promedio (LTV)</span>
                            <span class="stat-value" id="kpi-avg-spent">$0</span>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon" style="background: rgba(59, 130, 246, 0.1); color: #3b82f6;"><i class="fa-solid fa-calendar-check"></i></div>
                        <div class="stat-info">
                            <span class="stat-label">Frecuencia Promedio</span>
                            <span class="stat-value" id="kpi-avg-freq">0 días</span>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;"><i class="fa-solid fa-heart-crack"></i></div>
                        <div class="stat-info">
                            <span class="stat-label">En Riesgo (Churn)</span>
                            <span class="stat-value" id="kpi-churn-risk">0</span>
                        </div>
                    </div>
                </div>

                <div class="accordion-card">
                    <!-- Filtros -->
                    <div class="card-title-bar" style="margin-bottom: 20px; flex-wrap: wrap; gap: 10px;">
                        <div class="input-group" style="flex: 1; min-width: 250px;">
                            <i class="fa-solid fa-magnifying-glass"></i>
                            <input type="text" id="crm-search-input" placeholder="Buscar por nombre, teléfono, email, o ID..." class="form-input">
                        </div>
                        <div style="display:flex; gap: 10px; align-items:center;">
                            <select id="crm-filter-tier" class="form-input" style="padding-left: 10px; width: auto;">
                                <option value="all">Todos los Niveles</option>
                                <option value="Oro VIP">Oro VIP</option>
                                <option value="Plata VIP">Plata VIP</option>
                                <option value="Bronce VIP">Bronce VIP</option>
                            </select>
                            <select id="crm-filter-status" class="form-input" style="padding-left: 10px; width: auto;">
                                <option value="all">Todos los Estados</option>
                                <option value="activo">Activo</option>
                                <option value="riesgo">En Riesgo</option>
                                <option value="nuevo">Nuevo</option>
                            </select>
                            <select id="crm-filter-month" class="form-input" style="padding-left: 10px; width: auto;">
                                <option value="all">Cualquier Mes</option>
                                <option value="01">Enero</option>
                                <option value="02">Febrero</option>
                                <option value="03">Marzo</option>
                                <option value="04">Abril</option>
                                <option value="05">Mayo</option>
                                <option value="06">Junio</option>
                                <option value="07">Julio</option>
                                <option value="08">Agosto</option>
                                <option value="09">Septiembre</option>
                                <option value="10">Octubre</option>
                                <option value="11">Noviembre</option>
                                <option value="12">Diciembre</option>
                            </select>
                        </div>
                    </div>
                    
                    <div style="overflow-x: auto;">
                        <table class="crm-table">
                            <thead>
                                <tr>
                                    <th>Cliente</th>
                                    <th>Contacto</th>
                                    <th>Cumpleaños / Registro</th>
                                    <th>Nivel VIP</th>
                                    <th>Puntos / Visitas</th>
                                    <th>Gasto Total</th>
                                    <th>Frecuencia</th>
                                    <th>Estado</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody id="crm-table-body">
                                <!-- Se llena vía JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>"""
    
    html = html.replace(old_crm, new_crm)
    
    with open('index.html', 'w') as f:
        f.write(html)
    print("HTML updated")
else:
    print("Could not find CRM section")
