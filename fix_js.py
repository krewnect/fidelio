import re

with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the tbody logic in loadInbox
old_tbody = "tbody.innerHTML += `"
new_tbody = "tbody.innerHTML += `"
old_row = """                <tr style="border-bottom: 1px solid var(--border-soft); ${t.status === 'resuelto' ? 'opacity: 0.6;' : ''}">
                    <td style="padding: 16px; font-size:12px; font-family:monospace;">#${t.id.substring(0,8)}</td>
                    <td style="padding: 16px;">
                        <strong>${t.email || 'Desconocido'}</strong>
                        <div style="font-size:12px; color:var(--text-muted);">${t.merchant_id || 'Visitante'}</div>
                    </td>
                    <td style="padding: 16px;">
                        <strong style="display:block;">${t.subject}</strong>
                        <span style="font-size:13px; color:var(--text-muted);">${t.message.substring(0, 50)}${t.message.length>50?'...':''}</span>
                    </td>
                    <td style="padding: 16px;">${statusBadge}</td>
                    <td style="padding: 16px; text-align: right;">
                        <button class="fidelio-btn-secondary-preset" onclick="viewTicketDetail(${index})" title="Ver Detalle"><i class="fa-solid fa-eye" style="color:var(--accent-violet);"></i></button>
                        ${t.status === 'abierto' ? `<button class="fidelio-btn-secondary-preset" onclick="resolveTicket('${t.id}')" title="Marcar Resuelto"><i class="fa-solid fa-check" style="color:var(--accent-violet);"></i></button>` : ''}
                    </td>
                </tr>"""

new_row = """                <div style="display: grid; grid-template-columns: 1fr 2fr 3fr 1fr 1fr; gap: 16px; padding: 16px; border-bottom: 1px solid var(--border-soft); align-items: center; ${t.status === 'resuelto' ? 'opacity: 0.6;' : ''}">
                    <div>
                        <div style="font-size:12px; font-family:monospace; color:var(--text-main); font-weight:700;">#${t.id.substring(0,8)}</div>
                        <div style="font-size:11px; color:var(--text-muted);">${date}</div>
                    </div>
                    <div>
                        <div style="font-weight:700; color:var(--text-main); font-size:13px;">${t.email || 'Desconocido'}</div>
                        <div style="font-size:11px; color:var(--text-muted);">${t.merchant_id || 'Visitante'}</div>
                    </div>
                    <div>
                        <div style="font-weight:700; color:var(--text-main); font-size:13px;">${t.subject}</div>
                        <div style="font-size:12px; color:var(--text-muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:250px;">${t.message}</div>
                    </div>
                    <div>${statusBadge}</div>
                    <div style="text-align: right; display:flex; justify-content:flex-end; gap:8px;">
                        <button class="fidelio-btn-secondary" style="padding:6px 10px;" onclick="viewTicketDetail(${index})" title="Ver Detalle"><i class="fa-solid fa-eye" style="color:var(--accent-violet);"></i></button>
                        ${t.status === 'abierto' ? `<button class="fidelio-btn-secondary" style="padding:6px 10px;" onclick="resolveTicket('${t.id}')" title="Marcar Resuelto"><i class="fa-solid fa-check" style="color:#10b981;"></i></button>` : ''}
                    </div>
                </div>"""

if old_row in js:
    js = js.replace(old_row, new_row)
else:
    print("WARNING: Row replacement failed")

# Add copyTicketForAntigravity
antigravity_logic = """
window.copyTicketForAntigravity = async function() {
    const id = document.getElementById('ticket-modal-id').innerText;
    const email = document.getElementById('ticket-modal-email').innerText;
    const subject = document.getElementById('ticket-modal-subject').innerText;
    const msg = document.getElementById('ticket-modal-message').innerText;
    
    const prompt = `¡Hola Antigravity! Un usuario me reportó el siguiente error en la aplicación. ¿Me ayudas a revisar el código e implementar la solución?
    
DATOS DEL TICKET:
- ID: ${id}
- Usuario: ${email}
- Asunto: ${subject}
- Descripción del problema:
"${msg}"

Por favor, revisa el código correspondiente y propón la corrección.`;

    try {
        await navigator.clipboard.writeText(prompt);
        if(typeof window.showToast === 'function') {
            window.showToast("Copiado al portapapeles. ¡Pégalo en tu consola local de Antigravity!", "success");
        } else {
            alert("Copiado al portapapeles. Pégalo en Antigravity.");
        }
    } catch(err) {
        if(typeof window.showToast === 'function') window.showToast("Error al copiar texto", "error");
    }
};
"""
js += antigravity_logic

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("JS updated.")
