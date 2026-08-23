import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Inject requireSpecialCardPayment
require_logic = """
window.requireSpecialCardPayment = function() {
    window.specialCardPaymentPending = true;
    const conceptInput = document.getElementById('caja-concept');
    if(conceptInput) conceptInput.value = 'Pago por Tarjeta Especial';
    
    // Auto-select general client
    const customerSelect = document.getElementById('caja-customer');
    if(customerSelect) customerSelect.value = '';
    
    window.openCajaModal();
};
"""
if "window.requireSpecialCardPayment" not in js:
    js = js.replace('window.openCajaModal = function() {', require_logic + '\nwindow.openCajaModal = function() {')

# 2. Edit saveCajaTransaction to handle the flag
old_save_success = """        if (error) {
            console.error(error);
            if(typeof window.showToast === 'function') window.showToast("Error al guardar transacción.", "error");
            btn.innerHTML = originalText;
            btn.disabled = false;
            return;
        }
        
        if(typeof window.showToast === 'function') window.showToast("Transacción registrada", "success");
        window.closeCajaModal();
        window.loadCajaTransactions();"""

new_save_success = """        if (error) {
            console.error(error);
            if(typeof window.showToast === 'function') window.showToast("Error al guardar transacción.", "error");
            btn.innerHTML = originalText;
            btn.disabled = false;
            return;
        }
        
        if(typeof window.showToast === 'function') window.showToast("Transacción registrada", "success");
        window.closeCajaModal();
        window.loadCajaTransactions();
        
        // Unlock special card emission if pending
        if (window.specialCardPaymentPending) {
            window.specialCardPaymentPending = false;
            const btnPayment = document.getElementById('special-card-pre-payment');
            const btnsEmission = document.getElementById('special-card-emission-buttons');
            if(btnPayment) btnPayment.style.display = 'none';
            if(btnsEmission) btnsEmission.style.display = 'grid';
            if(typeof window.showToast === 'function') window.showToast('Pago registrado. Procede a emitir la tarjeta.', 'success');
        }"""

if "window.specialCardPaymentPending = false;" not in js:
    js = js.replace(old_save_success, new_save_success)

# 3. Edit emitirEspecial to reset the UI after emission
old_emit_reset = """        // Limpiar
        document.getElementById('emit-special-name').value = '';
        document.getElementById('emit-special-phone').value = '';
        document.getElementById('emit-special-email').value = '';"""

new_emit_reset = """        // Limpiar
        document.getElementById('emit-special-name').value = '';
        document.getElementById('emit-special-phone').value = '';
        document.getElementById('emit-special-email').value = '';
        
        // Reset special card emission UI back to payment required
        const btnPayment = document.getElementById('special-card-pre-payment');
        const btnsEmission = document.getElementById('special-card-emission-buttons');
        if(btnPayment) btnPayment.style.display = 'block';
        if(btnsEmission) btnsEmission.style.display = 'none';"""

if "Reset special card emission UI" not in js:
    js = js.replace(old_emit_reset, new_emit_reset)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS updated.")
