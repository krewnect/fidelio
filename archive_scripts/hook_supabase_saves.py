import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# 1. Add saveDesignToSupabase to btn-submit-branch click
js = js.replace(
    "state.branches.push(newBranch);\n            \n            if (addModal)",
    "state.branches.push(newBranch);\n            saveDesignToSupabase();\n            \n            if (addModal)"
)

# 2. Add saveDesignToSupabase to removeBranch
js = js.replace(
    "tenantDatabase[currentTenantId].branches = state.branches;",
    "// tenantDatabase logic removed\n            saveDesignToSupabase();"
)
# Wait, did I already remove tenantDatabase from removeBranch?
# Let's check how removeBranch looks now.
