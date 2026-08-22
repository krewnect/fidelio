with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_js = """
// --- GLOBAL GEMINI WIDGETS ---
window.fetchGeminiDashboardInsights = async function() {
    const textEl = document.getElementById('gemini-dashboard-text');
    if (!textEl) return;
    
    textEl.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Gemini está analizando tus ingresos y escaneos...';
    
    try {
        const sales = document.getElementById('metric-sales') ? document.getElementById('metric-sales').textContent : '$0.00';
        const scans = document.getElementById('metric-scans') ? document.getElementById('metric-scans').textContent : '0';
        const active = document.getElementById('metric-active-users') ? document.getElementById('metric-active-users').textContent : '0';
        
        const token = localStorage.getItem('merchant_token');
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ metrics: { sales, scans, active } })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('/api/ai/dashboard-insights', reqOpts);
        if (!res.ok) throw new Error('Error al conectar con Gemini');
        const data = await res.json();
        
        textEl.innerHTML = `<b>Insight:</b> ${data.insight}`;
    } catch (err) {
        textEl.innerHTML = '<i>No se pudo obtener el análisis de Gemini en este momento.</i>';
        console.error(err);
    }
};

window.fetchGeminiCRMInsights = async function() {
    const textEl = document.getElementById('gemini-crm-text');
    if (!textEl) return;
    
    textEl.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Evaluando oportunidades en tu base de clientes...';
    
    try {
        const customersCount = window.merchantData && window.merchantData.customers ? window.merchantData.customers.length : 0;
        
        const token = localStorage.getItem('merchant_token');
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customersCount })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('/api/ai/crm-insights', reqOpts);
        if (!res.ok) throw new Error('Error al conectar con Gemini');
        const data = await res.json();
        
        textEl.innerHTML = `<b>Recomendación Estratégica:</b> ${data.insight}`;
    } catch (err) {
        textEl.innerHTML = '<i>Gemini no está disponible en este momento.</i>';
        console.error(err);
    }
};

// Auto-trigger when switching tabs
document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch for dashboard if it's the active tab
    setTimeout(() => {
        if (document.getElementById('tab-home').classList.contains('active')) {
            fetchGeminiDashboardInsights();
        }
    }, 1500);
});

// We need to patch switchTab to also trigger these if needed
const originalSwitchTab = window.switchTab;
window.switchTab = function(tabId) {
    if(originalSwitchTab) originalSwitchTab(tabId);
    
    if (tabId === 'home') {
        setTimeout(fetchGeminiDashboardInsights, 500);
    } else if (tabId === 'crm') {
        setTimeout(fetchGeminiCRMInsights, 500);
    }
};
"""

js += new_js

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
