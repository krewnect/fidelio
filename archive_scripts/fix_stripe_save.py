with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """    // Asignar el payment link a la campaña especificada (Mock)
    console.log("Stripe Linked to campaign: " + campId);
    
    if (typeof showToast === 'function') showToast("Checkout de Stripe vinculado exitosamente a la Tarjeta", "success");"""

replacement = """    const btn = event ? event.target.closest('button') : null;
    const originalText = btn ? btn.innerHTML : '';
    if(btn) btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Vinculando...';

    // Update campaign in Supabase
    try {
        const { error } = await window.supabaseClient
            .from('campaigns')
            .update({ stripe_payment_link: paymentLink })
            .eq('id', campId);
            
        if (error) throw error;
        
        if (typeof showToast === 'function') showToast("Checkout de Stripe vinculado exitosamente", "success");
        linkInput.value = ''; // clear
    } catch(err) {
        console.error("Error saving Stripe Link:", err);
        if (typeof showToast === 'function') showToast("Error al guardar enlace: " + err.message, "error");
    } finally {
        if(btn) btn.innerHTML = originalText;
    }"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
