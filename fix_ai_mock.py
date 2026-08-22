import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_func = """    try {
        const token = localStorage.getItem('merchant_token');
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ industry, businessName })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('/api/ai/magic-builder', reqOpts);
        
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.error || 'Error al conectar con Gemini API');
        }
        
        const strategy = await res.json();"""

new_func = """    try {
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

js = js.replace(old_func, new_func)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
