with open('scanner.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """            const data = await fetchCustomer(cId);
            
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
            }"""

replacement = """            const data = await fetchCustomer(cId);
            
            if (data) {
                if (campId) {
                    // VERIFICACION ESTRICTA: La campaña debe pertenecer a este negocio
                    const { data: camp, error: campErr } = await supabaseClient.from('campaigns').select('*').eq('id', campId).eq('merchant_id', currentMerchantData.id).single();
                    if (campErr || !camp) {
                        alert('❌ TARJETA RECHAZADA:\\n\\nEsta tarjeta digital pertenece a otro negocio o profesional.\\n\\nNo puedes escanearla en este panel.');
                        resetScanner();
                        return;
                    }
                    
                    const link = await fetchCustomerCampaign(cId, campId);
                    if (link) {
                        data.stamps_count = link.stamps_count;
                        data.balance_cashback = link.cashback_balance;
                    }
                    window.currentCampaignData = camp;
                }
                
                showToast('Cliente localizado', 'success');
                renderClientProfile(data);
            } else {
                alert('❌ ACCESO DENEGADO:\\n\\nEste código QR no pertenece a tu base de datos de clientes o es de otro negocio.\\n\\nLa visita NO será registrada.');
                resetScanner();
            }"""

html = html.replace(target, replacement)

with open('scanner.html', 'w', encoding='utf-8') as f:
    f.write(html)
