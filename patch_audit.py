import re

with open('app.js', 'r') as f:
    content = f.read()

# 1. Update Auth Middleware to include userId
old_middleware = """        req.userPermissions = user.user_metadata.custom_permissions || {};
    } else {
        req.merchantId = user.id;
        req.userRole = 'admin';"""

new_middleware = """        req.userPermissions = user.user_metadata.custom_permissions || {};
        req.userId = user.id;
    } else {
        req.merchantId = user.id;
        req.userRole = 'admin';
        req.userId = user.id;"""
content = content.replace(old_middleware, new_middleware)

# 2. Update Scanner Transaction
old_scanner = """        // Registrar Transacción
        await supabase
            .from('transactions')
            .insert([{
                merchant_id: req.merchantId,
                customer_id: customerId,
                amount: amount,
                type: type
            }]);"""
            
new_scanner = """        // Registrar Transacción con Auditoría de Seguridad (B2B Audit Log)
        await supabase
            .from('transactions')
            .insert([{
                merchant_id: req.merchantId,
                customer_id: customerId,
                amount: amount,
                type: type,
                staff_id: req.userRole === 'staff' ? req.userId : null,
                branch_id: req.userBranchId || null
            }]);"""
content = content.replace(old_scanner, new_scanner)

# 3. Add Audit Logs API Endpoint
audit_api = """
// --- B2B AUDIT LOGS API ---
app.get('/api/merchant/audit-logs', requireMerchantAuth, async (req, res) => {
    // Solo Master Admin y Managers pueden ver logs
    if (req.userRole !== 'admin' && req.userRoleLevel === 'cashier') {
        return res.status(403).json({ error: 'Acceso denegado a auditoría' });
    }
    
    try {
        let query = supabase
            .from('transactions')
            .select(`
                *,
                customers ( name, email ),
                staff ( name, email )
            `)
            .eq('merchant_id', req.merchantId)
            .order('created_at', { ascending: false })
            .limit(100);
            
        // Si es manager, solo ve las transacciones de su sucursal
        if (req.userRoleLevel === 'manager' && req.userBranchId) {
            query = query.eq('branch_id', req.userBranchId);
        }
        
        const { data, error } = await query;
        if (error) throw error;
        
        res.json({ success: true, logs: data });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});
"""

# Insert before Checkout con Stripe
content = content.replace("// Checkout con Stripe", audit_api + "\n// Checkout con Stripe")

with open('app.js', 'w') as f:
    f.write(content)
print("Audit backend patched successfully")
