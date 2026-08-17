import re

with open('dashboard.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add loadAppointments and loadBankStats to the tab logic
old_tabs_logic = """                if(targetTab === 'tab-leads' && typeof window.loadLeads === 'function') window.loadLeads();
                else if(targetTab === 'tab-global-db' && typeof window.loadGlobalDatabase === 'function') window.loadGlobalDatabase();
                else if(targetTab === 'tab-merchants-control' && typeof window.loadMerchantsControl === 'function') window.loadMerchantsControl();
                else if(targetTab === 'tab-inbox' && typeof window.loadInbox === 'function') window.loadInbox();
                else if(targetTab === 'tab-fidelio-team' && typeof window.loadFidelioTeam === 'function') window.loadFidelioTeam();"""

new_tabs_logic = """                if(targetTab === 'tab-leads' && typeof window.loadLeads === 'function') window.loadLeads();
                else if(targetTab === 'tab-global-db' && typeof window.loadGlobalDatabase === 'function') window.loadGlobalDatabase();
                else if(targetTab === 'tab-merchants-control' && typeof window.loadMerchantsControl === 'function') window.loadMerchantsControl();
                else if(targetTab === 'tab-inbox' && typeof window.loadInbox === 'function') window.loadInbox();
                else if(targetTab === 'tab-fidelio-team' && typeof window.loadFidelioTeam === 'function') window.loadFidelioTeam();
                else if(targetTab === 'tab-appointments' && typeof window.loadAppointments === 'function') window.loadAppointments();
                else if(targetTab === 'tab-bank' && typeof window.loadBankStats === 'function') window.loadBankStats();"""

if old_tabs_logic in js and "tab-appointments" not in old_tabs_logic:
    js = js.replace(old_tabs_logic, new_tabs_logic)
    with open('dashboard.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed tab loading logic in dashboard.js")
else:
    print("Tab logic already updated or not found")
