import re

with open('dashboard_v3.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_logic = """            // Toggle Business-only tabs
            document.querySelectorAll('.plan-business-only').forEach(el => {
                if(isBusiness) {
                    el.style.display = '';
                } else {
                    el.style.display = 'none';
                }
            });"""

new_logic = """            // Toggle Business-only tabs
            console.log("checkPlanPermissions evaluating...", { plan, isBusiness, isAdmin, email: window.merchantSession?.user?.email });
            document.querySelectorAll('.plan-business-only').forEach(el => {
                if(isBusiness) {
                    // Restore optimal layout depending on element type
                    if (el.classList.contains('role-card') || el.classList.contains('nav-tab') || el.tagName.toLowerCase() === 'label') {
                        el.style.display = 'flex';
                    } else if (el.classList.contains('content-panel')) {
                        el.style.display = 'block';
                    } else {
                        el.style.display = '';
                    }
                } else {
                    el.style.display = 'none';
                }
            });"""

if old_logic in js:
    js = js.replace(old_logic, new_logic)
    with open('dashboard_v3.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched dashboard_v3.js successfully.")
else:
    print("Could not find the exact old_logic string.")

