import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update loadMerchantsControl() to use openAdminMerchant instead of inline buttons
old_row = """                    paymentStatus = '<span style="color:#ef4444;font-weight:700;">Pago Requerido</span>';
                    morososHTML += `
                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border-soft); padding:12px 0;">
                            <div>
                                <strong style="display:block;">${m.business_name}</strong>
                                <span style="font-size:12px; color:var(--text-muted);">Trial expirado hace ${Math.abs(14 - daysSinceCreated)} días</span>
                            </div>
                            <button class="fidelio-btn-secondary-preset" onclick="contactMerchant('${m.id}')"><i class="fa-solid fa-envelope"></i> Aviso</button>
                        </div>
                    `;
                } else {
                    paymentStatus = '<span style="color:#f59e0b;">Trial Activo</span>';
                }
            } else if (m.plan_status === 'expired') {
                paymentStatus = '<span style="color:#ef4444;font-weight:700;">Expirado</span>';
            } else if (m.plan_status === 'lifetime_free') {
                daysLeft = '∞';
                paymentStatus = '<span style="color:#8b5cf6;font-weight:700;">Lifetime Free</span>';
            } else if (m.plan_status === 'active') {
                paymentStatus = '<span style="color:#10b981;font-weight:700;">Pagado</span>';
            }
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid #F3F4F6; transition: background 0.2s;" onmouseover="this.style.background='#F9FAFB'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 16px; font-weight: 600; color: #111827;">${m.business_name}</td>
                    <td style="padding: 16px;">${planBadge}</td>
                    <td style="padding: 16px; font-variant-numeric: tabular-nums;">${daysLeft}</td>
                    <td style="padding: 16px;">${paymentStatus}</td>
                    <td style="padding: 16px; text-align: right;">
                        <button class="fidelio-btn-secondary-preset" onclick="grantFreeAccount('${m.id}')" style="background:rgba(139,92,246,0.1); color:var(--accent-violet); padding:6px 12px; font-size:12px;"><i class="fa-solid fa-gift"></i></button>
                        <button class="fidelio-btn-secondary-preset" onclick="forcePaidStatus('${m.id}', 'active')" style="padding:6px 12px; font-size:12px;"><i class="fa-solid fa-check"></i> Activar</button>
                    </td>
                </tr>
            `;"""

new_row = """                    paymentStatus = '<span style="color:#ef4444;font-weight:700;">Pago Requerido</span>';
                    morososHTML += `
                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border-soft); padding:12px 0;">
                            <div>
                                <strong style="display:block;">${m.business_name}</strong>
                                <span style="font-size:12px; color:var(--text-muted);">Trial expirado hace ${Math.abs(14 - daysSinceCreated)} días</span>
                            </div>
                            <button class="fidelio-btn-secondary-preset" onclick="openAdminMerchant('${m.id}')"><i class="fa-solid fa-gear"></i> Administrar</button>
                        </div>
                    `;
                } else {
                    paymentStatus = '<span style="color:#f59e0b;">Trial Activo</span>';
                }
            } else if (m.plan_status === 'expired') {
                paymentStatus = '<span style="color:#ef4444;font-weight:700;">Expirado</span>';
            } else if (m.plan_status === 'lifetime_free') {
                daysLeft = '∞';
                paymentStatus = '<span style="color:#8b5cf6;font-weight:700;">Lifetime Free</span>';
            } else if (m.plan_status === 'active') {
                paymentStatus = '<span style="color:#10b981;font-weight:700;">Pagado</span>';
            }
            
            tbody.innerHTML += `
                <tr style="border-bottom: 1px solid #F3F4F6; transition: background 0.2s;" onmouseover="this.style.background='#F9FAFB'" onmouseout="this.style.background='transparent'">
                    <td style="padding: 16px; font-weight: 600; color: #111827;">${m.business_name}</td>
                    <td style="padding: 16px;">${planBadge}</td>
                    <td style="padding: 16px; font-variant-numeric: tabular-nums;">${daysLeft}</td>
                    <td style="padding: 16px;">${paymentStatus}</td>
                    <td style="padding: 16px; text-align: right;">
                        <button class="fidelio-btn-secondary-preset" onclick="openAdminMerchant('${m.id}')" style="background:var(--bg-main); color:var(--text-main); padding:6px 12px; font-size:12px; border:1px solid var(--border-soft);"><i class="fa-solid fa-sliders"></i> Administrar</button>
                    </td>
                </tr>
            `;"""

if old_row in js:
    js = js.replace(old_row, new_row)
else:
    print("WARNING: Could not find old_row in loadMerchantsControl")

# 2. Inject the new modal logic
new_functions = """
    // --- ADVANCED MERCHANT CONTROL MODAL ---
    window.openAdminMerchant = async function(merchantId) {
        if (!checkMasterAdmin()) return;
        
        document.getElementById('admin-current-merchant-id').value = merchantId;
        document.getElementById('admin-merchant-name').textContent = "Cargando...";
        document.getElementById('admin-merchant-status').textContent = "...";
        document.getElementById('admin-merchant-passes').textContent = "...";
        document.getElementById('admin-merchant-scans').textContent = "...";
        document.getElementById('admin-merchant-crm').textContent = "...";
        document.getElementById('admin-custom-price').value = "";
        
        openModal('modal-admin-merchant');

        try {
            // 1. Fetch Merchant Details
            const { data: m, error: mErr } = await window.supabaseClient.from('merchants').select('business_name, plan_status, created_at, custom_price').eq('id', merchantId).single();
            if (mErr) throw mErr;
            
            document.getElementById('admin-merchant-name').textContent = m.business_name;
            document.getElementById('admin-merchant-id').textContent = merchantId;
            document.getElementById('admin-merchant-created').textContent = new Date(m.created_at).toLocaleDateString();
            document.getElementById('admin-merchant-status').textContent = m.plan_status.toUpperCase();
            document.getElementById('admin-custom-price').value = m.custom_price || "";
            
            // 2. Fetch Passes Count
            const { count: pCount, error: pErr } = await window.supabaseClient.from('wallet_passes').select('*', { count: 'exact', head: true }).eq('merchant_id', merchantId);
            document.getElementById('admin-merchant-passes').textContent = pErr ? "Error" : (pCount || 0);

            // 3. Fetch Scans Count
            const { count: sCount, error: sErr } = await window.supabaseClient.from('scans').select('*', { count: 'exact', head: true }).eq('merchant_id', merchantId);
            document.getElementById('admin-merchant-scans').textContent = sErr ? "Error" : (sCount || 0);

            // 4. Fetch CRM Count
            const { count: cCount, error: cErr } = await window.supabaseClient.from('customers').select('*', { count: 'exact', head: true }).eq('merchant_id', merchantId);
            document.getElementById('admin-merchant-crm').textContent = cErr ? "Error" : (cCount || 0);

        } catch (e) {
            console.error("Error loading merchant details:", e);
            window.showToast("Error al cargar detalles del negocio", "error");
        }
    };

    window.saveAdminCustomPrice = async function() {
        if (!checkMasterAdmin()) return;
        const id = document.getElementById('admin-current-merchant-id').value;
        const priceVal = document.getElementById('admin-custom-price').value;
        const customPrice = priceVal ? parseFloat(priceVal) : null;
        
        const { error } = await window.supabaseClient.from('merchants').update({ custom_price: customPrice }).eq('id', id);
        if (error) {
            window.showToast("Error al guardar precio", "error");
        } else {
            window.showToast("Precio personalizado actualizado", "success");
        }
    };

    window.setAdminPlanStatus = async function(status) {
        if (!checkMasterAdmin()) return;
        const id = document.getElementById('admin-current-merchant-id').value;
        if(!confirm(`¿Estás seguro de cambiar el estatus a ${status}?`)) return;
        
        const { error } = await window.supabaseClient.from('merchants').update({ plan_status: status }).eq('id', id);
        if (error) {
            window.showToast("Error al actualizar estatus", "error");
        } else {
            window.showToast("Estatus actualizado exitosamente", "success");
            document.getElementById('admin-merchant-status').textContent = status.toUpperCase();
            loadMerchantsControl();
        }
    };

    window.addAdminTrialDays = async function(daysToAdd) {
        if (!checkMasterAdmin()) return;
        const id = document.getElementById('admin-current-merchant-id').value;
        if(!confirm(`¿Estás seguro de regalar ${daysToAdd} días más de prueba?`)) return;
        
        try {
            // Get current created_at
            const { data, error } = await window.supabaseClient.from('merchants').select('created_at').eq('id', id).single();
            if (error) throw error;
            
            // Add X days to the future of the base calculation
            const currentCreated = new Date(data.created_at);
            currentCreated.setDate(currentCreated.getDate() + daysToAdd);
            
            const { error: uErr } = await window.supabaseClient.from('merchants').update({ created_at: currentCreated.toISOString(), plan_status: 'trial' }).eq('id', id);
            if (uErr) throw uErr;
            
            window.showToast("Días de prueba extendidos exitosamente", "success");
            document.getElementById('admin-merchant-status').textContent = 'TRIAL';
            loadMerchantsControl();
        } catch (e) {
            window.showToast("Error al extender periodo de prueba", "error");
            console.error(e);
        }
    };

"""

# Insert new functions before window.forcePaidStatus
anchor = "    window.forcePaidStatus = async function(id, newStatus) {"
if anchor in js:
    js = js.replace(anchor, new_functions + anchor)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("JS logic injected.")
else:
    print("WARNING: Could not find anchor in dashboard_v2.js")

