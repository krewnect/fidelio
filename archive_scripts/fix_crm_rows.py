import re
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        filtered.forEach(c => {
            const tr = document.createElement('tr');
            const comp = c.computed;
            const tierClass = comp.tier.includes('Oro') ? 'oro' : comp.tier.includes('Plata') ? 'plata' : 'bronce';
            const bdayAlert = comp.isBirthdayMonth ? `<i class="fa-solid fa-cake-candles" style="color:var(--accent-violet); margin-right:4px;" title="¡Cumpleaños este mes!"></i>` : `<i class="fa-solid fa-cake-candles" style="color:var(--text-muted); margin-right:4px;"></i>`;

            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${(c.full_name || c.name || '?').charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${c.full_name || c.name || 'Cliente sin nombre'}</strong>
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
                    <div style="display:flex; gap: 4px; justify-content: flex-end;">
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:#25D366; border-color:rgba(37, 211, 102, 0.2);" title="Enviar WhatsApp" onclick="alert('Abriendo WhatsApp Web para ${c.phone || 'cliente'}')">
                            <i class="fa-brands fa-whatsapp"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px;" title="Enviar Correo Electrónico" onclick="alert('Abriendo editor de correo para ${c.email || 'cliente'}')">
                            <i class="fa-regular fa-envelope"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:var(--accent-violet); border-color:rgba(139, 92, 246, 0.2);" title="Enviar Push a Apple/Google Wallet" onclick="alert('Redactando Notificación Push para ${(c.full_name || c.name || 'Cliente').replace(/'/g, "\\'")}')">
                            <i class="fa-regular fa-bell"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; margin-left:4px;" title="Escanear QR" onclick="window.showCustomerQR('${c.id}', '${(c.full_name || c.name || 'Cliente').replace(/'/g, "\\'")}')">
                            <i class="fa-solid fa-qrcode"></i>
                        </button>
                    </div>
                </td>
            `;
            crmTableBody.appendChild(tr);
        });"""

replacement = """        filtered.forEach(c => {
            const tr = document.createElement('tr');
            const comp = c.computed;
            const tierClass = comp.tier.includes('Oro') ? 'oro' : comp.tier.includes('Plata') ? 'plata' : 'bronce';
            const bdayAlert = comp.isBirthdayMonth ? `<i class="fa-solid fa-cake-candles" style="color:var(--accent-violet); margin-right:4px;" title="¡Cumpleaños este mes!"></i>` : ``;
            
            // Determine active campaign logic to show appropriate stamps text
            let isStamps = false;
            let stampsGoal = 5;
            if (state.campaigns && state.campaigns.length > 0) {
                isStamps = state.campaigns[0].type === 'stamps';
                if (isStamps) stampsGoal = state.campaigns[0].stamps_goal || 5;
            }

            const phoneDigits = c.phone ? c.phone.replace(/\\D/g, '') : '';
            const waAction = phoneDigits ? `window.open('https://wa.me/${phoneDigits}', '_blank')` : `alert('El cliente no tiene un teléfono registrado.')`;
            const emailAction = c.email ? `window.open('mailto:${c.email}', '_self')` : `alert('El cliente no tiene un correo registrado.')`;
            
            const avgSpend = c.visits && c.visits > 0 ? (comp.spent / c.visits) : 0;

            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:34px; height:34px; border-radius:50%; background:var(--fidelio-violet); color:white; display:flex; align-items:center; justify-content:center; font-weight:800;">${(c.full_name || c.name || '?').charAt(0).toUpperCase()}</div>
                        <div>
                            <strong>${c.full_name || c.name || 'Cliente sin nombre'}</strong>
                            <small style="display:block; color:var(--text-muted);">${c.id.substring(0,8)}...</small>
                        </div>
                    </div>
                </td>
                <td>
                    <strong>${c.phone || 'N/A'}</strong>
                    <small style="display:block; color:var(--text-muted);">${c.email || 'Sin correo'}</small>
                </td>
                <td><span class="tier-pill ${tierClass}">${comp.tier}</span></td>
                <td>
                    <strong style="color:#10b981; font-size:14px;">$${comp.balance.toFixed(2)} MXN</strong>
                    <small style="display:block; color:var(--text-muted);">Saldo actual</small>
                </td>
                <td>
                    <strong><i class="fa-solid fa-stamp" style="color:var(--accent-violet);"></i> ${c.visits || 0}/${stampsGoal}</strong>
                    <small style="display:block; color:var(--text-muted);">Visitas registradas</small>
                </td>
                <td>
                    <strong>${comp.lastVisitFormatted}</strong>
                    <small style="display:block; color:var(--text-muted);">${bdayAlert} Cumpleaños: ${comp.bdayFormatted}</small>
                </td>
                <td>
                    <strong style="color:var(--fidelio-violet);">${comp.freqText}</strong>
                    <small style="display:block; color:var(--text-muted);"><span class="badge-status ${comp.statusClass}" style="padding:2px 6px; font-size:9px;">${comp.statusText}</span></small>
                </td>
                <td><strong>$${comp.spent.toFixed(2)} MXN</strong></td>
                <td><strong>$${avgSpend.toFixed(2)} MXN</strong></td>
                <td>
                    <div style="display:flex; gap: 4px; justify-content: flex-end;">
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:#25D366; border-color:rgba(37, 211, 102, 0.2);" title="Enviar WhatsApp" onclick="${waAction}">
                            <i class="fa-brands fa-whatsapp"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:#3b82f6; border-color:rgba(59, 130, 246, 0.2);" title="Enviar Correo Electrónico" onclick="${emailAction}">
                            <i class="fa-regular fa-envelope"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; color:var(--accent-violet); border-color:rgba(139, 92, 246, 0.2);" title="Enviar Notificación Push a Wallet" onclick="if(typeof Swal !== 'undefined'){Swal.fire('Notificaciones Push','El envío de notificaciones directas al Apple Wallet/Google Wallet se habilitará cuando contrates un Add-on o subas de plan.','info');}else{alert('El envío de notificaciones directas requiere un add-on adicional.');}">
                            <i class="fa-regular fa-bell"></i>
                        </button>
                        <button class="btn btn-outline" style="padding:6px 10px; font-size:12px; margin-left:4px;" title="Ver Perfil Detallado" onclick="if(typeof Swal !== 'undefined'){Swal.fire('Perfil del Cliente','Detalles extendidos del cliente muy pronto.','info');}else{alert('Detalles del perfil pronto.');}">
                            <i class="fa-solid fa-qrcode"></i>
                        </button>
                    </div>
                </td>
            `;
            crmTableBody.appendChild(tr);
        });"""

js = js.replace(target, replacement)
with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js)
