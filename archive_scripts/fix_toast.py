import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update showToast
target_toast = """        let iconClass = 'fa-circle-info';
        if (type === 'success') iconClass = 'fa-circle-check text-emerald';
        if (type === 'warning') iconClass = 'fa-triangle-exclamation';

        toast.innerHTML = `<i class="fa-solid ${iconClass}"></i> <span>${message}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);"""

replacement_toast = """        let iconClass = 'fa-circle-info';
        if (type === 'success') iconClass = 'fa-circle-check text-emerald';
        if (type === 'warning') iconClass = 'fa-triangle-exclamation';
        if (type === 'error') iconClass = 'fa-circle-xmark';
        
        let errColor = type === 'error' ? 'color:#ef4444;' : '';
        let autoReportBtn = '';
        
        if (type === 'error') {
            const safeMsg = message.replace(/'/g, "\\\\'").replace(/"/g, '&quot;');
            autoReportBtn = `<button onclick="window.autoReportError('${safeMsg}', this)" style="margin-left:12px; background:rgba(239, 68, 68, 0.1); color:#ef4444; border:1px solid rgba(239, 68, 68, 0.3); border-radius:6px; padding:4px 8px; font-size:10px; cursor:pointer; font-weight:bold; white-space:nowrap; transition:all 0.2s;">Reportar Problema</button>`;
        }

        toast.innerHTML = `<i class="fa-solid ${iconClass}" style="${errColor}"></i> <span style="flex:1;">${message}</span> ${autoReportBtn}`;
        container.appendChild(toast);

        const delay = type === 'error' ? 10000 : 4000; // Give 10 seconds for errors so they can click report
        setTimeout(() => {
            if(toast) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => toast.remove(), 300);
            }
        }, delay);"""

js = js.replace(target_toast, replacement_toast)

# 2. Add window.autoReportError
target_report = "window.submitSupportTicket = async function(type) {"
replacement_report = """window.autoReportError = async function(errMsg, btnEl) {
    if (btnEl) {
        btnEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        btnEl.disabled = true;
    }
    try {
        const { error } = await window.supabaseClient.from('support_tickets').insert([{
            merchant_id: window.merchantSession ? window.merchantSession.user.id : null,
            email: window.merchantSession ? window.merchantSession.user.email : 'auto-report',
            subject: '[AUTO-REPORTE] Error del Sistema',
            message: 'El sistema arrojó el siguiente error al usuario:\\n\\n' + errMsg,
            status: 'abierto'
        }]);
        
        if (btnEl) {
            btnEl.innerHTML = '<i class="fa-solid fa-check"></i> Reportado';
            btnEl.style.background = 'rgba(16, 185, 129, 0.1)';
            btnEl.style.color = '#10b981';
            btnEl.style.borderColor = 'rgba(16, 185, 129, 0.3)';
        }
    } catch(err) {
        if (btnEl) btnEl.innerHTML = 'Fallo al reportar';
    }
};

window.submitSupportTicket = async function(type) {"""

js = js.replace(target_report, replacement_report)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
