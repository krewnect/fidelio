import re

with open('dashboard.js', 'r') as f:
    js = f.read()

# Expose saveDesignToSupabase
js = js.replace(
    "async function saveDesignToSupabase() {",
    "window.saveDesignToSupabase = async function saveDesignToSupabase() {"
)

# In the submit branch listener, call window.saveDesignToSupabase()
js = js.replace(
    "state.branches.push(newBranch);",
    "state.branches.push(newBranch);\n            if (window.saveDesignToSupabase) window.saveDesignToSupabase();"
)

# In removeBranch, call window.saveDesignToSupabase()
js = js.replace(
    "renderBranches();\n            showToast(\"Sucursal eliminada",
    "renderBranches();\n            if (window.saveDesignToSupabase) window.saveDesignToSupabase();\n            showToast(\"Sucursal eliminada"
)

# In the main push button, also call it just in case!
js = js.replace(
    "btnConfirmPush.addEventListener('click', () => {",
    "btnConfirmPush.addEventListener('click', () => {\n            if (window.saveDesignToSupabase) window.saveDesignToSupabase();"
)


with open('dashboard.js', 'w') as f:
    f.write(js)
