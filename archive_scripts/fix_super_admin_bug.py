import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the bug that caused any email containing 'fidelio' to become super admin
js = js.replace("if ((currentEmail.trim().toLowerCase().includes('hola') || currentEmail.trim().toLowerCase().includes('fidelio')))", "if (currentEmail === 'hola@fideliorewards.com' || currentEmail === 'ro8ert@gmail.com')")

# Remove the broken 'fidelio' includes condition above it too
js = js.replace("if (currentEmail.toLowerCase().includes('hola') && !(currentEmail.trim().toLowerCase().includes('hola') || currentEmail.trim().toLowerCase().includes('fidelio')))", "if (false)")

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

