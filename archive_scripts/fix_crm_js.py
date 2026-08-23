import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# I will replace the entire renderCRMTable function
old_render_start = "function renderCRMTable() {"
# Find the end of renderCRMTable
end_idx = js.find("function updatePassRender", js.find(old_render_start))
if end_idx != -1:
    # Go back to the end of the previous function
    end_idx = js.rfind("}", 0, end_idx) + 1
    old_func = js[js.find(old_render_start):end_idx]

    new_func = """function renderCRMTable() {
        const crmTableBody = document.getElementById('crm-table-body');
        const crmSearchInput = document.getElementById('crm-search-input');
        const crmFilterTier = document.getElementById('crm-filter-tier');
        const crmFilterStatus = document.getElementById('crm-filter-status');
        const crmFilterMonth = document.getElementById('crm-filter-month');
        const crmCountBadge = document.getElementById('crm-count-badge');
        
        if (!crmTableBody) return;

        const searchTerm = (crmSearchInput?.value || '').toLowerCase();
        const tierFilter = crmFilterTier?.value || 'all';
        const statusFilter = crmFilterStatus?.value || 'all';
        const monthFilter = crmFilterMonth?.value || 'all';
        
        const now = new Date();
        const currentMonth = String(now.getMonth() + 1).padStart(2, '0');

        let totalLTV = 0;
        let totalFreqDays = 0;
        let validFreqCount = 0;
        let churnRiskCount = 0;

        // PRE-PROCESS CUSTOMERS FOR METRICS
        const processedCustomers = state.customers.map(c => {
            const balance = c.current_balance || 0;
            const spent = parseFloat(c.lifetime_value || 0);
            totalLTV += spent;
            
            const tier = spent > 3000 ? 'Oro VIP' : (spent > 1000 ? 'Plata VIP' : 'Bronce VIP');
            
            const createdDate = new Date(c.created_at || now);
            const lastVisitDate = new Date(c.last_visit || c.created_at || now);
            const daysSinceRegistration = Math.max(1, Math.floor((now - createdDate) / (1000 * 60 * 60 * 24)));
            const daysSinceLastVisit = Math.floor((now - lastVisitDate) / (1000 * 60 * 60 * 24));
            
            const visits = parseInt(c.visits || 0);
            
            // Frequency calculation (days per visit)
            let freqDays = 0;
            let freqText = 'Nuevo';
            if (visits > 1) {
                freqDays = daysSinceRegistration / visits;
                freqText = `1 visita c/${Math.round(freqDays)} días`;
                totalFreqDays += freqDays;
                validFreqCount++;
            } else if (visits === 1) {
                freqText = '1 visita';
            }
            
            // Churn Risk (if they haven't visited in 2x their normal frequency, or > 60 days)
            let status = 'activo';
            let statusClass = 'activo';
            let statusText = 'Activo';
            
            if (visits === 0) {
                status = 'nuevo';
                statusClass = 'bronce';
                statusText = 'Nuevo';
            } else if (daysSinceLastVisit > 60 || (freqDays > 0 && daysSinceLastVisit > (freqDays * 2.5))) {
                status = 'riesgo';
                statusClass = 'riesgo';
                statusText = 'En Riesgo';
                churnRiskCount++;
            }
            
            // Birthday formatting
            let bdayFormatted = 'N/A';
            let bdayMonth = null;
            let isBirthdayMonth = false;
            if (c.birthday) {
                const bDate = new Date(c.birthday + 'T12:00:00Z'); // force midday to avoid timezone shift
                bdayFormatted = bDate.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
                bdayMonth = String(bDate.getMonth() + 1).padStart(2, '0');
                isBirthdayMonth = (bdayMonth === currentMonth);
            }
            
            // Anniversary
            const annivFormatted = createdDate.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' });
            const lastVisitFormatted = lastVisitDate.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });

            return {
                ...c,
                computed: {
                    balance, spent, tier, status, statusClass, statusText, freqText,
                    bdayFormatted, bdayMonth, isBirthdayMonth, annivFormatted, lastVisitFormatted, daysSinceLastVisit
                }
            };
        });

        // UPDATE KPI CARDS
        const kpiTotal = document.getElementById('kpi-total-customers');
        const kpiAvgSpent = document.getElementById('kpi-avg-spent');
        const kpiAvgFreq = document.getElementById('kpi-avg-freq');
        const kpiChurn = document.getElementById('kpi-churn-risk');
        
        if (kpiTotal) kpiTotal.textContent = state.customers.length;
        if (kpiAvgSpent) kpiAvgSpent.textContent = `$${state.customers.length ? (totalLTV / state.customers.length).toFixed(2) : 0} MXN`;
        if (kpiAvgFreq) kpiAvgFreq.textContent = validFreqCount ? `${Math.round(totalFreqDays / validFreqCount)} días` : 'N/A';
        if (kpiChurn) kpiChurn.textContent = churnRiskCount;

        // FILTER
        const filtered = processedCustomers.filter(c => {
            const matchesSearch = c.name.toLowerCase().includes(searchTerm) || 
                                  (c.phone && c.phone.includes(searchTerm)) || 
                                  (c.email && c.email.toLowerCase().includes(searchTerm)) ||
                                  (c.id && c.id.toLowerCase().includes(searchTerm));
            
            const matchesTier = tierFilter === 'all' || c.computed.tier === tierFilter;
            const matchesStatus = statusFilter === 'all' || c.computed.status === statusFilter;
            const matchesMonth = monthFilter === 'all' || c.computed.bdayMonth === monthFilter;

            return matchesSearch && matchesTier && matchesStatus && matchesMonth;
        });

        if (crmCountBadge) crmCountBadge.textContent = filtered.length;
        crmTableBody.innerHTML = '';

        if (filtered.length === 0) {
            crmTableBody.innerHTML = `<tr><td colspan="9" style="text-align:center; color: var(--text-muted); padding: 30px;">No se encontraron registros de clientes.</td></tr>`;
            return;
        }

        filtered.forEach(c => {
            const tr = document.createElement('tr');
            const comp = c.computed;
            const tierClass = comp.tier.includes('Oro') ? 'oro' : comp.tier.includes('Plata') ? 'plata' : 'bronce';
            const bdayAlert = comp.isBirthdayMonth ? `<i class="fa-solid fa-cake-candles" style="color:var(--accent-violet); margin-right:4px;" title="¡Cumpleaños este mes!"></i>` : `<i class="fa-solid fa-cake-candles" style="color:var(--text-muted); margin-right:4px;"></i>`;

            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${c.name.charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${c.name}</strong>
                            <small style="display:block; color:var(--text-muted);">${c.id.substring(0,8)}...</small>
                        </div>
                    </div>
                </td>
                <td>
                    <strong>${c.phone || 'N/A'}</strong>
                    <small style="display:block; color:var(--text-muted);">${c.email || 'Sin correo'}</small>
                </td>
                <td>
                    <div style="font-size:13px;">
                        <strong>${bdayAlert} ${comp.bdayFormatted}</strong>
                        <small style="display:block; color:var(--text-muted); margin-top:2px;"><i class="fa-solid fa-calendar-plus" style="margin-right:4px;"></i>${comp.annivFormatted}</small>
                    </div>
                </td>
                <td><span class="tier-pill ${tierClass}">${comp.tier}</span></td>
                <td>
                    <strong><i class="fa-solid fa-stamp" style="color:var(--accent-violet);"></i> ${c.visits || 0}/${state.stampsTotal || 5}</strong>
                    <small style="display:block; color:var(--text-muted);">$${comp.balance.toFixed(2)} cash</small>
                </td>
                <td><strong>$${comp.spent.toFixed(2)} MXN</strong></td>
                <td>
                    <strong style="color:var(--fidelio-violet);">${comp.freqText}</strong>
                    <small style="display:block; color:var(--text-muted);">Última: ${comp.lastVisitFormatted}</small>
                </td>
                <td><span class="badge-status ${comp.statusClass}">${comp.statusText}</span></td>
                <td>
                    <div style="display:flex; gap: 4px;">
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px;" title="Ver QR de Cliente" onclick="window.showCustomerQR('${c.id}', '${c.name.replace(/'/g, "\\'")}')">
                            <i class="fa-solid fa-qrcode"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px;" title="Enviar Promo" onclick="alert('Iniciando envío de promo directo a ${c.email || c.phone}')">
                            <i class="fa-solid fa-bullhorn"></i>
                        </button>
                    </div>
                </td>
            `;
            crmTableBody.appendChild(tr);
        });
    }"""
    
    js = js.replace(old_func, new_func)
    
    # Also add event listeners for the new filters
    init_end = js.find("function renderCRMTable")
    if init_end != -1:
        listeners = """
    // Listeners para CRM
    document.getElementById('crm-search-input')?.addEventListener('input', renderCRMTable);
    document.getElementById('crm-filter-tier')?.addEventListener('change', renderCRMTable);
    document.getElementById('crm-filter-status')?.addEventListener('change', renderCRMTable);
    document.getElementById('crm-filter-month')?.addEventListener('change', renderCRMTable);
    
"""
        js = js[:init_end] + listeners + js[init_end:]

    with open('dashboard.js', 'w') as f:
        f.write(js)
    print("JS updated")
else:
    print("Function not found")
