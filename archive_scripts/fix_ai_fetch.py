import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_auth = """    try {
        const token = localStorage.getItem('merchant_token');
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ industry, businessName })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('https://api.fideliorewards.com/api/ai/magic-builder', reqOpts).catch(() => fetch('/api/ai/magic-builder', reqOpts));"""

good_auth = """    try {
        const token = window.merchantSession?.access_token || '';
        const reqOpts = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ industry, businessName })
        };
        if (token) reqOpts.headers['Authorization'] = `Bearer ${token}`;

        const res = await fetch('/api/ai/magic-builder', reqOpts);"""

js = js.replace(bad_auth, good_auth)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
