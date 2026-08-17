import re

def refine_professional_tabs_add_metrics():
    with open('dashboard.js', 'r') as f:
        content = f.read()
                
    old_logic = "const proTabs = ['tab-home', 'tab-builder', 'tab-appointments', 'tab-stripe', 'tab-account', 'tab-support', 'tab-crm'];"
    new_logic = "const proTabs = ['tab-home', 'tab-builder', 'tab-appointments', 'tab-stripe', 'tab-account', 'tab-support', 'tab-crm', 'tab-metrics'];"
                
    content = content.replace(old_logic, new_logic)

    with open('dashboard.js', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    refine_professional_tabs_add_metrics()
