import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Dashboard Insights Caching
old_dash = """    try {
        const sales = document.getElementById('metric-sales') ? document.getElementById('metric-sales').textContent : '$0.00';
        const scans = document.getElementById('metric-scans') ? document.getElementById('metric-scans').textContent : '0';
        const active = document.getElementById('metric-active-users') ? document.getElementById('metric-active-users').textContent : '0';
        
        const token = window.merchantSession?.access_token;
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ metrics: { sales, scans, active } })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('/api/ai/dashboard-insights', reqOpts);"""

new_dash = """    try {
        const cacheKey = 'gemini_cache_dashboard';
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const parsed = JSON.parse(cached);
            if (Date.now() - parsed.timestamp < 1000 * 60 * 60 * 4) { // 4 hours TTL
                textEl.innerHTML = `<b>Insight:</b> ${parsed.data.insight}`;
                return;
            }
        }

        const sales = document.getElementById('metric-sales') ? document.getElementById('metric-sales').textContent : '$0.00';
        const scans = document.getElementById('metric-scans') ? document.getElementById('metric-scans').textContent : '0';
        const active = document.getElementById('metric-active-users') ? document.getElementById('metric-active-users').textContent : '0';
        
        const token = window.merchantSession?.access_token;
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ metrics: { sales, scans, active } })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('/api/ai/dashboard-insights', reqOpts);"""

js = js.replace(old_dash, new_dash)

# Cache saving for Dashboard
old_dash_save = """        if(typeof stepInterval !== 'undefined') clearInterval(stepInterval);
        const data = await res.json();
        
        textEl.innerHTML = `<b>Insight:</b> ${data.insight}`;"""

new_dash_save = """        if(typeof stepInterval !== 'undefined') clearInterval(stepInterval);
        const data = await res.json();
        
        localStorage.setItem('gemini_cache_dashboard', JSON.stringify({ timestamp: Date.now(), data }));
        textEl.innerHTML = `<b>Insight:</b> ${data.insight}`;"""

js = js.replace(old_dash_save, new_dash_save)

# 2. CRM Insights Caching
old_crm = """    try {
        const customersCount = typeof state !== "undefined" && state.customers ? state.customers.length : 0;
        
        const token = window.merchantSession?.access_token;
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customersCount })
        };"""

new_crm = """    try {
        const cacheKey = 'gemini_cache_crm';
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const parsed = JSON.parse(cached);
            if (Date.now() - parsed.timestamp < 1000 * 60 * 60 * 4) { // 4 hours TTL
                textEl.innerHTML = `<b>Oportunidad:</b> ${parsed.data.insight}`;
                return;
            }
        }

        const customersCount = typeof state !== "undefined" && state.customers ? state.customers.length : 0;
        
        const token = window.merchantSession?.access_token;
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customersCount })
        };"""
js = js.replace(old_crm, new_crm)

old_crm_save = """        const data = await res.json();
        
        textEl.innerHTML = `<b>Oportunidad:</b> ${data.insight}`;"""
new_crm_save = """        const data = await res.json();
        
        localStorage.setItem('gemini_cache_crm', JSON.stringify({ timestamp: Date.now(), data }));
        textEl.innerHTML = `<b>Oportunidad:</b> ${data.insight}`;"""
js = js.replace(old_crm_save, new_crm_save)

# 3. Metrics Insights Caching
old_metrics = """    try {
        const token = window.merchantSession?.access_token;"""
new_metrics = """    try {
        const cacheKey = 'gemini_cache_metrics';
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const parsed = JSON.parse(cached);
            if (Date.now() - parsed.timestamp < 1000 * 60 * 60 * 4) {
                textEl.innerHTML = `<b>Reporte de Optimización:</b> ${parsed.data.insight}`;
                return;
            }
        }
        const token = window.merchantSession?.access_token;"""
js = js.replace(old_metrics, new_metrics)

old_metrics_save = """        const data = await res.json();
        textEl.innerHTML = `<b>Reporte de Optimización:</b> ${data.insight}`;"""
new_metrics_save = """        const data = await res.json();
        localStorage.setItem('gemini_cache_metrics', JSON.stringify({ timestamp: Date.now(), data }));
        textEl.innerHTML = `<b>Reporte de Optimización:</b> ${data.insight}`;"""
js = js.replace(old_metrics_save, new_metrics_save)

# 4. Appointments Insights Caching
old_appt = """    try {
        const token = window.merchantSession?.access_token;"""
new_appt = """    try {
        const cacheKey = 'gemini_cache_appointments';
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            const parsed = JSON.parse(cached);
            if (Date.now() - parsed.timestamp < 1000 * 60 * 60 * 4) {
                textEl.innerHTML = `<b>Táctica Sugerida:</b> ${parsed.data.insight}`;
                return;
            }
        }
        const token = window.merchantSession?.access_token;"""
# Be careful to replace only the second occurrence since old_metrics is identical to old_appt
js = js.replace(old_appt, new_appt, 1)

old_appt_save = """        const data = await res.json();
        textEl.innerHTML = `<b>Táctica Sugerida:</b> ${data.insight}`;"""
new_appt_save = """        const data = await res.json();
        localStorage.setItem('gemini_cache_appointments', JSON.stringify({ timestamp: Date.now(), data }));
        textEl.innerHTML = `<b>Táctica Sugerida:</b> ${data.insight}`;"""
js = js.replace(old_appt_save, new_appt_save)


with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS updated with cache logic.")
