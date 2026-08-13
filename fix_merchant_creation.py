import re

with open('dashboard.js', 'r') as f:
    js = f.read()

old_load = """        if (error) {
            console.error("Error cargando perfil:", error);
            showToast("Error al cargar configuración", "warning");
            return false;
        }"""

new_load = """        if (error) {
            console.log("El perfil del merchant no existe. Creando perfil por defecto...");
            
            // Auto-create merchant profile if it doesn't exist
            const { data: newMerchant, error: insertError } = await window.supabaseClient
                .from('merchants')
                .insert([{
                    id: merchantId,
                    business_name: "Mi Negocio",
                    industry: "restaurant",
                    color_primary: "#090d16",
                    color_accent: "#5b0eb8",
                    cashback_percent: 5,
                    stamps_total: 10,
                    stamps_reward_text: "Recompensa Gratis",
                    branches: []
                }])
                .select('*')
                .single();
                
            if (insertError) {
                console.error("No se pudo auto-crear el merchant:", insertError);
                alert("CRASH FATAL: Tu cuenta no tiene un perfil de negocio asignado en la base de datos y no pudo ser auto-creado. Por favor, crea una cuenta de prueba normal para probar las sucursales, no la cuenta Master Admin, o contacta a soporte.");
                return false;
            }
            merchantData = newMerchant;
        }"""

js = js.replace(old_load, new_load)

# Because we are replacing merchantData, we need to make it 'let' instead of 'const'
js = js.replace(
    "const { data: merchantData, error } = await window.supabaseClient",
    "let { data: merchantData, error } = await window.supabaseClient"
)

with open('dashboard.js', 'w') as f:
    f.write(js)
