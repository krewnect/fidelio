import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

endpoint = """
// ============================================================================
// ADMIN API: GET MERCHANT AUTH DETAILS
// ============================================================================
app.get('/api/admin/merchant-details/:id', async (req, res) => {
    const merchantId = req.params.id;
    if (!supabaseAdmin) return res.status(500).json({error: 'Admin client not initialized'});
    try {
        const { data: { user }, error } = await supabaseAdmin.auth.admin.getUserById(merchantId);
        if (error || !user) return res.status(404).json({error: 'Not found'});
        res.json({
            email: user.email,
            first_name: user.user_metadata?.first_name || '',
            last_name: user.user_metadata?.last_name || '',
            phone: user.phone || ''
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({error: err.message});
    }
});
"""

if "// ============================================================================" in js:
    # Just append it before the trigger push API
    anchor = "// TRIGGER MARKETING PUSH API"
    if anchor in js:
        js = js.replace(anchor, endpoint + "\n// ============================================================================\n" + anchor)
        
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("app.js patched.")
