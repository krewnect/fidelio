import re

def fix_dashboard_mutual_exclusion():
    with open('dashboard.js', 'r') as f:
        content = f.read()

    old_func = """        window.checkPlanPermissions = function() {
            if (!window.merchantData) return;
            const plan = window.merchantData.business_type || 'starter';
            const isAdmin = window.merchantSession && window.merchantSession.user.email === 'hola@fideliorewards.com';
            
            // Business is the highest tier, Professional is the limited tier
            const isBusiness = plan === 'business' || plan === 'enterprise' || isAdmin;
            const isProfessional = plan === 'professional' || isBusiness; // If business, they have all professional stuff too
            
            // Enforce visibility of ALL tabs based on plan.
            const allNavTabs = document.querySelectorAll('.nav-tab');
            
            allNavTabs.forEach(tab => {
                const tabId = tab.getAttribute('data-tab');
                if (!tabId) return;
                
                // Tabs allowed for everyone (including starter)
                const baseTabs = ['tab-home', 'tab-metrics', 'tab-builder', 'tab-account', 'tab-support', 'tab-crm'];
                
                // Tabs allowed for Professional
                const proTabs = ['tab-appointments', 'tab-stripe'];
                
                // All other tabs are strictly Business/Enterprise/Admin
                // (tab-campaigns, tab-branches, tab-staff, tab-bank, tab-loyalty, tab-special-cards, tab-marketing, tab-copilot, tab-api, tab-mybusiness, tab-caja, tab-store)
                
                if (tab.classList.contains('admin-only-item')) {
                    tab.style.display = isAdmin ? 'flex' : 'none';
                    return;
                }
                
                if (baseTabs.includes(tabId)) {
                    tab.style.display = 'flex';
                } else if (proTabs.includes(tabId)) {
                    tab.style.display = isProfessional ? 'flex' : 'none';
                } else {
                    tab.style.display = isBusiness ? 'flex' : 'none';
                }
            });
        };"""
        
    new_func = """        window.checkPlanPermissions = function() {
            if (!window.merchantData) return;
            const plan = window.merchantData.business_type || 'starter';
            const isAdmin = window.merchantSession && window.merchantSession.user.email === 'hola@fideliorewards.com';
            
            const allNavTabs = document.querySelectorAll('.nav-tab');
            
            allNavTabs.forEach(tab => {
                const tabId = tab.getAttribute('data-tab');
                if (!tabId) return;
                
                if (tab.classList.contains('admin-only-item')) {
                    tab.style.display = isAdmin ? 'flex' : 'none';
                    return;
                }
                
                const baseTabs = ['tab-home', 'tab-metrics', 'tab-builder', 'tab-account', 'tab-support', 'tab-crm'];
                const proExclusiveTabs = ['tab-appointments', 'tab-stripe'];
                
                if (baseTabs.includes(tabId)) {
                    tab.style.display = 'flex';
                } else if (proExclusiveTabs.includes(tabId)) {
                    // Professional exclusives (Admin and Enterprise also get them)
                    tab.style.display = (plan === 'professional' || plan === 'enterprise' || isAdmin) ? 'flex' : 'none';
                } else {
                    // Business features (Admin and Enterprise also get them, but NOT professional)
                    tab.style.display = (plan === 'business' || plan === 'enterprise' || isAdmin) ? 'flex' : 'none';
                }
            });
        };"""
        
    content = content.replace(old_func, new_func)

    with open('dashboard.js', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    fix_dashboard_mutual_exclusion()
