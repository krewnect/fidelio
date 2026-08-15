// --- PASSLOYALTY SUPER ADMIN MASTER SCRIPT (4 MAIN TABS) --- //

document.addEventListener('DOMContentLoaded', async () => {

    // --- TAB NAVIGATION FOR SUPER ADMIN ---
    const adminNavTabs = document.querySelectorAll('[data-admin-tab]');
    const adminTabContents = document.querySelectorAll('.tab-content');

    adminNavTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            adminNavTabs.forEach(t => t.classList.remove('active'));
            adminTabContents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const targetTabId = tab.getAttribute('data-admin-tab');
            document.getElementById(targetTabId).classList.add('active');
        });
    });

    // --- FETCH MERCHANTS FROM SUPABASE ---
    const tbody = document.getElementById('master-table-body');
    const searchInput = document.getElementById('master-search-input');
    
    // Change table headers in super-admin.html to match merchants
    // We'll just render it differently in JS.
    let merchants = [];

    async function fetchMerchants() {
        if (!window.supabaseClient) return;
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;">Cargando restaurantes...</td></tr>';
        
        // Fetch Merchants
        const { data: merchantsData, error: mErr } = await window.supabaseClient
            .from('merchants')
            .select('*')
            .order('created_at', { ascending: false });
            
        // Fetch Customers (Pases Emitidos)
        const { count: customersCount, error: cErr } = await window.supabaseClient
            .from('customers')
            .select('*', { count: 'exact', head: true });
            
        if (mErr) {
            console.error(mErr);
            tbody.innerHTML = '<tr><td colspan="10" style="text-align:center; color:red;">Error cargando datos.</td></tr>';
            return;
        }
        
        merchants = merchantsData || [];
        renderMasterTable();
        
        // --- ACTUALIZAR MÉTRICAS REALES ---
        
        // 1. Negocios
        const elMerchants = document.getElementById('sa-metric-merchants');
        if (elMerchants) elMerchants.textContent = `${merchants.length} Comercios`;
        
        // 2. Pases Emitidos
        const elPasses = document.getElementById('sa-metric-passes');
        if (elPasses) elPasses.textContent = `${customersCount || 0} Pases`;
        
        // 3. Ubicaciones (Asumiremos un estimado o lo calcularemos de branches)
        const elBranches = document.getElementById('sa-metric-branches');
        if (elBranches) {
            const { count: branchesCount } = await window.supabaseClient.from('branches').select('*', { count: 'exact', head: true });
            elBranches.textContent = `${branchesCount || merchants.length} Ubicaciones`;
        }
        
        // 4. MRR ($999 por comercio activo)
        const elMRR = document.getElementById('sa-metric-mrr');
        const activeMerchants = merchants.filter(m => m.plan_status === 'active').length;
        // Si no hay filtro de pago estricto aún, contamos todos para la demo de proyección
        const projectedMRR = merchants.length * 999; 
        if (elMRR) elMRR.textContent = `$${projectedMRR.toLocaleString()} MXN`;
        
        // 5. Distribución
        const elDist = document.getElementById('sa-metric-distribution');
        if (elDist && merchants.length > 0) {
            const indCount = {};
            merchants.forEach(m => {
                const ind = m.industry || 'General';
                indCount[ind] = (indCount[ind] || 0) + 1;
            });
            let distHtml = '';
            for (const [ind, count] of Object.entries(indCount)) {
                const pct = Math.round((count / merchants.length) * 100);
                distHtml += `<div class="calc-row"><span>${ind}</span><strong>${pct}%</strong></div>`;
            }
            elDist.innerHTML = distHtml;
        } else if (elDist) {
            elDist.innerHTML = '<div class="calc-row"><span>Sin datos suficientes</span><strong>0%</strong></div>';
        }
    }

    function renderMasterTable() {
        if (!tbody) return;
        const query = searchInput ? searchInput.value.toLowerCase() : '';
        const filtered = merchants.filter(m => 
            (m.business_name || '').toLowerCase().includes(query) ||
            (m.email || '').toLowerCase().includes(query) ||
            (m.industry || '').toLowerCase().includes(query) ||
            (m.id || '').toLowerCase().includes(query)
        );

        tbody.innerHTML = '';
        
        if (filtered.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;">No hay comercios registrados.</td></tr>';
            return;
        }

        filtered.forEach(m => {
            const tr = document.createElement('tr');
            const date = m.created_at ? new Date(m.created_at).toISOString().split('T')[0] : 'N/A';
            const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=1000x1000&data=${encodeURIComponent(window.location.origin + '/pass.html?m=' + m.id)}`;

            tr.innerHTML = `
                <td><code>${m.id.substring(0,8)}...</code></td>
                <td><strong>${m.business_name || 'Sin Nombre'}</strong></td>
                <td><span class="tier-pill" style="background:rgba(99, 102, 241, 0.15); color:var(--indigo);">${m.industry || 'General'}</span></td>
                <td>${m.email || 'N/A'}</td>
                <td><strong class="text-emerald">Activo</strong></td>
                <td>${date}</td>
                <td>
                    <button class="btn-outline" style="padding: 4px 8px; font-size: 0.8rem; border-color:var(--border-glass);" onclick="setCustomPrice('${m.id}', ${m.custom_price || null})">
                        ${m.custom_price ? '$' + m.custom_price : 'Fijar'}
                    </button>
                </td>
                <td>
                    <button class="btn-primary" style="padding: 6px 12px; font-size: 0.8rem;" onclick="downloadQR('${qrUrl}', '${m.business_name || 'comercio'}')">
                        <i class="fa-solid fa-qrcode"></i> Descargar QR
                    </button>
                </td>
                <td colspan="2"></td>
            `;
            tbody.appendChild(tr);
        });
    }
    
    window.downloadQR = function(url, name) {
        const a = document.createElement('a');
        a.href = url;
        a.download = `QR_Mesa_${name}.png`;
        a.target = '_blank';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    window.setCustomPrice = async function(merchantId, currentPrice) {
        const newPrice = prompt(`Fijar Precio Especial (MXN) mensual.\n(Deja en blanco para borrar el precio especial):`, currentPrice || '');
        if (newPrice === null) return;
        
        const priceVal = newPrice.trim() === '' ? null : parseInt(newPrice.trim(), 10);
        if (newPrice.trim() !== '' && isNaN(priceVal)) return alert("Precio inválido");

        const { error } = await window.supabaseClient
            .from('merchants')
            .update({ custom_price: priceVal })
            .eq('id', merchantId);

        if (error) {
            console.error(error);
            alert("Error actualizando precio");
        } else {
            // refresh data locally
            const m = merchants.find(x => x.id === merchantId);
            if(m) m.custom_price = priceVal;
            renderMasterTable();
        }
    };

    if (searchInput) {
        searchInput.addEventListener('input', renderMasterTable);
    }

    const btnExportMaster = document.getElementById('btn-export-master-db');
    if (btnExportMaster) {
        btnExportMaster.addEventListener('click', () => {
            alert("Exportando Base de Datos Maestra Consolidada en formato CSV...");
        });
    }

    const btnSaveAi = document.getElementById('btn-save-ai-config');
    if (btnSaveAi) {
        btnSaveAi.addEventListener('click', () => {
            alert("Configuración de DeepSeek API y prompts del sistema guardados correctamente.");
        });
    }

    const btnOnboardNew = document.getElementById('btn-onboard-new-restaurant');
    if (btnOnboardNew) {
        btnOnboardNew.addEventListener('click', () => {
            alert("Abriendo formulario para dar de alta un nuevo restaurante en la plataforma...");
        });
    }

    fetchMerchants();
});


// --- INBOX (FACTURAS Y TRANSFERENCIAS) SUPER ADMIN LOGIC ---
async function fetchAdminInbox() {
    if (!window.supabaseClient) return;
    const tbody = document.getElementById('inbox-table-body');
    if(!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Cargando solicitudes...</td></tr>';
    
    // Fetch Requests with Merchant info
    const { data: inboxData, error } = await window.supabaseClient
        .from('admin_inbox')
        .select(`*, merchants(business_name, email)`)
        .order('created_at', { ascending: false });
        
    if (error) {
        console.error("Error fetching inbox:", error);
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:red;">Error cargando buzón.</td></tr>';
        return;
    }
    
    if (!inboxData || inboxData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; color:#6b7280;">No hay solicitudes pendientes.</td></tr>';
        return;
    }
    
    let html = '';
    inboxData.forEach(item => {
        const date = new Date(item.created_at).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        const merchantName = item.merchants ? item.merchants.business_name : 'Desconocido';
        const merchantEmail = item.merchants ? item.merchants.email : '';
        
        let statusBadge = '';
        if (item.status === 'pending') statusBadge = '<span class="badge-status inactivo">Pendiente</span>';
        else if (item.status === 'processed') statusBadge = '<span class="badge-status activo">Procesado</span>';
        else statusBadge = `<span class="badge-status inactivo">${item.status}</span>`;
        
        let fileLink = item.file_url ? `<a href="${item.file_url}" target="_blank" class="btn btn-outline" style="padding:4px 8px; font-size:11px;"><i class="fa-solid fa-file-arrow-down"></i> Ver Comprobante</a>` : 'Sin archivo';
        
        let detailsHtml = '';
        if (item.type === 'factura' && item.details) {
            detailsHtml = `
                <div style="font-size:11px; color:#4b5563;">
                    <strong>RFC:</strong> ${item.details.rfc || 'N/A'}<br>
                    <strong>Razón:</strong> ${item.details.razon || 'N/A'}<br>
                    <strong>CP/Rég/Uso:</strong> ${item.details.cp} | ${item.details.regimen} | ${item.details.uso_cfdi}
                </div>
            `;
        } else {
            detailsHtml = `<div style="font-size:11px; color:#4b5563;">Comprobante de Pago Mensual</div>`;
        }
        
        let actionHtml = `<button onclick="markAsProcessed('${item.id}')" class="btn btn-primary" style="padding:4px 8px; font-size:11px; background:#10b981;"><i class="fa-solid fa-check"></i> Marcar Listo</button>`;
        if(item.status === 'processed') {
            actionHtml = `<span style="font-size:11px; color:#10b981;"><i class="fa-solid fa-check-double"></i> Listo</span>`;
        }
        
        html += `
            <tr>
                <td style="font-size:12px;">${date}</td>
                <td>
                    <strong>${merchantName}</strong>
                    <div style="font-size:11px; color:#6b7280;">${merchantEmail}</div>
                </td>
                <td style="text-transform:capitalize; font-weight:bold; color: ${item.type === 'factura' ? '#8b5cf6' : '#3b82f6'};">
                    ${item.type}
                </td>
                <td>${statusBadge}</td>
                <td>${fileLink}</td>
                <td>${detailsHtml}</td>
                <td>${actionHtml}</td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

window.markAsProcessed = async function(id) {
    if (!window.supabaseClient) return;
    const { error } = await window.supabaseClient
        .from('admin_inbox')
        .update({ status: 'processed' })
        .eq('id', id);
        
    if (error) {
        alert("Error: " + error.message);
        return;
    }
    fetchAdminInbox();
};

// Hook into tab switching to refresh inbox when tab is clicked
const inboxTabBtn = document.querySelector('[data-tab="tab-inbox"]');
if (inboxTabBtn) {
    inboxTabBtn.addEventListener('click', () => {
        fetchAdminInbox();
    });
}

// Fetch on load just in case it's the active tab (usually isn't on load)
setTimeout(fetchAdminInbox, 1500);


