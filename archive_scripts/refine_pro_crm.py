import re

def refine_professional_tabs_add_crm():
    with open('dashboard.js', 'r') as f:
        content = f.read()
                
    old_logic = "const proTabs = ['tab-home', 'tab-builder', 'tab-appointments', 'tab-stripe', 'tab-account', 'tab-support'];"
    new_logic = "const proTabs = ['tab-home', 'tab-builder', 'tab-appointments', 'tab-stripe', 'tab-account', 'tab-support', 'tab-crm'];"
                
    content = content.replace(old_logic, new_logic)

    with open('dashboard.js', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    refine_professional_tabs_add_crm()
