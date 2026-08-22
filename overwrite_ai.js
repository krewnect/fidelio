window.sendSupportGeminiMessage = async function() {
    const input = document.getElementById('support-gemini-input');
    const chatWindow = document.getElementById('support-gemini-chat');
    const msg = input.value.trim();
    if (!msg) return;

    // User Message
    chatWindow.innerHTML += `
        <div style="background: var(--accent-violet); color: white; padding: 12px 16px; border-radius: 12px 12px 0 12px; max-width: 85%; align-self: flex-end;">
            ${msg}
        </div>
    `;
    input.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // AI "Typing"
    const typingId = 'typing-' + Date.now();
    chatWindow.innerHTML += `
        <div id="${typingId}" style="background: var(--bg-hover); color: var(--text-muted); padding: 12px 16px; border-radius: 12px 12px 12px 0; max-width: 85%; align-self: flex-start; font-style: italic;">
            Escribiendo...
        </div>
    `;
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Simulate Human AI Processing time (delayed)
    setTimeout(() => {
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.remove();
        
        const text = msg.toLowerCase();
        const isBusiness = window.merchantData && window.merchantData.tier === 'business';
        let reply = "¡Hola! Estoy listo para apoyarte.";
        
        if (text.includes('escaner') || text.includes('escáner') || text.includes('premium')) {
            reply = "¡Claro que sí! Usar el escáner es pan comido. 🍞<br><br>Veamos paso a paso cómo hacerlo para que no haya pierde:<br>1️⃣ Dirígete a tu menú principal del lado izquierdo y dale clic a <strong>'Escáner Staff'</strong>.<br>2️⃣ Pídele a tu cliente que te muestre el código QR de su tarjeta Fidelio (la que guardaron en Apple Wallet o Google Pay).<br>3️⃣ Apunta la cámara de tu celular o tablet hacia su QR. ¡Y pum! El sistema registrará su visita automáticamente y le sumará su sello o beneficio.<br><br>Un dato curioso: ¿Sabías que los clientes se emocionan muchísimo cuando escuchan el sonidito de un nuevo sello? 😅 ¡Pruébalo hoy mismo y me cuentas cómo te va!";
        } else if (text.includes('nivel') || text.includes('logro') || text.includes('vip') || text.includes('cashback') || text.includes('referido') || text.includes('push') || text.includes('inbox') || text.includes('8') || text.includes('ocho')) {
            if (!isBusiness) {
                reply = "¡Uy! Me encantaría mostrarte esa función, pero es como el pase VIP para el backstage 🎸... ¡Es exclusiva del <strong>Plan Business</strong>!<br><br>Actualmente tienes la versión Professional. Si alguna vez quieres desbloquear superpoderes como las Campañas Push, automatizaciones VIP o el Inbox, te súper recomiendo darte una vuelta por la pestaña de 'Monetización' y mejorar tu plan. ¡Vale muchísimo la pena!";
            } else {
                reply = "¡Hola! Como cuentas con el Plan Business, tienes acceso a todas nuestras funciones premium. Dirígete a la pestaña de 'Mis Campañas' para configurar tus niveles VIP, referidos y Cashback.";
            }
        } else if (text.includes('stripe') || text.includes('cobro') || text.includes('cita')) {
            reply = "¡Claro! Configurar los cobros y la agenda es de lo mejor que puedes hacer para que no te dejen plantado (a nadie le gusta eso 💔).<br><br>Aquí tienes los pasos, súper sencillos:<br>1️⃣ Ve a la pestaña <strong>'Citas/Servicios'</strong> para armar tus horarios disponibles y guardar.<br>2️⃣ Para cobrar por adelantado o apartar lugar, entra a <strong>'Monetización'</strong> y pega ahí tu Enlace de Pago de Stripe.<br><br>¡Así de fácil! Tus clientes reservan solos desde su teléfono mientras tú te tomas un cafecito ☕.";
        } else if (text.includes('hola') || text.includes('ayuda') || text.includes('buenas') || text.includes('buenos')) {
            reply = "¡Hola, hola! 👋 Qué gusto saludarte. Soy tu asistente de Fidelio (aunque a veces trabajo tanto que creo que soy un humano atrapado en el código 🤖). <br><br>Estoy aquí para ayudarte a sacarle el máximo provecho a la plataforma. ¿En qué te puedo echar la mano hoy? Pregúntame sobre el escáner, las citas o tu cuenta de Stripe.";
        } else {
            reply = "¡Ay caramba! 😅 Me agarraste un poquito en curva con esa pregunta. Mi cerebro digital todavía está procesando algunas cosas y no encontré la respuesta exacta a eso.<br><br>Pero no te preocupes, no te voy a dejar solo. Justo a tu derecha tienes el formulario para <strong>Levantar un Ticket de Soporte</strong>. Envía el reporte y mis amigos los ingenieros (ellos sí toman café de verdad ☕) te resolverán este tema de volada.";
        }

        chatWindow.innerHTML += `
            <div style="background: var(--surface); border: 1px solid var(--border-soft); color: var(--text-main); padding: 12px 16px; border-radius: 12px 12px 12px 0; max-width: 85%; align-self: flex-start; line-height: 1.5; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                ${reply}
            </div>
        `;
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 2800); // Retraso de casi 3 segundos para simular "humanidad"
};
