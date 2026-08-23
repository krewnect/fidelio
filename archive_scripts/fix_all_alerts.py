import re

def replace_alerts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic replace for alert("...") or alert('...')
    # This regex handles single quotes, double quotes, and simple concatenations 
    # as long as they don't contain unescaped quotes matching the outer ones.
    
    # We will just write a custom replacer to be safe.
    # Instead of complex regex, I'll do specific replacements for the worst offenders.

    replacements = [
        ("alert(\"CRASH LOG DB (por favor muéstrale esto a tu asistente):\\n\" + err.stack);", 
         "console.error('DB Init Error:', err.stack); if(typeof showToast==='function') showToast('Error inicializando datos', 'error');"),
        
        ("alert(\"CRASH FATAL: Tu cuenta no tiene un perfil de negocio asignado en la base de datos y no pudo ser auto-creado. Por favor, crea una cuenta de prueba normal para probar las sucursales, no la cuenta Master Admin, o contacta a soporte.\");", 
         "console.error('CRASH FATAL: No tenant profile.'); if(typeof showToast==='function') showToast('Error crítico: Cuenta sin perfil de negocio. Contacta a soporte.', 'error');"),
        
        ("onclick=\"alert('Funcionalidad de contacto próximamente')\"",
         "onclick=\"if(typeof showToast==='function') showToast('La funcionalidad de contacto directo llegará pronto', 'info');\""),
         
        ("alert('¡LA VARIABLE TENANT ID ESTÁ NULA AL HACER CLIC!');",
         "if(typeof showToast==='function') showToast('Error interno: No se pudo identificar tu cuenta', 'error');"),
         
        ("alert(\"Error en DB: \" + error.message);",
         "if(typeof showToast==='function') showToast('Error de conexión: ' + error.message, 'error');"),
         
        ("alert(\"Crash inline DB: \" + ex.message);",
         "if(typeof showToast==='function') showToast('Error procesando solicitud: ' + ex.message, 'error');"),
         
        ("alert('Nombre y teléfono son obligatorios.');",
         "if(typeof showToast==='function') showToast('Nombre y teléfono son obligatorios', 'warning');"),
         
        ("alert('Error registrando cliente: ' + err.message);",
         "if(typeof showToast==='function') showToast('Error registrando cliente: ' + err.message, 'error');"),
         
        ("alert(\"Error: \" + err.message);",
         "if(typeof showToast==='function') showToast('Error: ' + err.message, 'error');"),
         
        ("alert('El cliente no tiene un teléfono registrado.')",
         "if(typeof showToast==='function') showToast('El cliente no tiene un teléfono registrado', 'warning')"),
         
        ("alert('El cliente no tiene un correo registrado.')",
         "if(typeof showToast==='function') showToast('El cliente no tiene un correo registrado', 'warning')"),
         
        ("alert('El envío de notificaciones directas requiere un add-on adicional.');",
         "if(typeof showToast==='function') showToast('El envío de notificaciones requiere un add-on adicional', 'info');"),
         
        ("alert('Funcionalidad de revocación disponible al conectar backend')",
         "if(typeof showToast==='function') showToast('Función de revocación próxima a liberarse', 'info')"),
         
        ("alert('Funcionalidad de correo automatizado para cobranza pendiente de conectar al CRM.');",
         "if(typeof showToast==='function') showToast('Correo automatizado llegará en la próxima versión', 'info');"),
         
        ("alert(\"Atención (Fidelio Debug): Estás intentando entrar como Super Admin, pero tu correo en base de datos es exactamente: '\" + currentEmail + \"'. Hay un error de escritura o un espacio extra que impide que te reconozca como 'hola@fideliorewards.com'.\");",
         "console.error('Auth Mismatch', currentEmail); if(typeof showToast==='function') showToast('No autorizado como Administrador Maestro', 'error');"),
         
        ("alert(\"CRASH LOG UI (por favor muéstrale esto a tu asistente):\\n\" + err.stack);",
         "console.error('UI Build Error:', err.stack);"),
         
        ("alert('Por favor completa todos los campos.');",
         "if(typeof showToast==='function') showToast('Por favor completa todos los campos', 'warning');"),
         
        ("alert('ACCESO DENEGADO: Solo la cuenta Master Admin puede crear otros usuarios de Acceso Sistema.');",
         "if(typeof showToast==='function') showToast('Acceso denegado: Se requieren permisos de Máster Admin', 'error');"),
         
        ("alert('¡Invitación enviada y usuario ' + role + ' registrado exitosamente!');",
         "if(typeof showToast==='function') showToast('Usuario ' + role + ' registrado exitosamente', 'success');"),
         
        ("alert(\"Por favor, ponle un nombre a tu filtro personalizado.\");",
         "if(typeof showToast==='function') showToast('Por favor, ponle un nombre a tu filtro', 'warning');"),
         
        ("alert(\"Error interno: No se pudo identificar tu cuenta (tenantId). Por favor recarga la página.\");",
         "if(typeof showToast==='function') showToast('Error: No se pudo identificar tu cuenta. Recarga la página.', 'error');"),
         
        ("alert(\"Error en la nube: \" + error.message);",
         "if(typeof showToast==='function') showToast('Error en la nube: ' + error.message, 'error');"),
         
        ("alert(\"Error de permisos: No tienes autorización para modificar este negocio. Tu sesión puede haber expirado.\");",
         "if(typeof showToast==='function') showToast('Error de permisos. Tu sesión pudo haber expirado.', 'error');"),
         
        ("alert(\"Error rendering summary: \" + sumErr.message);",
         "console.error('Summary error:', sumErr);"),
         
        ("alert(\"CRASH AL GUARDAR HORARIOS: \" + err.message);",
         "if(typeof showToast==='function') showToast('Error al guardar horarios: ' + err.message, 'error');"),
         
        ("alert(\"Por favor ingresa un concepto y monto válido.\");",
         "if(typeof showToast==='function') showToast('Ingresa un concepto y monto válido', 'warning');"),

        ("onclick=\"alert('Exportación CSV/Excel se activará en la próxima actualización de backend')\"",
         "onclick=\"if(typeof showToast==='function') showToast('La exportación Excel se habilitará pronto', 'info');\""),
         
        ("onclick=\"alert('Funcionalidad de múltiples reglas en desarrollo.')\"",
         "onclick=\"if(typeof showToast==='function') showToast('Las reglas compuestas llegarán pronto', 'info');\""),
         
        ("onclick=\"alert('Guardado')\"",
         "onclick=\"if(typeof showToast==='function') showToast('Cambios guardados', 'success');\""),
         
        # Index error
        ("alert(\"Error crítico: No se encontró la sesión al cargar el Dashboard. Esto puede ser por un bloqueo de cookies en tu navegador o caché viejo. Redirigiendo al inicio...\");",
         "console.error('Session not found, redirecting.');")
    ]

    for target, rep in replacements:
        content = content.replace(target, rep)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

replace_alerts('dashboard_v2.js')
replace_alerts('index.html')

