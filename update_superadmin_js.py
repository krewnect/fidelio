import re

filepath = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/super-admin.js'

with open(filepath, 'r') as f:
    content = f.read()

replacement = """
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
"""

pattern = re.compile(r'async function fetchMerchants\(\) \{.*?\n    \}', re.DOTALL)
new_content = pattern.sub(replacement.strip(), content)

with open(filepath, 'w') as f:
    f.write(new_content)
