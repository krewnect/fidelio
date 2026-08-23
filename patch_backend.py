import re

with open('app.js', 'r') as f:
    content = f.read()

# 1. Update Staff Creation
old_staff = """app.post('/api/auth/staff/create', apiLimiter, requireMerchantAuth, async (req, res) => {
    const { email, password, name } = req.body;
    
    if (req.userRole !== 'admin') {
        return res.status(403).json({ error: 'Solo el dueño puede crear cajeros.' });
    }
    if (!supabaseAdmin) {
        return res.status(500).json({ error: 'Supabase Admin no configurado (Falta SERVICE_ROLE_KEY).' });
    }

    try {
        // 1. Crear el usuario con la API Admin para no cerrar la sesión del dueño
        const { data: staffAuth, error: authError } = await supabaseAdmin.auth.admin.createUser({
            email: email,
            password: password,
            email_confirm: true,
            user_metadata: {
                role: 'staff',
                merchant_id: req.merchantId,
                name: name
            }
        });

        if (authError) throw authError;

        // 2. Registrar al cajero en la tabla 'staff' para que el dueño lo vea en la lista
        const { error: dbError } = await supabaseAdmin
            .from('staff')
            .insert([{ 
                id: staffAuth.user.id, 
                merchant_id: req.merchantId, 
                email: email,
                name: name
            }]);
            
        if (dbError) throw dbError;

        res.json({ success: true, user: staffAuth.user });
    } catch (error) {
        console.error("Staff Create Error:", error);
        res.status(400).json({ error: error.message });
    }
});"""

new_staff = """app.post('/api/auth/staff/create', apiLimiter, requireMerchantAuth, async (req, res) => {
    // RBAC: Extraemos los nuevos campos (role_level, branch_id, custom_permissions)
    const { email, password, name, role_level = 'cashier', branch_id = null, custom_permissions = {} } = req.body;
    
    // Solo el dueño (admin) o un 'master' puede crear staff
    if (req.userRole !== 'admin' && req.userRoleLevel !== 'master') {
        return res.status(403).json({ error: 'Permisos insuficientes para crear usuarios.' });
    }
    if (!supabaseAdmin) {
        return res.status(500).json({ error: 'Supabase Admin no configurado (Falta SERVICE_ROLE_KEY).' });
    }

    try {
        // 1. Crear el usuario con la API Admin para no cerrar la sesión del dueño
        const { data: staffAuth, error: authError } = await supabaseAdmin.auth.admin.createUser({
            email: email,
            password: password,
            email_confirm: true,
            user_metadata: {
                role: 'staff',
                role_level: role_level,
                merchant_id: req.merchantId,
                branch_id: branch_id,
                custom_permissions: custom_permissions,
                name: name
            }
        });

        if (authError) throw authError;

        // 2. Registrar al cajero en la tabla 'staff' con la nueva jerarquía corporativa
        const { error: dbError } = await supabaseAdmin
            .from('staff')
            .insert([{ 
                id: staffAuth.user.id, 
                merchant_id: req.merchantId, 
                branch_id: branch_id,
                email: email,
                name: name,
                role_level: role_level,
                permissions: custom_permissions
            }]);
            
        if (dbError) throw dbError;

        res.json({ success: true, user: staffAuth.user });
    } catch (error) {
        console.error("Staff Create Error:", error);
        res.status(400).json({ error: error.message });
    }
});

// --- B2B ENTERPRISE API: BRANCHES & FRANCHISES ---
app.post('/api/merchant/branches', requireMerchantAuth, async (req, res) => {
    if (req.userRole !== 'admin' && req.userRoleLevel !== 'master') return res.status(403).json({ error: 'No autorizado' });
    const { name, address, lat, lng, radius, customMessage } = req.body;
    try {
        const { data, error } = await supabase
            .from('branches')
            .insert([{ merchant_id: req.merchantId, name, address, lat, lng, radius, custom_message: customMessage }])
            .select();
        if (error) throw error;
        res.json({ success: true, branch: data[0] });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.get('/api/merchant/branches', requireMerchantAuth, async (req, res) => {
    try {
        let query = supabase.from('branches').select('*').eq('merchant_id', req.merchantId);
        // RBAC: Manager can only see their own branch
        if (req.userRole === 'staff' && req.userRoleLevel === 'manager' && req.userBranchId) {
            query = query.eq('id', req.userBranchId);
        }
        const { data, error } = await query;
        if (error) throw error;
        res.json({ success: true, branches: data });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});"""

content = content.replace(old_staff, new_staff)

# 2. Update Auth Middleware to extract role_level and branch_id
old_middleware = """    if (user.user_metadata && user.user_metadata.role === 'staff') {
        req.merchantId = user.user_metadata.merchant_id;
        req.userRole = 'staff';
    } else {
        req.merchantId = user.id;
        req.userRole = 'admin';
    }"""
    
new_middleware = """    if (user.user_metadata && user.user_metadata.role === 'staff') {
        req.merchantId = user.user_metadata.merchant_id;
        req.userRole = 'staff';
        req.userRoleLevel = user.user_metadata.role_level || 'cashier';
        req.userBranchId = user.user_metadata.branch_id || null;
        req.userPermissions = user.user_metadata.custom_permissions || {};
    } else {
        req.merchantId = user.id;
        req.userRole = 'admin';
        req.userRoleLevel = 'master'; // Owner has master privileges
        req.userBranchId = null; // Owner sees all branches
    }"""
    
content = content.replace(old_middleware, new_middleware)

with open('app.js', 'w') as f:
    f.write(content)
print("Backend patched successfully")
