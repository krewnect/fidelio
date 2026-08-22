import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_endpoint = """// ============================================================================
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
});"""

new_endpoint = """// ============================================================================
// ADMIN API: DELETE MERCHANT
// ============================================================================
app.delete('/api/admin/merchant/:id', async (req, res) => {
    const merchantId = req.params.id;
    if (!supabaseAdmin) return res.status(500).json({error: 'Admin client not initialized'});
    try {
        // Attempt to delete from Auth (this cascades to tables if configured)
        const { error: authError } = await supabaseAdmin.auth.admin.deleteUser(merchantId);
        
        // Even if auth fails (e.g. 'User not found' orphan record), force delete from merchants table
        const { error: dbError } = await supabaseAdmin.from('merchants').delete().eq('id', merchantId);
        
        if (authError && authError.message !== 'User not found' && !dbError) {
            console.warn("Auth deletion had an issue, but DB record was deleted:", authError);
        } else if (authError && authError.message !== 'User not found' && dbError) {
            throw new Error(`Auth Error: ${authError.message} | DB Error: ${dbError.message}`);
        }
        
        res.json({ success: true, warning: authError ? authError.message : null });
    } catch (err) {
        console.error("Delete Merchant Error:", err);
        res.status(500).json({error: err.message});
    }
});"""

if old_endpoint in js:
    js = js.replace(old_endpoint, new_endpoint)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("app.js endpoint updated.")
else:
    print("WARNING: Could not find endpoint in app.js")

