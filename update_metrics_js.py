with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        // Citas Pendientes
        let processed = [];
        try { processed = window.merchantData.appointment_settings.processed_appointments || []; } catch(e){}
        const pendingCitas = state.transactions.filter(t => t.transaction_type === 'appointment_request' && !processed.includes(t.id)).length;
        const citasBadge = document.getElementById('citas-count-badge');
        if (citasBadge) {
            citasBadge.textContent = pendingCitas;
            citasBadge.style.display = pendingCitas > 0 ? 'inline-flex' : 'none';
        }"""

replacement = """        // Citas Pendientes
        let processed = [];
        try { processed = window.merchantData.appointment_settings.processed_appointments || []; } catch(e){}
        const pendingCitas = state.transactions.filter(t => t.transaction_type === 'appointment_request' && !processed.includes(t.id)).length;
        const citasBadge = document.getElementById('citas-count-badge');
        if (citasBadge) {
            citasBadge.textContent = pendingCitas;
            citasBadge.style.display = pendingCitas > 0 ? 'inline-flex' : 'none';
        }

        // --- ADVANCED METRICS TAB ---
        
        // Base Lealtad
        const mAdvLoyalty = document.getElementById('metric-adv-loyalty');
        if(mAdvLoyalty) mAdvLoyalty.textContent = totalCustomers.toLocaleString();
        
        // Ticket Promedio
        const mAdvTicket = document.getElementById('metric-adv-ticket');
        if(mAdvTicket) {
            const earnTx = state.transactions.filter(t => t.type === 'earn');
            const avgTicket = earnTx.length > 0 ? (totalSales / earnTx.length) : 0;
            mAdvTicket.textContent = `$${avgTicket.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        }
        
        // Tasa Redención
        const mAdvRedemp = document.getElementById('metric-adv-redemption');
        if(mAdvRedemp) {
            const burnCount = state.transactions.filter(t => t.type === 'burn').length;
            const totalTx = state.transactions.filter(t => t.type === 'earn' || t.type === 'burn').length;
            const redempRate = totalTx > 0 ? Math.round((burnCount / totalTx) * 100) : 0;
            mAdvRedemp.textContent = `${redempRate}%`;
        }
        
        // Frecuencia
        const mAdvFreq = document.getElementById('metric-adv-freq');
        if(mAdvFreq) {
            const earnCount = state.transactions.filter(t => t.type === 'earn').length;
            const freq = totalCustomers > 0 ? (earnCount / totalCustomers) : 0;
            mAdvFreq.innerHTML = `${freq.toFixed(1)}x<span style="font-size:16px; color:var(--text-muted); font-weight:500;">/mes</span>`;
        }
        
        // Loyalty Revenue (ROI panel)
        const mLoyaltyRev = document.getElementById('metric-loyalty-revenue');
        if(mLoyaltyRev) {
            mLoyaltyRev.innerHTML = `+$${totalSales.toLocaleString('es-MX', {minimumFractionDigits: 2, maximumFractionDigits: 2})} <span style="font-size:16px; font-weight:600; opacity:0.8; color:white;">MXN</span>`;
        }
        
        // LIVE ACTIVITY FEED
        const feedContainer = document.getElementById('live-activity-feed');
        if(feedContainer) {
            const recentTx = [...state.transactions].sort((a,b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 5);
            
            if(recentTx.length === 0) {
                feedContainer.innerHTML = '<div style="text-align: center; color: var(--text-muted); font-size: 13px; padding: 20px 0;">No hay actividad reciente.</div>';
            } else {
                feedContainer.innerHTML = '';
                recentTx.forEach(tx => {
                    const d = new Date(tx.created_at);
                    const isToday = d.toDateString() === new Date().toDateString();
                    const timeStr = isToday ? d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : d.toLocaleDateString();
                    
                    let icon = '<i class="fa-solid fa-qrcode"></i>';
                    let iconColor = 'var(--accent-violet)';
                    let iconBg = 'var(--bg-input)';
                    let desc = '';
                    
                    // Find customer
                    const c = state.customers.find(cus => cus.id === tx.customer_id);
                    const cName = c ? (c.first_name || 'Cliente') : 'Cliente';
                    
                    if(tx.type === 'earn') {
                        desc = `<strong>${cName}</strong> sumó puntos/cashback por compra de $${(tx.amount||0).toFixed(2)}`;
                    } else if(tx.type === 'burn') {
                        icon = '<i class="fa-solid fa-fire"></i>';
                        iconColor = '#F59E0B';
                        iconBg = 'rgba(245, 158, 11, 0.1)';
                        desc = `<strong>${cName}</strong> canjeó premio/saldo`;
                    } else if(tx.transaction_type === 'appointment_request') {
                        icon = '<i class="fa-regular fa-calendar"></i>';
                        iconColor = '#10b981';
                        iconBg = 'rgba(16, 185, 129, 0.1)';
                        desc = `<strong>${cName}</strong> solicitó una cita`;
                    } else {
                        desc = `<strong>${cName}</strong> registró actividad`;
                    }
                    
                    feedContainer.innerHTML += `
                    <div style="display:flex; align-items:center; gap:12px; font-size:13px; padding: 8px 0; border-bottom: 1px solid var(--border-soft);">
                        <div style="width:32px; height:32px; border-radius:50%; background:${iconBg}; color:${iconColor}; display:flex; align-items:center; justify-content:center; font-size:12px; flex-shrink: 0;">${icon}</div>
                        <div style="flex:1;">${desc}</div>
                        <div style="font-size:11px; color:var(--text-muted); white-space:nowrap;">${timeStr}</div>
                    </div>`;
                });
            }
        }
"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

