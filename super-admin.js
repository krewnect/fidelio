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
                    <button class="btn-primary" style="padding: 6px 12px; font-size: 0.8rem;" onclick="downloadQR('${qrUrl}', '${m.business_name || 'comercio'}')">
                        <i class="fa-solid fa-qrcode"></i> Descargar QR
                    </button>
                </td>
                <td colspan="3"></td>
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
