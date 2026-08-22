import re

# 1. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

delete_endpoint = """
// ============================================================================
// ADMIN API: DELETE MERCHANT
// ============================================================================
app.delete('/api/admin/merchant/:id', async (req, res) => {
    const merchantId = req.params.id;
    if (!supabaseAdmin) return res.status(500).json({error: 'Admin client not initialized'});
    try {
        const { error } = await supabaseAdmin.auth.admin.deleteUser(merchantId);
        if (error) throw error;
        res.json({ success: true });
    } catch (err) {
        console.error(err);
        res.status(500).json({error: err.message});
    }
});
"""

anchor = "// TRIGGER MARKETING PUSH API"
if anchor in js:
    js = js.replace(anchor, delete_endpoint + "\n" + anchor)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("app.js patched with DELETE endpoint.")
else:
    print("WARNING: Could not find anchor in app.js")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

btn_html = """
                    <div style="background: var(--bg-main); border: 1px solid var(--border-soft); border-radius: 16px; padding: 24px;">
                        <h3 style="font-size: 14px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px;"><i class="fa-solid fa-credit-card"></i> Gestión de Facturación</h3>
                        
                        <div style="margin-bottom: 16px;">
                            <label class="premium-label" style="display: block; margin-bottom: 8px;">Precio Personalizado (Mensualidad)</label>
                            <div style="display: flex; gap: 12px; align-items: center;">
                                <div style="position: relative; flex: 1;">
                                    <span style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-muted);">$</span>
                                    <input type="number" id="admin-custom-price" class="fidelio-input" placeholder="Ej. 1500" style="padding-left: 28px;">
                                </div>
                                <div style="position: relative; flex: 1;">
                                    <input type="number" id="admin-custom-price-months" class="fidelio-input" placeholder="Meses de vigencia (opcional)">
                                </div>
                                <button onclick="saveAdminCustomPrice()" class="fidelio-btn-primary" style="padding: 10px 16px; border-radius: 8px;"><i class="fa-solid fa-save"></i></button>
                            </div>
                            <div id="admin-custom-price-expiry-label" style="font-size: 11px; color: #f59e0b; font-weight: 700; margin-top: 6px;"></div>
                            <p style="font-size: 12px; color: var(--text-muted); margin-top: 8px; line-height: 1.4;">Este precio sobrescribe el plan estándar. Si lo dejas en blanco, se cobrará la tarifa regular de $999 MXN. Si indicas meses de vigencia, cambiará a precio normal automáticamente al terminar el periodo.</p>
                        </div>
                    </div>
                    
                    <button class="fidelio-btn-secondary" style="border-color: #ef4444; color: #ef4444; width: 100%; margin-top: 8px;" onclick="if(confirm('¿Estás seguro de que deseas ELIMINAR permanentemente esta cuenta? Esta acción no se puede deshacer y borrará toda la información del negocio, clientes y tarjetas.')) window.deleteAdminMerchant()">
                        <i class="fa-solid fa-trash"></i> Eliminar Cuenta Permanentemente
                    </button>
"""

anchor_html = """
                    <div style="background: var(--bg-main); border: 1px solid var(--border-soft); border-radius: 16px; padding: 24px;">
                        <h3 style="font-size: 14px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px;"><i class="fa-solid fa-credit-card"></i> Gestión de Facturación</h3>
                        
                        <div style="margin-bottom: 16px;">
                            <label class="premium-label" style="display: block; margin-bottom: 8px;">Precio Personalizado (Mensualidad)</label>
                            <div style="display: flex; gap: 12px; align-items: center;">
                                <div style="position: relative; flex: 1;">
                                    <span style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--text-muted);">$</span>
                                    <input type="number" id="admin-custom-price" class="fidelio-input" placeholder="Ej. 1500" style="padding-left: 28px;">
                                </div>
                                <div style="position: relative; flex: 1;">
                                    <input type="number" id="admin-custom-price-months" class="fidelio-input" placeholder="Meses de vigencia (opcional)">
                                </div>
                                <button onclick="saveAdminCustomPrice()" class="fidelio-btn-primary" style="padding: 10px 16px; border-radius: 8px;"><i class="fa-solid fa-save"></i></button>
                            </div>
                            <div id="admin-custom-price-expiry-label" style="font-size: 11px; color: #f59e0b; font-weight: 700; margin-top: 6px;"></div>
                            <p style="font-size: 12px; color: var(--text-muted); margin-top: 8px; line-height: 1.4;">Este precio sobrescribe el plan estándar. Si lo dejas en blanco, se cobrará la tarifa regular de $999 MXN. Si indicas meses de vigencia, cambiará a precio normal automáticamente al terminar el periodo.</p>
                        </div>
                    </div>
"""

if anchor_html in html:
    html = html.replace(anchor_html, btn_html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html patched with DELETE button.")
else:
    print("WARNING: Could not find anchor in index.html")

# 3. Update dashboard_v2.js
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

delete_func = """
    window.deleteAdminMerchant = async function() {
        if (window.fidelioAdminRole !== 'admin' && window.fidelioAdminRole !== 'super_admin') return;
        const id = document.getElementById('admin-current-merchant-id').value;
        if(!id) return;
        
        try {
            window.showToast("Eliminando cuenta...", "info");
            const res = await fetch('https://fidelio-41j9.onrender.com/api/admin/merchant/' + id, {
                method: 'DELETE'
            });
            
            if(!res.ok) {
                const errData = await res.json().catch(()=>({}));
                throw new Error(errData.error || 'Error del servidor');
            }
            
            window.showToast("Cuenta eliminada permanentemente", "success");
            document.getElementById('modal-admin-merchant').style.display = 'none';
            // Refrescar lista de negocios
            if(typeof window.loadFidelioTeam === 'function') {
                window.loadFidelioTeam();
            }
        } catch(e) {
            console.error(e);
            window.showToast("Error al eliminar la cuenta: " + e.message, "error");
        }
    };
"""

js_anchor = "window.saveAdminCustomPrice = async function() {"
if js_anchor in js:
    js = js.replace(js_anchor, delete_func + "\n    " + js_anchor)
    with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("dashboard_v2.js patched with deleteAdminMerchant.")
else:
    print("WARNING: Could not find anchor in dashboard_v2.js")

