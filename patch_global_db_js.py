import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace loadGlobalDatabase
old_load = """    window.loadGlobalDatabase = async function() {
        if (!checkMasterAdmin()) return;
        const tbody = document.getElementById('global-db-body');
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Cargando base de datos global...</td></tr>';
        
        // Obtener clientes junto con los datos de su restaurante
        const { data, error } = await window.supabaseClient
            .from('customers')
            .select(`
                id, full_name, email, merchant_id, created_at,
                merchants(business_name, industry)
            `)
            .order('created_at', { ascending: false })
            .limit(1000); 

        if (error) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;
            return;
        }
        
        // Formatear la data para que sea más plana y fácil de filtrar
        globalDBCache = (data || []).map(c => {
            const m = c.merchants || {};
            return {
                id: c.id,
                full_name: c.full_name,
                email: c.email,
                merchant_id: c.merchant_id,
                created_at: c.created_at,
                business_name: m.business_name || 'Desconocido',
                country: m.country || '',
                state: m.state || '',
                industry: m.industry || 'other'
            };
        });
        
        filterGlobalDB(); // Llama el render inicial respetando filtros (si los hubiera en el DOM cacheado)
    };"""

new_load = """    window.loadGlobalDatabase = async function() {
        if (!checkMasterAdmin()) return;
        const tbody = document.getElementById('global-db-body');
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Cargando base de datos global...</td></tr>';
        
        // Obtener clientes junto con los datos geográficos de su restaurante
        const { data, error } = await window.supabaseClient
            .from('customers')
            .select(`
                id, full_name, email, merchant_id, created_at,
                merchants(*)
            `)
            .order('created_at', { ascending: false })
            .limit(1500); 

        if (error) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:#ef4444;">Error: ${error.message}</td></tr>`;
            return;
        }
        
        // Privacidad: Enmascarar email y aplanar datos
        globalDBCache = (data || []).map(c => {
            const m = c.merchants || {};
            
            // Mask Email (e.g. j***@gmail.com)
            let maskedEmail = 'N/D';
            if (c.email && c.email.includes('@')) {
                const parts = c.email.split('@');
                maskedEmail = parts[0].charAt(0) + '****@' + parts[1];
            }

            return {
                id: c.id,
                full_name: c.full_name || 'Anónimo',
                email: maskedEmail,
                raw_email: c.email || '', 
                merchant_id: c.merchant_id,
                created_at: c.created_at,
                business_name: m.business_name || 'Desconocido',
                country: m.country || '',
                state: m.state || '',
                colonia: m.colonia || m.neighborhood || '',
                industry: m.industry || 'other'
            };
        });
        
        filterGlobalDB();
    };"""

js = js.replace(old_load, new_load)

# Replace renderGlobalDB
old_render = """    window.renderGlobalDB = function(data) {
        const tbody = document.getElementById('global-db-body');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-muted);">No se encontraron registros.</td></tr>';
            return;
        }
        
        tbody.innerHTML = '';
        
        data.forEach(c => {
            const date = new Date(c.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' });
            
            // Format labels for location/industry
            let locationLabel = c.country ? `${c.country}` : '';
            if(c.state) locationLabel += locationLabel ? `, ${c.state}` : c.state;
            if(!locationLabel) locationLabel = 'N/D';
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft);">
                    <td style="padding: 16px; font-family: monospace; font-size: 12px; color: var(--text-muted);">${c.id.substring(0,8)}...</td>
                    <td style="padding: 16px; font-weight: 500;">${c.full_name}</td>
                    <td style="padding: 16px;">${c.email}</td>
                    <td style="padding: 16px;">${c.merchant_id.substring(0,8)}... <span style="font-size:11px;color:#8b5cf6;">(${c.business_name})</span></td>
                    <td style="padding: 16px;">${date}</td>
                </tr>
            `;
        });
    };"""

new_render = """    window.renderGlobalDB = function(data) {
        const tbody = document.getElementById('global-db-body');
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-muted);">No se encontraron registros.</td></tr>';
            return;
        }
        
        tbody.innerHTML = '';
        
        data.forEach(c => {
            const date = new Date(c.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' });
            
            // Format labels for location (Country, State, Colonia)
            let locationLabel = c.country ? `${c.country}` : '';
            if (c.state) locationLabel += locationLabel ? `, ${c.state}` : c.state;
            if (c.colonia) locationLabel += `, Col. ${c.colonia}`;
            if (!locationLabel) locationLabel = '<span style="color:#9ca3af;font-style:italic;">No especificada</span>';
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid var(--border-soft); transition: background 0.2s;" onmouseover="this.style.background='#F9FAFB'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 16px; font-family: monospace; font-size: 12px; color: var(--text-muted);">${c.id.substring(0,8)}...</td>
                    <td style="padding: 16px; font-weight: 500;">${c.full_name}</td>
                    <td style="padding: 16px; font-family: monospace; font-size: 13px; color: var(--text-muted);">${c.email}</td>
                    <td style="padding: 16px; font-weight: 600; color: #111827;">${c.business_name}</td>
                    <td style="padding: 16px; font-size: 13px; color: var(--text-muted);">${locationLabel}</td>
                    <td style="padding: 16px; font-variant-numeric: tabular-nums;">${date}</td>
                </tr>
            `;
        });
    };"""

js = js.replace(old_render, new_render)

# Replace filterGlobalDB
old_filter = """    window.filterGlobalDB = function() {
        const searchInput = document.getElementById('global-db-search')?.value.toLowerCase() || '';
        const filterCountry = document.getElementById('global-db-filter-country')?.value || '';
        const filterState = document.getElementById('global-db-filter-state')?.value.toLowerCase() || '';
        const filterIndustry = document.getElementById('global-db-filter-industry')?.value || '';
        const filterBusiness = document.getElementById('global-db-filter-business')?.value.toLowerCase() || '';

        const filtered = globalDBCache.filter(c => {
            let match = true;
            // Name or email search
            if (searchInput && !c.full_name.toLowerCase().includes(searchInput) && !c.email.toLowerCase().includes(searchInput)) match = false;
            // Country
            if (filterCountry && c.country !== filterCountry) match = false;
            // State
            if (filterState && !c.state.toLowerCase().includes(filterState)) match = false;
            // Industry
            if (filterIndustry && c.industry !== filterIndustry) match = false;
            // Business Name
            if (filterBusiness && !c.business_name.toLowerCase().includes(filterBusiness)) match = false;
            
            return match;
        });
        
        renderGlobalDB(filtered);
    };"""

new_filter = """    window.filterGlobalDB = function() {
        const searchInput = document.getElementById('global-db-search')?.value.toLowerCase() || '';
        const filterBusiness = document.getElementById('global-db-filter-business')?.value.toLowerCase() || '';
        const filterCountry = document.getElementById('global-db-filter-country')?.value.toLowerCase() || '';
        const filterState = document.getElementById('global-db-filter-state')?.value.toLowerCase() || '';
        const filterColonia = document.getElementById('global-db-filter-colonia')?.value.toLowerCase() || '';

        const filtered = globalDBCache.filter(c => {
            let match = true;
            // Name or hash search
            if (searchInput && !c.full_name.toLowerCase().includes(searchInput) && !c.id.toLowerCase().includes(searchInput)) match = false;
            
            // Geography & Business filters
            if (filterBusiness && !c.business_name.toLowerCase().includes(filterBusiness)) match = false;
            if (filterCountry && !c.country.toLowerCase().includes(filterCountry)) match = false;
            if (filterState && !c.state.toLowerCase().includes(filterState)) match = false;
            if (filterColonia && !c.colonia.toLowerCase().includes(filterColonia)) match = false;
            
            return match;
        });
        
        renderGlobalDB(filtered);
    };"""

js = js.replace(old_filter, new_filter)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Dashboard JS logic updated for Global DB.")
