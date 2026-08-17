import re

with open('super-admin.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the loadInbox function with the new Zendesk style logic
old_loadInbox = """async function loadInbox() {
    try {
        const theme = document.getElementById('inbox-theme-filter').value;
        const tbody = document.getElementById('inbox-table-body');
        
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Cargando tickets...</td></tr>';
        
        let query = window.supabaseClient.from('support_tickets').select(`
            id, theme, subject, message, status, created_at,
            merchants(business_name, email)
        `).order('created_at', { ascending: false });
        
        if (theme !== 'all') {
            query = query.eq('theme', theme);
        }
        
        const { data, error } = await query;
        if (error) throw error;
        
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--text-muted);">No hay tickets en esta categoría.</td></tr>';
            return;
        }
        
        let html = '';
        data.forEach(t => {
            const date = new Date(t.created_at).toLocaleString();
            const merchantName = t.merchants ? t.merchants.business_name : 'Desconocido';
            const shortId = t.id.split('-')[0].toUpperCase();
            
            let statusBadge = '';
            if (t.status === 'open') statusBadge = '<span style="background: var(--accent-orange); color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">Abierto</span>';
            else if (t.status === 'resolved') statusBadge = '<span style="background: #10b981; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">Resuelto</span>';
            else statusBadge = '<span style="background: var(--surface-light); color: var(--text-color); padding: 4px 8px; border-radius: 12px; font-size: 11px;">Pendiente</span>';
            
            html += `
            <tr style="border-bottom: 1px solid var(--border-soft);">
                <td style="padding: 16px; font-family: monospace; font-size: 12px; color: var(--text-muted);">#${shortId}</td>
                <td style="padding: 16px; font-weight: bold;">${merchantName}</td>
                <td style="padding: 16px;">
                    <div style="font-weight: 600;">${t.subject}</div>
                    <div style="font-size: 12px; color: var(--text-muted);">${date}</div>
                </td>
                <td style="padding: 16px;">${statusBadge}</td>
                <td style="padding: 16px; text-align: right;">
                    <button class="btn btn-outline" style="font-size: 12px; padding: 6px 12px;" onclick="viewTicket('${t.id}')">Ver Detalle</button>
                </td>
            </tr>`;
        });
        
        tbody.innerHTML = html;
    } catch (err) {
        console.error("Error loading inbox:", err);
        document.getElementById('inbox-table-body').innerHTML = `<tr><td colspan="5" style="text-align:center;color:red;">Error: ${err.message}</td></tr>`;
    }
}"""

new_loadInbox = """let currentTickets = [];
let currentSelectedTicketId = null;

async function loadInbox() {
    try {
        const theme = document.getElementById('inbox-theme-filter').value;
        const listContainer = document.getElementById('inbox-ticket-list');
        if(!listContainer) return; // Fallback
        
        listContainer.innerHTML = '<div style="text-align:center; padding:20px; color:var(--text-muted);">Cargando tickets...</div>';
        
        let query = window.supabaseClient.from('support_tickets').select(`
            id, theme, subject, message, status, created_at, merchant_id,
            merchants(business_name, email)
        `).order('created_at', { ascending: false });
        
        if (theme !== 'all') {
            query = query.eq('theme', theme);
        }
        
        const { data, error } = await query;
        if (error) throw error;
        
        currentTickets = data || [];
        
        if (currentTickets.length === 0) {
            listContainer.innerHTML = '<div style="text-align:center; padding:20px; color:var(--text-muted);">No hay tickets en esta categoría.</div>';
            return;
        }
        
        renderTicketList();
    } catch (err) {
        console.error("Error loading inbox:", err);
    }
}

function renderTicketList() {
    const listContainer = document.getElementById('inbox-ticket-list');
    let html = '';
    
    currentTickets.forEach(t => {
        const date = new Date(t.created_at).toLocaleDateString();
        const merchantName = t.merchants ? t.merchants.business_name : 'Desconocido';
        const shortId = t.id.split('-')[0].toUpperCase();
        
        let statusDot = '';
        if (t.status === 'open') statusDot = '<div style="width:8px; height:8px; border-radius:50%; background:var(--accent-orange);"></div>';
        else if (t.status === 'resolved') statusDot = '<div style="width:8px; height:8px; border-radius:50%; background:#10b981;"></div>';
        else statusDot = '<div style="width:8px; height:8px; border-radius:50%; background:var(--text-muted);"></div>';
        
        const isSelected = currentSelectedTicketId === t.id;
        const bg = isSelected ? 'background:rgba(139,92,246,0.1); border-left:3px solid var(--primary);' : 'background:transparent; border-left:3px solid transparent;';
        
        html += `
        <div onclick="selectTicket('${t.id}')" style="padding:15px; border-radius:8px; cursor:pointer; transition:all 0.2s; border-bottom:1px solid rgba(255,255,255,0.02); ${bg}">
            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                <span style="font-weight:bold; font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${merchantName}</span>
                <span style="font-size:11px; color:var(--text-muted);">${date}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:13px; color:var(--text-color); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:80%;">${t.subject}</span>
                ${statusDot}
            </div>
        </div>`;
    });
    
    listContainer.innerHTML = html;
}

function selectTicket(id) {
    currentSelectedTicketId = id;
    renderTicketList();
    
    const ticket = currentTickets.find(t => t.id === id);
    if(!ticket) return;
    
    document.getElementById('inbox-empty-state').style.display = 'none';
    document.getElementById('chat-header').style.display = 'flex';
    document.getElementById('chat-messages').style.display = 'flex';
    document.getElementById('chat-input-area').style.display = 'block';
    
    document.getElementById('chat-merchant-name').textContent = ticket.merchants ? ticket.merchants.business_name : 'Desconocido';
    document.getElementById('chat-ticket-subject').textContent = `#${id.split('-')[0].toUpperCase()} - ${ticket.subject}`;
    document.getElementById('chat-ticket-status').value = ticket.status || 'open';
    
    // Simulate chat history with the initial message
    const msgDate = new Date(ticket.created_at).toLocaleString();
    const chatHtml = `
        <div style="display:flex; gap:15px; align-items:flex-start;">
            <div style="width:40px; height:40px; border-radius:50%; background:var(--surface-light); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <i class="fa-solid fa-store" style="color:var(--text-muted);"></i>
            </div>
            <div style="flex:1;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:5px;">
                    <span style="font-weight:bold; font-size:14px;">${document.getElementById('chat-merchant-name').textContent}</span>
                    <span style="font-size:11px; color:var(--text-muted);">${msgDate}</span>
                </div>
                <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:0 12px 12px 12px; font-size:14px; line-height:1.5;">
                    ${ticket.message}
                </div>
            </div>
        </div>
        
        <div id="chat-replies-container" style="display:flex; flex-direction:column; gap:20px; margin-top:10px;">
            <!-- Simulating no replies yet for this demo phase -->
        </div>
    `;
    
    document.getElementById('chat-messages').innerHTML = chatHtml;
}

async function updateTicketStatus() {
    if(!currentSelectedTicketId) return;
    const status = document.getElementById('chat-ticket-status').value;
    try {
        await window.supabaseClient.from('support_tickets').update({ status }).eq('id', currentSelectedTicketId);
        const tIndex = currentTickets.findIndex(t => t.id === currentSelectedTicketId);
        if (tIndex > -1) currentTickets[tIndex].status = status;
        renderTicketList();
    } catch(e) {
        console.error(e);
    }
}

function replyToTicket() {
    const text = document.getElementById('chat-reply-text').value;
    if(!text.trim() || !currentSelectedTicketId) return;
    
    // In a real app we would INSERT into 'support_replies' table.
    // For now we simulate it visually for the MVP demonstration.
    const repliesContainer = document.getElementById('chat-replies-container');
    const now = new Date().toLocaleString();
    
    const replyHtml = `
        <div style="display:flex; gap:15px; align-items:flex-start; flex-direction:row-reverse;">
            <div style="width:40px; height:40px; border-radius:50%; background:var(--primary); display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <i class="fa-solid fa-headset" style="color:white;"></i>
            </div>
            <div style="flex:1; display:flex; flex-direction:column; align-items:flex-end;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:5px; flex-direction:row-reverse;">
                    <span style="font-weight:bold; font-size:14px;">Fidelio Support</span>
                    <span style="font-size:11px; color:var(--text-muted);">${now}</span>
                </div>
                <div style="background:var(--primary); color:white; padding:15px; border-radius:12px 0 12px 12px; font-size:14px; line-height:1.5; max-width:80%;">
                    ${text.replace(/\\n/g, '<br>')}
                </div>
            </div>
        </div>
    `;
    
    repliesContainer.innerHTML += replyHtml;
    document.getElementById('chat-reply-text').value = '';
    
    // Auto mark as pending if it was open
    if (document.getElementById('chat-ticket-status').value === 'open') {
        document.getElementById('chat-ticket-status').value = 'pending';
        updateTicketStatus();
    }
    
    // Scroll to bottom
    const messagesDiv = document.getElementById('chat-messages');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
"""

if "function selectTicket" not in js:
    js = js.replace(old_loadInbox, new_loadInbox)
    with open('super-admin.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("super-admin.js updated with Zendesk style Inbox")
else:
    print("super-admin.js already contains Zendesk Inbox")
