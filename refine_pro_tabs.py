import re

def refine_professional_tabs():
    with open('dashboard.js', 'r') as f:
        content = f.read()

    old_logic = """                const baseTabs = ['tab-home', 'tab-metrics', 'tab-builder', 'tab-account', 'tab-support', 'tab-crm'];
                const proExclusiveTabs = ['tab-appointments', 'tab-stripe'];
                
                if (baseTabs.includes(tabId)) {
                    tab.style.display = 'flex';
                } else if (proExclusiveTabs.includes(tabId)) {
                    // Professional exclusives (Admin and Enterprise also get them)
                    tab.style.display = (plan === 'professional' || plan === 'enterprise' || isAdmin) ? 'flex' : 'none';
                } else {
                    // Business features (Admin and Enterprise also get them, but NOT professional)
                    tab.style.display = (plan === 'business' || plan === 'enterprise' || isAdmin) ? 'flex' : 'none';
                }"""
                
    new_logic = """                const proTabs = ['tab-home', 'tab-builder', 'tab-appointments', 'tab-stripe', 'tab-account', 'tab-support'];
                const businessExcludes = ['tab-appointments', 'tab-stripe'];

                if (isAdmin || plan === 'enterprise') {
                    tab.style.display = 'flex';
                } else if (plan === 'professional') {
                    // Profesionistas solo ven: Dashboard(home), Sellos(builder), Citas, Pagos, Cuenta y Soporte.
                    tab.style.display = proTabs.includes(tabId) ? 'flex' : 'none';
                } else {
                    // Business (Restaurantes) ven todo EXCEPTO citas y pagos de Stripe
                    tab.style.display = businessExcludes.includes(tabId) ? 'none' : 'flex';
                }"""
                
    content = content.replace(old_logic, new_logic)

    with open('dashboard.js', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    refine_professional_tabs()
