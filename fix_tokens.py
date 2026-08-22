import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix all token retrieval logic for AI fetch calls
js = js.replace("localStorage.getItem('merchant_token')", "window.merchantSession?.access_token")

# Also, there's fidelio_jwt and fidelio_token in other places? Let's check those too.
# line 4119: const token = localStorage.getItem('fidelio_token');
# line 5705: const token = localStorage.getItem('fidelio_jwt');
# It's safer to just replace them all with window.merchantSession?.access_token if they are used for backend API calls.
js = js.replace("localStorage.getItem('fidelio_token')", "window.merchantSession?.access_token")
js = js.replace("localStorage.getItem('fidelio_jwt')", "window.merchantSession?.access_token")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Tokens unified.")
