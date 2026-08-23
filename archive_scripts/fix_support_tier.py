with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add plan-business-only class to the appropriate tutorial cards
cards_to_hide = [
    "Cómo usar Campañas Push",
    "Los 8 Programas (Cupones)",
    "Uso del Inbox de Soporte",
    "Niveles y Logros",
    "Programa de Referidos"
]

for card_title in cards_to_hide:
    # Find the specific content-panel div that contains this title
    # We will just replace 'class="content-panel"' with 'class="content-panel plan-business-only"' for the blocks that contain these strings
    import re
    # Match the content-panel div and everything until the title
    pattern = r'(<div class="content-panel" style="[^"]*"[^>]*onclick="[^"]*"[^>]*>[\s\S]*?<h4[^>]*>' + re.escape(card_title) + r'</h4>)'
    
    def replacer(match):
        return match.group(1).replace('class="content-panel"', 'class="content-panel plan-business-only"')
        
    html = re.sub(pattern, replacer, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update the Gemini mock logic
target = """        if (text.includes('escaner') || text.includes('escáner') || text.includes('premium')) {
            reply = "<strong>Escáner Premium y PoS:</strong><br><br>Para usar el escáner, ve a la opción 'Escáner Staff' en el menú principal izquierdo. Esta herramienta te permite:<br>1. Leer códigos QR de clientes<br>2. Registrar visitas y compras<br>3. Entregar premios automáticamente.<br><br>Recuerda que cada escáner de tu cuenta solo funciona con tus propias campañas para garantizar máxima seguridad.";
        } else if (text.includes('nivel') || text.includes('logro') || text.includes('vip')) {
            reply = "<strong>Niveles y Logros:</strong><br><br>Los niveles VIP automáticos permiten que tus clientes suban de categoría (por ejemplo: Bronce, Plata, Oro) basándose en su gasto total. Configúralos en la pestaña 'Mi Cuenta' encendiendo el apagador de 'Niveles VIP Automáticos'. Los clientes VIP suelen tener un ticket promedio un 20% más alto.";
        } else if (text.includes('referido') || text.includes('invitar')) {
            reply = "<strong>Programa de Referidos:</strong><br><br>El sistema de referidos motiva a tus clientes a traer a sus amigos. Puedes asignar puntos o premios extra a cualquier cliente que comparta su código único. Esta función se activa desde la configuración de la campaña en 'Mis Campañas'.";
        } else if (text.includes('inbox') || text.includes('zendesk') || text.includes('admin')) {
            reply = "<strong>Inbox de Soporte:</strong><br><br>Si cuentas con permisos de Administrador Central, podrás visualizar el Inbox de Soporte en tu menú. Ahí llegarán todos los tickets levantados por las sucursales o franquicias, y podrás responderles como un centro de ayuda.";
        } else if (text.includes('hola') || text.includes('ayuda')) {
            reply = "¡Hola! Estoy listo para apoyarte. Pregúntame sobre el Escáner, los Niveles VIP, el sistema de Referidos o cómo usar el Inbox de soporte.";
        }"""

replacement = """        const isBusiness = window.merchantData && window.merchantData.tier === 'business';
        
        if (text.includes('escaner') || text.includes('escáner') || text.includes('premium')) {
            reply = "<strong>Escáner Premium:</strong><br><br>Para usar el escáner, ve a la opción 'Escáner Staff' en el menú principal izquierdo. Esta herramienta te permite:<br>1. Leer códigos QR de clientes<br>2. Registrar citas o visitas<br>3. Entregar sellos automáticamente.<br><br>Recuerda que cada escáner de tu cuenta solo funciona con tus propias campañas para garantizar máxima seguridad.";
        } else if (text.includes('nivel') || text.includes('logro') || text.includes('vip') || text.includes('cashback') || text.includes('referido') || text.includes('push') || text.includes('inbox')) {
            if (!isBusiness) {
                reply = "<strong>Función Exclusiva:</strong><br><br>Esa función (Campañas Push, Niveles VIP, Cashback, Inbox Central) es exclusiva del <strong>Plan Business</strong>. Tu cuenta actual es Professional. Te invito a mejorar tu plan en la pestaña de Monetización para desbloquear estas herramientas avanzadas.";
            } else {
                if (text.includes('nivel') || text.includes('vip')) {
                    reply = "<strong>Niveles y Logros:</strong><br><br>Los niveles VIP automáticos permiten que tus clientes suban de categoría (por ejemplo: Bronce, Plata, Oro) basándose en su gasto total. Configúralos en la pestaña 'Mi Cuenta' encendiendo el apagador de 'Niveles VIP Automáticos'.";
                } else if (text.includes('referido')) {
                    reply = "<strong>Programa de Referidos:</strong><br><br>El sistema de referidos motiva a tus clientes a traer a sus amigos y te permite asignarles recompensas. Esta función se activa desde la configuración de la campaña.";
                } else if (text.includes('push')) {
                    reply = "<strong>Campañas Push:</strong><br><br>Envía notificaciones directo al celular de tus clientes desde la pestaña 'Campañas Push'.";
                } else if (text.includes('inbox')) {
                    reply = "<strong>Inbox de Soporte:</strong><br><br>En el Inbox puedes gestionar tickets levantados por sucursales. Es ideal para control de franquicias.";
                } else {
                    reply = "Esa función está disponible en tu plan Business. Ve a 'Mis Campañas' o 'Mi Cuenta' para configurarla.";
                }
            }
        } else if (text.includes('stripe') || text.includes('cobro') || text.includes('cita')) {
            reply = "<strong>Citas y Stripe:</strong><br><br>En la pestaña 'Citas/Servicios' puedes gestionar tu agenda. Si configuras tus llaves de Stripe en la pestaña Monetización, podrás cobrar reservas por adelantado.";
        } else if (text.includes('hola') || text.includes('ayuda')) {
            if (isBusiness) {
                reply = "¡Hola! Estoy listo para apoyarte. Pregúntame sobre el Escáner, Niveles VIP, Campañas Push, Referidos, Stripe o el Inbox.";
            } else {
                reply = "¡Hola! Soy tu asistente Professional. Pregúntame sobre cómo usar el Escáner, cómo gestionar tus Citas o cómo conectar tu cuenta de Stripe.";
            }
        }"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

