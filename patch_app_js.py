import sys

def patch_app_js():
    with open('app.js', 'r') as f:
        content = f.read()

    # Add requireProPlan middleware after requireMerchantAuth
    middleware_code = """
const requireProPlan = async (req, res, next) => {
    try {
        const { data: merchant, error } = await supabase
            .from('merchants')
            .select('business_type')
            .eq('id', req.merchantId)
            .single();
            
        if (error || !merchant) return res.status(404).json({ success: false, error: 'Merchant not found' });
        
        // Admin overrides
        if (req.userRole === 'admin' && req.merchantId === 'hola@fideliorewards.com') return next(); // Fallback if using email
        
        const plan = merchant.business_type || 'starter';
        if (plan === 'professional' || plan === 'enterprise') {
            next();
        } else {
            return res.status(403).json({ success: false, error: 'Upgrade to Professional to access this feature.' });
        }
    } catch (e) {
        return res.status(500).json({ success: false, error: 'Internal validation error' });
    }
};
"""
    if "const requireProPlan" not in content:
        content = content.replace('const apiLimiter', middleware_code + '\nconst apiLimiter')

    # Fix negative amount in transaction
    transaction_check = """
    if (!customerId || !amount || amount <= 0 || !['earn', 'redeem'].includes(type)) {
        return res.status(400).json({ success: false, error: 'Datos inválidos' });
    }
"""
    # Verify if it already exists, actually we saw it in app.js: "if (!customerId || !amount || amount <= 0 || !['earn', 'redeem'].includes(type))" 
    # Yes, it is already there! But let's add an extra safety check for amount just in case it's not a number.
    safe_transaction_check = """
    amount = parseFloat(amount);
    if (!customerId || isNaN(amount) || amount <= 0 || !['earn', 'redeem'].includes(type)) {
        return res.status(400).json({ success: false, error: 'Datos inválidos' });
    }
"""
    content = content.replace("    if (!customerId || !amount || amount <= 0 || !['earn', 'redeem'].includes(type)) {\n        return res.status(400).json({ success: false, error: 'Datos inválidos' });\n    }", safe_transaction_check)

    with open('app.js', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    patch_app_js()
