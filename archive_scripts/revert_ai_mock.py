import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_mock = """    try {
        // DEMO MOCK: Simulate API delay
        await new Promise(r => setTimeout(r, 2000));
        
        const strategy = {
            primaryColor: '#7C3AED',
            accentColor: '#10B981',
            reward: '1 Bebida Gratis o Postre',
            instruction: 'Acumula 5 sellos para canjear.',
            stampsTotal: 5,
            iconClass: 'fa-solid fa-mug-hot',
            tip: 'Para restaurantes y cafeterías, regalar un ticket bajo (bebida) en la 5ta visita incrementa la retención un 35%.'
        };"""

good_original = """    try {
        const token = localStorage.getItem('merchant_token');
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ industry, businessName })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('https://api.fideliorewards.com/api/ai/magic-builder', reqOpts).catch(() => fetch('/api/ai/magic-builder', reqOpts));
        
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.error || 'Error al conectar con Gemini API');
        }
        
        const strategy = await res.json();"""

js = js.replace(bad_mock, good_original)

# Also expose showToast globally so the user can see errors
js = js.replace('function showToast(message, type = "info") {', 'window.showToast = function(message, type = "info") {')

# Also fix the calls inside the DOMContentLoaded to use window.showToast
js = js.replace('showToast(', 'window.showToast(')

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
