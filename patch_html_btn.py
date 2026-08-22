import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_btn = """                            <button onclick="setAdminPlanStatus('expired')" style="width: 100%; background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); padding: 12px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 8px;">
                                <i class="fa-solid fa-lock"></i> Bloquear Cuenta por Falta de Pago
                            </button>"""

new_btn = """                            <button onclick="setAdminPlanStatus('expired')" style="width: 100%; background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); padding: 12px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 8px;">
                                <i class="fa-solid fa-lock"></i> Bloquear Cuenta por Falta de Pago
                            </button>
                            <button onclick="if(confirm('¿Estás seguro de que deseas ELIMINAR permanentemente esta cuenta? Esta acción borrará al usuario de la base de datos de autenticación y cascadas de datos. NO SE PUEDE DESHACER.')) window.deleteAdminMerchant()" style="width: 100%; background: white; color: #ef4444; border: 1px solid #ef4444; padding: 12px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 24px;">
                                <i class="fa-solid fa-trash"></i> Eliminar Cuenta Permanentemente
                            </button>"""

if old_btn in html:
    html = html.replace(old_btn, new_btn)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html patched.")
else:
    print("Failed to patch index.html")

