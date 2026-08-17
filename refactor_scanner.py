import re

with open('scanner.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add currentCampaignData variable
content = content.replace('let window.currentCustomerData = null;', 'let window.currentCustomerData = null;\nlet window.currentCampaignData = null;')

# 2. Update fetchCustomer to use both UUIDs
new_fetchCustomer = """
        async function fetchCustomer(customerId) {
            try {
                let query = supabaseClient.from('customers').select('*').eq('merchant_id', currentMerchantData.id);
                if (customerId.length === 36 && customerId.includes('-')) {
                    query = query.eq('id', customerId);
                } else if (customerId.includes('@')) {
                    query = query.eq('email', customerId.toLowerCase());
                } else {
                    query = query.eq('phone', customerId);
                }
                const { data, error } = await query.single();
                if (error || !data) return null;
                return data;
            } catch (err) {
                console.error(err);
                return null;
            }
        }
        
        async function fetchCustomerCampaign(customerId, campaignId) {
            try {
                const { data, error } = await supabaseClient.from('customer_campaigns')
                    .select('*')
                    .eq('customer_id', customerId)
                    .eq('campaign_id', campaignId)
                    .single();
                if (error) {
                    // Try to insert it if it doesn't exist
                    const { data: newLink, error: insErr } = await supabaseClient.from('customer_campaigns')
                        .insert([{ customer_id: customerId, campaign_id: campaignId }])
                        .select('*').single();
                    if (!insErr) return newLink;
                    return null;
                }
                return data;
            } catch(e) {
                console.error(e);
                return null;
            }
        }
"""
content = re.sub(r'async function fetchCustomer\(identifier\) \{.*?\n        \}', new_fetchCustomer, content, flags=re.DOTALL)

# 3. Update onScanSuccess
new_onScanSuccess = """
        async function onScanSuccess(decodedText) {
            try{ html5QrcodeScanner.stop(); }catch(e){}
            document.getElementById('cyber-effect').style.display = 'none';
            
            const parts = decodedText.split('|');
            const cId = parts[0];
            const campId = parts.length > 1 ? parts[1] : null;
            
            currentCustomerId = cId;
            window.currentCampaignId = campId;
            
            showToast('Pase escaneado. Buscando...', 'info');
            const data = await fetchCustomer(cId);
            
            if (data) {
                if (campId) {
                    const link = await fetchCustomerCampaign(cId, campId);
                    if (link) {
                        data.stamps_count = link.stamps_count;
                        data.balance_cashback = link.cashback_balance;
                    }
                    const { data: camp } = await supabaseClient.from('campaigns').select('*').eq('id', campId).single();
                    if (camp) window.currentCampaignData = camp;
                }
                
                showToast('Cliente localizado', 'success');
                renderClientProfile(data);
            } else {
                resetScanner();
            }
        }
"""
content = re.sub(r'async function onScanSuccess\(decodedText\) \{.*?\n        \}', new_onScanSuccess, content, flags=re.DOTALL)

# 4. Update searchCustomerManual
new_searchCustomerManual = """
        async function searchCustomerManual() {
            const query = document.getElementById('manual-search-input').value.trim();
            const btn = document.getElementById('btn-manual-search');
            if (!query) { showToast('Ingresa un teléfono o correo', 'error'); return; }
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Buscando...';
            btn.disabled = true;

            const data = await fetchCustomer(query);
            btn.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i> Buscar Cliente';
            btn.disabled = false;
            
            if (data) {
                window.currentCampaignId = null;
                showToast('Cliente localizado (Búsqueda manual - Modo Global)', 'warning');
                currentCustomerId = data.id;
                renderClientProfile(data);
            }
        }
"""
content = re.sub(r'async function searchCustomerManual\(\) \{.*?\n        \}', new_searchCustomerManual, content, flags=re.DOTALL)

# 5. Fix renderClientProfile
content = content.replace("const totalStampsReq = currentMerchantData?.stamps_total || 10;", "const totalStampsReq = (window.currentCampaignData && window.currentCampaignData.rules_config && window.currentCampaignData.rules_config.stamps_total) ? window.currentCampaignData.rules_config.stamps_total : (currentMerchantData?.stamps_total || 10);")

# 6. Update processAction
new_processAction = """
        async function processAction(actionType) {
            if (!window.currentCustomerData) return;
            const amountStr = document.getElementById('op-amount').value;
            let amount = parseFloat(amountStr);
            if (actionType === 'add_stamp_only' || actionType === 'redeem_reward') {
                amount = 0; 
            } else {
                if (isNaN(amount) || amount <= 0) {
                    showToast('Ingresa el monto de la operación primero.', 'error');
                    document.getElementById('op-amount').focus();
                    return;
                }
            }

            showToast('Procesando transacción en vivo...', 'info');
            
            let statusMsg = "";
            let newCashback = parseFloat(window.currentCustomerData.balance_cashback || 0);
            let newWallet = parseFloat(window.currentCustomerData.wallet_balance || 0);
            let newStamps = parseInt(window.currentCustomerData.stamps_count || 0);
            let newVisits = parseInt(window.currentCustomerData.visits || 0) + 1;
            let newLifetime = parseFloat(window.currentCustomerData.lifetime_value || 0);
            let totalSpent = parseFloat(window.currentCustomerData.total_spent || 0);
            
            let txType = '';
            let cashbackEarned = 0;
            let cashbackRedeemed = 0;
            let walletAmount = 0;
            
            if (actionType === 'add_funds') {
                txType = 'earn';
                newWallet += amount;
                walletAmount = amount;
                newLifetime += amount;
                statusMsg = `<strong style="color:var(--text-main);">Depósito Completado</strong><br><br>Se abonaron <span style="color:var(--success); font-weight:800;">$${amount.toFixed(2)} USD</span><br>al Monedero del cliente.`;
            } 
            else if (actionType === 'charge_ticket') {
                txType = 'redeem';
                let amountToPay = amount;
                if (newWallet > 0) {
                    if (newWallet >= amountToPay) { newWallet -= amountToPay; amountToPay = 0; }
                    else { amountToPay -= newWallet; newWallet = 0; }
                }
                if (amountToPay > 0 && newCashback > 0) {
                    if (newCashback >= amountToPay) { newCashback -= amountToPay; amountToPay = 0; }
                    else { amountToPay -= newCashback; newCashback = 0; }
                }
                const cashbackRate = (window.currentCampaignData && window.currentCampaignData.rules_config && window.currentCampaignData.rules_config.cashback_percent) ? window.currentCampaignData.rules_config.cashback_percent : (currentMerchantData?.cashback_percent || 0);
                cashbackEarned = amount * (cashbackRate / 100);
                newCashback += cashbackEarned;
                totalSpent += amount;
                statusMsg = `<strong style="color:var(--text-main);">Venta Cobrada</strong><br><br>El cliente ganó <span style="color:var(--accent-violet); font-weight:800;">$${cashbackEarned.toFixed(2)}</span> de Cashback por esta compra.`;
            }
            else if (actionType === 'add_stamp_only') {
                txType = 'earn';
                newStamps += 1;
                statusMsg = `<strong style="color:var(--text-main);">Sello Otorgado</strong><br><br>El cliente ahora tiene <span style="color:var(--warning); font-weight:800;">${newStamps} sellos</span>.`;
            }
            else if (actionType === 'redeem_reward') {
                txType = 'redeem';
                const required = (window.currentCampaignData && window.currentCampaignData.rules_config && window.currentCampaignData.rules_config.stamps_total) ? window.currentCampaignData.rules_config.stamps_total : (currentMerchantData?.stamps_total || 10);
                if (newStamps >= required) {
                    newStamps -= required;
                    statusMsg = `<strong style="color:var(--success);">¡Recompensa Canjeada!</strong><br><br>Se restaron ${required} sellos.`;
                } else {
                    showToast(`No tiene suficientes sellos (Requiere ${required})`, 'error');
                    return;
                }
            }

            try {
                const { error: updErr } = await supabaseClient.from('customers').update({
                    balance_cashback: newCashback,
                    wallet_balance: newWallet,
                    stamps_count: newStamps,
                    visits: newVisits,
                    lifetime_value: newLifetime,
                    total_spent: totalSpent,
                    last_visit: new Date().toISOString()
                }).eq('id', window.currentCustomerData.id);

                if (updErr) throw updErr;

                if (window.currentCampaignId) {
                    const { error: campUpdErr } = await supabaseClient.from('customer_campaigns').update({
                        stamps_count: newStamps,
                        cashback_balance: newCashback,
                        updated_at: new Date().toISOString()
                    }).eq('customer_id', window.currentCustomerData.id).eq('campaign_id', window.currentCampaignId);
                    if (campUpdErr) console.error("Warning: could not update customer_campaigns", campUpdErr);
                }

                const { error: txErr } = await supabaseClient.from('transactions').insert([{
                    merchant_id: currentMerchantData.id,
                    customer_id: window.currentCustomerData.id,
                    campaign_id: window.currentCampaignId || null,
                    type: txType,
                    amount: amount,
                    cashback_earned: cashbackEarned,
                    cashback_redeemed: cashbackRedeemed,
                    wallet_amount: walletAmount,
                    stamps_awarded: (actionType==='add_stamp_only')?1:0,
                    status: 'completed',
                    metadata: { source: 'scanner', action: actionType }
                }]);

                if (txErr) throw txErr;

                document.getElementById('status-msg').innerHTML = statusMsg;
                document.getElementById('status-overlay').style.display = 'flex';
                
                try { fetch(`/api/pass/${window.currentCustomerData.id}/webhook`, { method: 'POST' }); } catch(e){}

            } catch (e) {
                console.error(e);
                showToast('Error en transacción: ' + e.message, 'error');
            }
        }
"""
content = re.sub(r'async function processAction\(actionType\) \{.*?\n        \}', new_processAction, content, flags=re.DOTALL)

with open('scanner.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Scanner refactored successfully.")
