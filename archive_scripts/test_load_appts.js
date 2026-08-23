const state = {
    customers: [
        { id: "d73dabae-0ac8-4305-97d7-3b6192c575ad", full_name: "Test Customer", phone: "1234567890" }
    ],
    transactions: [
        { id: "appt-123", customer_id: "d73dabae-0ac8-4305-97d7-3b6192c575ad", transaction_type: "appointment_request", created_at: new Date().toISOString(), notes: '{"date":"2026-08-19","time":"14:00","notes":"Test"}' }
    ]
};
const window = { merchantData: { appointment_settings: { processed_appointments: [] } } };

    const appts = state.transactions
        .filter(t => t.transaction_type === 'appointment_request')
        .sort((a,b) => new Date(b.created_at) - new Date(a.created_at));

    let stripeLink = "";

    const html = appts.map(t => {
        let details = {};
        try { details = JSON.parse(t.notes || "{}"); } catch(e){}
        const cust = state.customers.find(c => c.id === t.customer_id) || {};
        
        const dateRaw = details.date || 'Sin fecha';
        const timeRaw = details.time || 'Sin hora';
        const serviceNotes = details.notes || 'Ninguna';
        const name = cust.full_name || cust.name || 'Cliente Desconocido';
        const phone = cust.phone || '';
        
        let msg = `Hola ${name}, he recibido tu solicitud de cita para el día ${dateRaw} a las ${timeRaw}. Para confirmar tu lugar, por favor realiza el pago o anticipo aquí: ${stripeLink}`;
        const waLink = phone ? `https://wa.me/${phone.replace(/\D/g,'')}?text=${encodeURIComponent(msg)}` : '#';
        
        return "SUCCESS";
    }).join('');

console.log(html);
