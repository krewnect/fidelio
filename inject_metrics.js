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
            const earnCount = state.transactions.filter(t => t.type === 'earn').length;
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
        
        // Retorno de Inversión (ROI) Matemático
        const mRoi = document.getElementById('metric-roi');
        const mRoiRatio = document.getElementById('metric-roi-ratio');
        if(mRoi && mRoiRatio) {
            // Asumimos un costo base del software
            const fidelioCost = window.merchantData.tier === 'business' ? 2499 : 999;
            
            if (totalSales === 0) {
                mRoi.textContent = '0%';
                mRoiRatio.textContent = '0.00';
            } else {
                const roiPercent = Math.round(((totalSales - fidelioCost) / fidelioCost) * 100);
                mRoi.textContent = (roiPercent > 0 ? '+' : '') + roiPercent + '%';
                
                const ratio = (totalSales / fidelioCost).toFixed(2);
                mRoiRatio.textContent = ratio;
            }
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

        // HEATMAP
        const heatmapGrid = document.getElementById('heatmap-grid');
        if(heatmapGrid) {
            const matrix = {
                12: [0,0,0,0,0,0,0], 14: [0,0,0,0,0,0,0], 18: [0,0,0,0,0,0,0], 20: [0,0,0,0,0,0,0]
            };
            
            let maxVal = 0;
            state.transactions.forEach(tx => {
                const d = new Date(tx.created_at);
                let day = d.getDay() - 1; // 0=Mon
                if(day === -1) day = 6;
                const h = d.getHours();
                
                let bucket = 12;
                if(h >= 13 && h < 17) bucket = 14;
                else if(h >= 17 && h < 20) bucket = 18;
                else if(h >= 20) bucket = 20;
                
                matrix[bucket][day]++;
                if(matrix[bucket][day] > maxVal) maxVal = matrix[bucket][day];
            });
            
            let hmHtml = `<div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; text-align:center; font-size:11px; font-weight:700; color:var(--text-muted); margin-bottom:8px;">
                <div></div><div>Lun</div><div>Mar</div><div>Mié</div><div>Jue</div><div>Vie</div><div>Sáb</div><div>Dom</div>
            </div>`;
            
            const labels = {12: '12 PM', 14: '2 PM', 18: '6 PM', 20: '8 PM'};
            [12, 14, 18, 20].forEach(bucket => {
                hmHtml += `<div style="display:grid; grid-template-columns: 50px repeat(7, 1fr); gap:4px; height:24px; margin-bottom:4px;">
                    <div style="font-size:10px; color:var(--text-muted); display:flex; align-items:center; justify-content:flex-end; padding-right:8px;">${labels[bucket]}</div>`;
                for(let i=0; i<7; i++) {
                    const val = matrix[bucket][i];
                    const opacity = maxVal > 0 ? (val / maxVal) : 0;
                    hmHtml += `<div class="heatmap-cell" style="background: rgba(76,29,149,${Math.max(0.05, opacity)});" title="${val} visitas"></div>`;
                }
                hmHtml += `</div>`;
            });
            heatmapGrid.innerHTML = hmHtml;
        }

        // LEADERBOARD
        const lbContainer = document.getElementById('leaderboard-container');
        if(lbContainer) {
            const customerSpend = {};
            state.transactions.filter(t => t.type === 'earn').forEach(t => {
                if(!customerSpend[t.customer_id]) customerSpend[t.customer_id] = {id: t.customer_id, spend: 0, visits: 0};
                customerSpend[t.customer_id].spend += (t.amount || 0);
                customerSpend[t.customer_id].visits++;
            });
            
            const sorted = Object.values(customerSpend).sort((a,b) => b.spend - a.spend).slice(0,3);
            if(sorted.length === 0) {
                lbContainer.innerHTML = '<div style="text-align:center; padding:20px 0;">No hay clientes suficientes.</div>';
            } else {
                lbContainer.innerHTML = '';
                const medals = ['#F59E0B', '#9CA3AF', '#D97706'];
                sorted.forEach((cus, idx) => {
                    const cInfo = state.customers.find(c => c.id === cus.id);
                    const name = cInfo ? `${cInfo.first_name || ''} ${cInfo.last_name || ''}`.trim() : 'Cliente Anónimo';
                    lbContainer.innerHTML += `
                    <div style="display:flex; align-items:center; justify-content:space-between; padding:12px; background:var(--bg-input); border-radius:12px; margin-bottom:8px;">
                        <div style="display:flex; align-items:center; gap:12px;">
                            <div style="width:28px; height:28px; border-radius:50%; background:rgba(245,158,11,0.1); color:${medals[idx] || '#10b981'}; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:800;">
                                ${idx+1}
                            </div>
                            <div style="font-weight:700; color:var(--text-main); font-size:14px;">${name}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-weight:800; color:var(--accent-violet);">$${cus.spend.toLocaleString('es-MX', {minimumFractionDigits:2})}</div>
                            <div style="font-size:10px; color:var(--text-muted);">${cus.visits} visitas</div>
                        </div>
                    </div>`;
                });
            }
        }
