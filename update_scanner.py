import re
import os

filepath = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/scanner.html'

with open(filepath, 'r') as f:
    content = f.read()

# We need to replace the logic from `let mockCustomerData` downwards.
# Let's find `let mockCustomerData` and replace everything down to `</script>` before `</body>`

replacement = """
        let currentMerchantData = null;

        async function init() {
            try {
                const res = await fetch('/api/config');
                const config = await res.json();
                supabaseClient = supabase.createClient(config.supabaseUrl, config.supabaseAnonKey);
                
                const { data, error } = await supabaseClient.auth.getSession();
                if (!error && data && data.session) {
                    await setupScannerSession(data.session);
                } else {
                    document.getElementById('login-screen').style.display = 'flex';
                }
            } catch (e) {
                showToast('Error conectando con el servidor', 'error');
                document.getElementById('login-screen').style.display = 'flex';
            }
        }

        async function handleLogin() {
            const email = document.getElementById('login-email').value.trim();
            const password = document.getElementById('login-password').value;
            const btn = document.getElementById('btn-login');

            if (!email || !password) {
                showToast('Llena todos los campos', 'error');
                return;
            }

            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Entrando...';
            
            const { data, error } = await supabaseClient.auth.signInWithPassword({ email, password });
            
            if (error) {
                showToast('Usuario o contraseña incorrectos', 'error');
                btn.innerHTML = 'Ingresar al Sistema';
                return;
            }
            await setupScannerSession(data.session);
        }

        async function setupScannerSession(session) {
            merchantSession = session;
            const role = session.user.user_metadata?.role;
            const targetMerchantId = role === 'staff' ? session.user.user_metadata.merchant_id : session.user.id;
            
            const { data: merchant } = await supabaseClient
                .from('merchants')
                .select('*')
                .eq('id', targetMerchantId)
                .single();
                
            if (merchant) {
                currentMerchantData = merchant;
                let badge = role === 'staff' ? ' <i class="fa-solid fa-user-tag"></i> Cajero' : ' <i class="fa-solid fa-crown"></i> Admin';
                document.getElementById('merchant-name').innerHTML = merchant.business_name + badge;
            }

            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('main-container').style.display = 'grid'; // Grid View
            showToast('Sesión Iniciada', 'success');
            setMode('scan');
        }

        function setMode(mode) {
            const btnScan = document.getElementById('btn-mode-scan');
            const btnManual = document.getElementById('btn-mode-manual');
            const btnNfc = document.getElementById('btn-mode-nfc');

            [btnScan, btnManual, btnNfc].forEach(btn => {
                btn.style.background = 'transparent';
                btn.style.color = 'var(--text-muted)';
                btn.style.boxShadow = 'none';
            });

            document.getElementById('scanner-section').style.display = 'none';
            document.getElementById('manual-section').style.display = 'none';
            document.getElementById('nfc-section').style.display = 'none';

            if (mode === 'scan') {
                document.getElementById('scanner-section').style.display = 'block';
                btnScan.style.background = 'var(--accent-gradient)';
                btnScan.style.color = 'white';
                btnScan.style.boxShadow = '0 4px 15px rgba(139, 92, 246, 0.3)';
                
                if (!html5QrcodeScanner) { startScanner(); } 
                else { try { html5QrcodeScanner.clear(); } catch(e){} startScanner(); }
            } else if (mode === 'nfc') {
                document.getElementById('nfc-section').style.display = 'flex';
                btnNfc.style.background = 'var(--accent-gradient)';
                btnNfc.style.color = 'white';
                btnNfc.style.boxShadow = '0 4px 15px rgba(139, 92, 246, 0.3)';
                if (html5QrcodeScanner) { try { html5QrcodeScanner.stop(); } catch(e){} }
            } else {
                document.getElementById('manual-section').style.display = 'flex';
                btnManual.style.background = 'var(--accent-gradient)';
                btnManual.style.color = 'white';
                btnManual.style.boxShadow = '0 4px 15px rgba(139, 92, 246, 0.3)';
                if (html5QrcodeScanner) { try { html5QrcodeScanner.stop(); } catch(e){} }
            }
        }

        async function startNfcReader() {
            const errEl = document.getElementById('nfc-error');
            const btn = document.getElementById('btn-nfc-start');
            errEl.style.display = 'none';

            if (!('NDEFReader' in window)) {
                errEl.textContent = "Tu navegador o dispositivo no soporta lectura NFC (Requiere Chrome en Android).";
                errEl.style.display = 'block';
                return;
            }

            try {
                const ndef = new NDEFReader();
                btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Escaneando NFC...';
                await ndef.scan();
                
                showToast('Escáner NFC Activado. Acerca la tarjeta.', 'info');
                
                ndef.addEventListener("readingerror", () => {
                    errEl.textContent = "No se pudo leer la tarjeta. Intenta acercarla más.";
                    errEl.style.display = 'block';
                });

                ndef.addEventListener("reading", ({ message, serialNumber }) => {
                    let nfcText = "";
                    for (const record of message.records) {
                        if (record.recordType === "text") {
                            const textDecoder = new TextDecoder(record.encoding);
                            nfcText = textDecoder.decode(record.data);
                            break;
                        }
                    }
                    
                    if (nfcText) {
                        showToast('Tarjeta NFC Leída con éxito', 'success');
                        btn.innerHTML = '<i class="fa-solid fa-satellite-dish"></i> Activar Lector NFC';
                        onScanSuccess(nfcText);
                    } else {
                        showToast('Hardware Tag Leído', 'success');
                        btn.innerHTML = '<i class="fa-solid fa-satellite-dish"></i> Activar Lector NFC';
                        onScanSuccess(serialNumber);
                    }
                });
            } catch (error) {
                errEl.textContent = "Error iniciando NFC: " + error.message;
                errEl.style.display = 'block';
                btn.innerHTML = '<i class="fa-solid fa-satellite-dish"></i> Activar Lector NFC';
            }
        }

        function startScanner() {
            document.getElementById('cyber-effect').style.display = 'block';
            
            html5QrcodeScanner = new Html5Qrcode("reader");
            const config = { fps: 10, qrbox: { width: 250, height: 250 } };
            
            html5QrcodeScanner.start({ facingMode: "environment" }, config, onScanSuccess, (err) => {})
            .catch(err => {
                document.getElementById('cyber-effect').style.display = 'none';
                document.getElementById('reader').innerHTML = '<div style="padding:40px; text-align:center; color:var(--text-muted); display:flex; flex-direction:column; justify-content:center; height:100%;"><i class="fa-solid fa-video-slash" style="font-size:3rem; margin-bottom:16px; color:var(--danger);"></i><span>Cámara bloqueada o no detectada.</span></div>';
            });
        }

        function renderClientProfile(data) {
            document.getElementById('empty-state').style.opacity = '0';
            setTimeout(() => { document.getElementById('empty-state').style.display = 'none'; }, 300);
            
            document.getElementById('op-amount').disabled = false;
            document.getElementById('btn-charge').disabled = false;
            document.getElementById('btn-add').disabled = false;
            
            document.getElementById('c-name').textContent = data.full_name || data.name || 'Cliente';
            document.getElementById('c-tier').innerHTML = `<i class="fa-solid fa-crown"></i> Cliente ${data.vip_tier || 'Bronce'}`;
            
            document.getElementById('c-monedero').innerHTML = `$${parseFloat(data.wallet_balance || 0).toFixed(2)}`;
            document.getElementById('c-cashback').innerHTML = `$${parseFloat(data.balance_cashback || 0).toFixed(2)}`;
            
            let stampsHtml = '';
            const totalStampsReq = currentMerchantData?.stamps_total || 10;
            const currentStamps = data.stamps_count || 0;
            
            for(let i=0; i < totalStampsReq; i++) {
                if(i < currentStamps) stampsHtml += '<i class="fa-solid fa-star"></i> ';
                else stampsHtml += '<i class="fa-regular fa-star" style="opacity:0.4;"></i> ';
            }
            document.getElementById('c-stamps').innerHTML = stampsHtml;
            
            // Save current customer global state
            window.currentCustomerData = data;
        }

        async function fetchCustomer(identifier) {
            try {
                let query = supabaseClient.from('customers').select('*').eq('merchant_id', currentMerchantData.id);
                
                // Si parece UUID, buscar por ID
                if (identifier.length === 36 && identifier.includes('-')) {
                    query = query.eq('id', identifier);
                } else if (identifier.includes('@')) {
                    query = query.eq('email', identifier.toLowerCase());
                } else {
                    query = query.eq('phone', identifier);
                }
                
                const { data, error } = await query.single();
                
                if (error || !data) {
                    showToast('Cliente no encontrado en este restaurante', 'error');
                    return null;
                }
                
                return data;
            } catch (err) {
                console.error(err);
                return null;
            }
        }

        async function onScanSuccess(decodedText) {
            try{ html5QrcodeScanner.stop(); }catch(e){}
            document.getElementById('cyber-effect').style.display = 'none';
            currentCustomerId = decodedText;
            
            showToast('Pase escaneado. Buscando...', 'info');
            const data = await fetchCustomer(decodedText);
            
            if (data) {
                showToast('Cliente localizado', 'success');
                renderClientProfile(data);
            } else {
                resetScanner();
            }
        }

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
                showToast('Cliente localizado', 'success');
                currentCustomerId = data.id;
                renderClientProfile(data);
            }
        }

        function resetScanner() {
            document.getElementById('empty-state').style.display = 'flex';
            setTimeout(() => { document.getElementById('empty-state').style.opacity = '1'; }, 10);
            
            document.getElementById('op-amount').value = '';
            document.getElementById('op-amount').disabled = true;
            document.getElementById('btn-charge').disabled = true;
            document.getElementById('btn-add').disabled = true;
            
            document.getElementById('status-overlay').style.display = 'none';
            currentCustomerId = null;
            window.currentCustomerData = null;
            
            if (document.getElementById('btn-mode-manual').style.color === 'white') {
                setMode('manual');
            } else {
                setMode('scan');
            }
        }

        // ==========================================
        // LÓGICA DE TRANSACCIONES (Supabase Live)
        // ==========================================
        async function processAction(actionType) {
            if (!window.currentCustomerData) return;
            
            const amountStr = document.getElementById('op-amount').value;
            const amount = parseFloat(amountStr);
            
            if (isNaN(amount) || amount <= 0) {
                showToast('Ingresa el monto de la operación primero.', 'error');
                document.getElementById('op-amount').focus();
                return;
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
            let msgParts = [];
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
                txType = 'redeem'; // Although it's a purchase, it can consume cashback
                let amountToPay = amount;
                
                // Consumir Monedero primero
                if (newWallet > 0) {
                    if (newWallet >= amountToPay) {
                        newWallet -= amountToPay;
                        msgParts.push(`<span style="color:var(--success); font-weight:700;">-$${amountToPay.toFixed(2)} pagados con Monedero pre-pagado</span>`);
                        amountToPay = 0;
                    } else {
                        msgParts.push(`<span style="color:var(--success); font-weight:700;">-$${newWallet.toFixed(2)} agotados del Monedero pre-pagado</span>`);
                        amountToPay -= newWallet;
                        newWallet = 0;
                    }
                }
                
                // Consumir Cashback si aún hay que pagar
                if (amountToPay > 0 && newCashback > 0) {
                    if (newCashback >= amountToPay) {
                        cashbackRedeemed = amountToPay;
                        newCashback -= amountToPay;
                        msgParts.push(`<span style="color:var(--accent-violet); font-weight:700;">-$${amountToPay.toFixed(2)} cobrados del Cashback</span>`);
                        amountToPay = 0;
                    } else {
                        cashbackRedeemed = newCashback;
                        msgParts.push(`<span style="color:var(--accent-violet); font-weight:700;">-$${newCashback.toFixed(2)} agotados del Cashback</span>`);
                        amountToPay -= newCashback;
                        newCashback = 0;
                    }
                }
                
                // Lo que sobra genera cashback nuevo
                if (amountToPay > 0) {
                    const cashbackRate = parseFloat(currentMerchantData?.cashback_percent || 10) / 100;
                    cashbackEarned = amountToPay * cashbackRate;
                    newCashback += cashbackEarned;
                    msgParts.push(`<span style="color:var(--text-main); font-weight:600;">Restante pagado en caja: $${amountToPay.toFixed(2)}</span>`);
                    if (cashbackEarned > 0) {
                        msgParts.push(`<span style="color:var(--accent-violet); font-weight:700;">+ $${cashbackEarned.toFixed(2)} Cashback Ganado</span>`);
                    }
                }
                
                // Sello
                const stampsReq = currentMerchantData?.stamps_total || 10;
                newStamps += 1;
                let stampMsg = `<span style="color:var(--warning); font-weight:700;">+ 1 Sello Registrado</span>`;
                if (newStamps >= stampsReq) {
                    stampMsg += `<br><strong style="color:var(--success); font-size:1.1rem;">¡CLIENTE GANÓ RECOMPENSA!</strong>`;
                    newStamps = 0; // Reset
                }
                msgParts.push(stampMsg);

                totalSpent += amount;
                
                statusMsg = `<strong style="color:var(--text-main); font-size:1.4rem;">Ticket total: $${amount.toFixed(2)}</strong><br><br><div style="text-align:left; font-size:1.1rem; line-height:1.8; background:var(--bg-main); padding:20px; border-radius:16px; border:1px solid var(--border-soft); margin-top:12px;">${msgParts.join('<br>')}</div>`;
            }

            try {
                // Update Customer
                const { error: updErr } = await supabaseClient
                    .from('customers')
                    .update({
                        wallet_balance: newWallet,
                        balance_cashback: newCashback,
                        stamps_count: newStamps,
                        visits: newVisits,
                        lifetime_value: newLifetime,
                        total_spent: totalSpent,
                        last_visit: new Date().toISOString()
                    })
                    .eq('id', window.currentCustomerData.id);

                if (updErr) throw updErr;

                // Insert Transaction
                await supabaseClient.from('transactions').insert([{
                    merchant_id: currentMerchantData.id,
                    customer_id: window.currentCustomerData.id,
                    transaction_type: txType,
                    amount_spent: amount,
                    cashback_earned: cashbackEarned,
                    cashback_redeemed: cashbackRedeemed,
                    stamps_earned: 1,
                    wallet_amount: walletAmount
                }]);

                document.getElementById('status-overlay').style.display = 'flex';
                document.getElementById('status-msg').innerHTML = statusMsg;
                
            } catch (err) {
                console.error(err);
                showToast('Error de conexión. Intenta de nuevo.', 'error');
            }
        }

        document.addEventListener('DOMContentLoaded', init);
"""

# Replace everything from `let mockCustomerData` to the end script tag
pattern = re.compile(r'let mockCustomerData.*(?=</script>)', re.DOTALL)
new_content = pattern.sub(replacement, content)

with open(filepath, 'w') as f:
    f.write(new_content)
