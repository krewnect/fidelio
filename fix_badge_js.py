import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace all simple textContent assignments to header-business-category with the innerHTML version
def replace_category(match):
    prefix = match.group(1)
    return prefix + "innerHTML = `<span style='display:flex; align-items:center; gap:6px;'><span>${bCatDisp || 'Profesional'}</span> <span style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 2px 6px; border-radius: 8px; font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 0 10px rgba(245,158,11,0.4); animation: pulseGlow 2s infinite;'>Lv. 1 Maestro</span></span>`;"

# Just do a blanket replacement for the loadDataFromSupabase part since that's the main one on load
target = "document.getElementById('header-business-category').textContent = bCatDisp;"
replacement = "document.getElementById('header-business-category').innerHTML = `<span style='display:flex; align-items:center; gap:6px;'><span>${bCatDisp}</span> <span style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 2px 6px; border-radius: 8px; font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 0 10px rgba(245,158,11,0.4); animation: pulseGlow 2s infinite;'>Lv. 1 Maestro</span></span>`;"

js = js.replace(target, replacement)

# Fix the fallback role assignment
target_role = "sbRole.textContent = data.role;"
replacement_role = "sbRole.innerHTML = `<span style='display:flex; align-items:center; gap:6px;'><span>${data.role}</span> <span style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 2px 6px; border-radius: 8px; font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 0 10px rgba(245,158,11,0.4); animation: pulseGlow 2s infinite;'>Lv. 1</span></span>`;"

js = js.replace(target_role, replacement_role)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
