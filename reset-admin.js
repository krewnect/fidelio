require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabaseAdmin = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_ROLE_KEY
);

async function resetAdmin() {
    console.log('Buscando usuarios...');
    const { data: { users }, error } = await supabaseAdmin.auth.admin.listUsers();
    
    if (error) {
        console.error('Error listando usuarios:', error);
        return;
    }

    const adminUser = users.find(u => u.email.includes('admin') || u.email.includes('roberto'));
    
    if (!adminUser) {
        console.log('No se encontró usuario admin. Correos encontrados:');
        users.forEach(u => console.log(u.email));
        return;
    }

    console.log(`Encontrado admin: ${adminUser.email}. Reseteando contraseña a "Admin123456!"`);
    
    const { data, error: updateError } = await supabaseAdmin.auth.admin.updateUserById(
        adminUser.id,
        { 
            password: 'Admin123456!',
            email_confirm: true
        }
    );

    if (updateError) {
        console.error('Error actualizando:', updateError);
    } else {
        console.log('Contraseña actualizada con éxito.');
        
        // Ensure it's in merchants table
        const { data: merchantData, error: dbError } = await supabaseAdmin
            .from('merchants')
            .upsert([
                { id: adminUser.id, business_name: 'Super Admin', plan_status: 'active' }
            ]);
            
        if (dbError) {
            console.error('Error inyectando a merchants:', dbError);
        } else {
            console.log('Inyectado correctamente a la tabla merchants.');
        }
    }
}

resetAdmin();
