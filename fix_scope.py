import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace checkMasterAdmin() calls in the injected functions with explicit role checks
# We only want to replace it in the specific functions we added, or globally since checkMasterAdmin is throwing an error for them anyway.

new_check = "if (window.fidelioAdminRole !== 'admin' && window.fidelioAdminRole !== 'super_admin') return;"

# Because the functions I injected all start with `if (!checkMasterAdmin()) return;`, I can just string replace it globally in my injected blocks.
js = js.replace('if (!checkMasterAdmin()) return;', new_check)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Scope issue fixed. checkMasterAdmin replaced with explicit role checks in global scope.")
