with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        const isBusiness = window.merchantData && window.merchantData.tier === 'business';
        
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
        }

        chatWindow.innerHTML += `
            <div style="background: var(--surface); border: 1px solid var(--border-soft); color: var(--text-main); padding: 12px 16px; border-radius: 12px 12px 12px 0; max-width: 85%; align-self: flex-start; line-height: 1.5;">
                ${reply}
            </div>
        `;
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 1500);"""

replacement = """        const isBusiness = window.merchantData && window.merchantData.tier === 'business';
        
        if (text.includes('escaner') || text.includes('escáner') || text.includes('premium')) {
            reply = "¡Claro que sí! Usar el escáner es pan comido. 🍞<br><br>Veamos paso a paso cómo hacerlo para que no haya pierde:<br>1️⃣ Dirígete a tu menú principal del lado izquierdo y dale clic a <strong>'Escáner Staff'</strong>.<br>2️⃣ Pídele a tu cliente que te muestre el código QR de su tarjeta Fidelio (la que guardaron en Apple Wallet o Google Pay).<br>3️⃣ Apunta la cámara de tu celular o tablet hacia su QR. ¡Y pum! El sistema registrará su visita automáticamente y le sumará su sello.<br><br>Un dato curioso: ¿Sabías que los clientes se emocionan muchísimo cuando escuchan el sonidito de un nuevo sello? 😅 ¡Pruébalo hoy mismo y me cuentas cómo te va!";
        } else if (text.includes('nivel') || text.includes('logro') || text.includes('vip') || text.includes('cashback') || text.includes('referido') || text.includes('push') || text.includes('inbox') || text.includes('8') || text.includes('ocho')) {
            if (!isBusiness) {
                reply = "¡Uy! Me encantaría mostrarte esa función, pero es como el pase VIP para el backstage 🎸... ¡Es exclusiva del <strong>Plan Business</strong>!<br><br>Actualmente tienes la versión Professional. Si alguna vez quieres desbloquear superpoderes como las Campañas Push, automatizaciones VIP o el Inbox, te súper recomiendo darte una vuelta por la pestaña de 'Monetización' y mejorar tu plan. ¡Vale muchísimo la pena!";
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
                    reply = "¡Hola! Veo que preguntas por funciones avanzadas. Como eres cliente Business, tienes acceso total. Dirígete a 'Mis Campañas' o 'Mi Cuenta' para configurarlas.";
                }
            }
        } else if (text.includes('stripe') || text.includes('cobro') || text.includes('cita')) {
            reply = "¡Claro! Configurar los cobros y la agenda es de lo mejor que puedes hacer para que no te dejen plantado (a nadie le gusta eso 💔).<br><br>Aquí tienes los pasos, súper sencillos:<br>1️⃣ Ve a la pestaña <strong>'Citas/Servicios'</strong> para armar tus horarios disponibles y guardar.<br>2️⃣ Para cobrar por adelantado o apartar lugar, entra a <strong>'Monetización (Stripe)'</strong> y pega ahí tu Enlace de Pago.<br><br>¡Así de fácil! Tus clientes reservan solos desde su teléfono mientras tú te tomas un cafecito ☕.";
        } else if (text.includes('hola') || text.includes('ayuda') || text.includes('buenos dias') || text.includes('buenas tardes')) {
            reply = "¡Hola, hola! 👋 Qué gusto saludarte. Soy tu asistente de Fidelio (aunque a veces trabajo tanto que creo que soy un humano atrapado en el código 🤖). <br><br>Estoy aquí para ayudarte a sacarle el máximo provecho a la plataforma. ¿En qué te puedo echar la mano hoy? Pregúntame sobre el escáner, las citas o tu cuenta de Stripe.";
        } else {
            reply = "¡Ay caramba! 😅 Me agarraste un poquito en curva con esa pregunta. Mi cerebro digital todavía está procesando algunas cosas y no encontré la respuesta exacta a eso.<br><br>Pero no te preocupes, no te voy a dejar solo. Justo a tu derecha tienes el formulario rojo para <strong>Levantar un Ticket de Soporte</strong>. Levanta el reporte y mis amigos los ingenieros (ellos sí toman café de verdad ☕) te resolverán este tema de volada.";
        }

        chatWindow.innerHTML += `
            <div style="background: var(--surface); border: 1px solid var(--border-soft); color: var(--text-main); padding: 12px 16px; border-radius: 12px 12px 12px 0; max-width: 85%; align-self: flex-start; line-height: 1.5; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                ${reply}
            </div>
        `;
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 2800); // Retraso de casi 3 segundos para simular que está "escribiendo" de verdad"""

js = js.replace(target, replacement)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)

