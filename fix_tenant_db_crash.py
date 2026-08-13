import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Fix 1: loadDataFromSupabase branches initialization
js = js.replace("branches: tenantDatabase[merchantData.id]?.branches || [],", "branches: [],")

# Fix 2: activeMode
js = js.replace("tenantDatabase[currentTenantId].activeMode = mode;", "")

# Fix 3: branch save
js = js.replace("tenantDatabase[currentTenantId].branches = state.branches;", "")

# Fix 4: Logo upload
js = js.replace("tenantDatabase[currentTenantId].customLogoUrl = evt.target.result;", "")
js = js.replace("tenantDatabase[currentTenantId].customLogoUrl = null;", "")

# Fix 5: Banner upload
js = js.replace("tenantDatabase[currentTenantId].customBannerUrl = evt.target.result;", "")
js = js.replace("tenantDatabase[currentTenantId].customBannerUrl = null;", "")

with open('dashboard.js', 'w') as f:
    f.write(js)
