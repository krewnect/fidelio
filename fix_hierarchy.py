import re

def fix_dashboard_permissions():
    with open('dashboard.js', 'r') as f:
        content = f.read()

    # Rewrite window.checkPlanPermissions
    old_func = """        window.checkPlanPermissions = function() {
            if (!window.merchantData) return;
            const plan = window.merchantData.business_type || 'starter';
            const isAdmin = window.merchantSession && window.merchantSession.user.email === 'hola@fideliorewards.com';
            
            const isBusiness = plan === 'business' || plan === 'professional' || plan === 'enterprise' || isAdmin;
            const isPro = plan === 'professional' || plan === 'enterprise' || isAdmin;
            
            // Toggle Business-only tabs
            document.querySelectorAll('.plan-business-only').forEach(el => {
                if(isBusiness) {
                    el.style.display = 'flex';
                } else {
                    el.style.display = 'none';
                }
            });
            
            // Toggle Pro-only tabs
            document.querySelectorAll('.plan-pro-only').forEach(el => {
                if(isPro) {
                    el.style.display = 'flex';
                } else {
                    el.style.display = 'none';
                }
            });
            
            // Si es profesional, escondemos lo exclusivo de Business
            if (merchantData.business_type === 'professional') {
                const businessOnly = document.querySelectorAll('.business-exclusive');
                businessOnly.forEach(el => el.style.display = 'none');
            }
        };"""
        
    new_func = """        window.checkPlanPermissions = function() {
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
        
    content = content.replace(old_func, new_func)
    
    # Fix Stripe check (line 196)
    content = content.replace(
        "if (window.merchantData && (window.merchantData.business_type === 'professional' || window.merchantData.business_type === 'enterprise')) {",
        "if (window.merchantData && (window.merchantData.business_type === 'professional' || window.merchantData.business_type === 'business' || window.merchantData.business_type === 'enterprise')) {"
    )
    
    # Fix Copilot logic (line 5263)
    content = content.replace(
        "if (plan !== 'professional' && plan !== 'enterprise' && !isAdmin) {",
        "if (plan !== 'business' && plan !== 'enterprise' && !isAdmin) {"
    )
    content = content.replace(
        "El Copiloto AI es exclusivo del Plan Profesional",
        "El Copiloto AI es exclusivo del Plan Business"
    )

    with open('dashboard.js', 'w') as f:
        f.write(content)

def fix_index():
    with open('index.html', 'r') as f:
        content = f.read()
        
    # Replace the "Upgrade a Pro" banner logic
    content = content.replace(
        "Hacer Upgrade a Pro",
        "Hacer Upgrade a Business"
    )
    
    with open('index.html', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    fix_dashboard_permissions()
    fix_index()
