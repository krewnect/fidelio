with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """                    <div style="display:flex; align-items:center; gap:12px; font-size:13px; padding: 8px 0; border-bottom: 1px solid var(--border-soft);">
                        <div style="width:32px; height:32px; border-radius:50%; background:${iconBg}; color:${iconColor}; display:flex; align-items:center; justify-content:center; font-size:12px; flex-shrink: 0;">${icon}</div>
                        <div style="flex:1;">${desc}</div>
                        <div style="font-size:11px; color:var(--text-muted); white-space:nowrap;">${timeStr}</div>
                    </div>`;
                });
            }
        }"""

replacement = """                    <div style="display:flex; align-items:center; gap:12px; font-size:13px; padding: 8px 0; border-bottom: 1px solid var(--border-soft);">
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
                12: [0,0,0,0,0,0,0], // 12 PM
                14: [0,0,0,0,0,0,0], // 2 PM
                18: [0,0,0,0,0,0,0], // 6 PM
                20: [0,0,0,0,0,0,0]  // 8 PM
            };
            
            let maxVal = 0;
            state.transactions.forEach(tx => {
                const d = new Date(tx.created_at);
                let day = d.getDay() - 1; // 0=Mon, 6=Sun
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
                const medals = ['#F59E0B', '#9CA3AF', '#D97706']; // Gold, Silver, Bronze
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
        }"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

