import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_inbox = """                <div class="content-panel" style="background: var(--surface); border-radius: 20px; padding: 24px; box-shadow: var(--shadow-sm); overflow-x: auto;">
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 2px solid var(--border-soft); color: var(--text-muted);">
                                <th style="padding: 16px;">ID Ticket</th>
                                <th style="padding: 16px;">Restaurante / Remitente</th>
                                <th style="padding: 16px;">Asunto</th>
                                <th style="padding: 16px;">Estado</th>
                                <th style="padding: 16px; text-align: right;">Acciones</th>
                            </tr>
                        </thead>
                        <tbody id="inbox-table-body">
                            <!-- JS inyecta tickets -->
                        </tbody>
                    </table>
                </div>"""

new_inbox = """                <div style="display:flex; height:700px; background:var(--surface); border-radius:20px; overflow:hidden; border:1px solid var(--border-color); box-shadow:0 10px 30px rgba(0,0,0,0.5);">
                    <!-- LEFT PANE: TICKET LIST -->
                    <div style="width:350px; background:var(--surface-color); border-right:1px solid var(--border-color); display:flex; flex-direction:column;">
                        <div style="padding:15px; border-bottom:1px solid var(--border-color); background:rgba(255,255,255,0.02);">
                            <input type="text" class="fidelio-input" placeholder="Buscar ticket o comercio..." style="width:100%; font-size:13px; padding:8px 12px;">
                        </div>
                        <div id="inbox-ticket-list" style="flex:1; overflow-y:auto; padding:10px; display:flex; flex-direction:column; gap:5px;">
                            <!-- JS inyectará tickets aquí -->
                            <div style="text-align:center; padding:20px; color:var(--text-muted);">Cargando tickets...</div>
                        </div>
                    </div>
                    
                    <!-- RIGHT PANE: CHAT THREAD -->
                    <div id="inbox-chat-pane" style="flex:1; background:var(--bg-color); display:flex; flex-direction:column; position:relative;">
                        <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); text-align:center; color:var(--text-muted);" id="inbox-empty-state">
                            <i class="fa-solid fa-inbox" style="font-size:48px; margin-bottom:15px; opacity:0.5;"></i>
                            <p>Selecciona un ticket de la izquierda<br>para ver la conversación.</p>
                        </div>
                        
                        <!-- Chat Header -->
                        <div id="chat-header" style="display:none; padding:15px 25px; background:var(--surface); border-bottom:1px solid var(--border-color); justify-content:space-between; align-items:center;">
                            <div>
                                <h3 id="chat-merchant-name" style="margin:0; font-size:16px;">...</h3>
                                <p id="chat-ticket-subject" style="margin:0; color:var(--text-muted); font-size:13px;">...</p>
                            </div>
                            <div style="display:flex; gap:10px;">
                                <select id="chat-ticket-status" class="fidelio-input" style="padding:6px 12px; font-size:12px;" onchange="updateTicketStatus()">
                                    <option value="open">Abierto</option>
                                    <option value="pending">Pendiente</option>
                                    <option value="resolved">Resuelto</option>
                                </select>
                            </div>
                        </div>
                        
                        <!-- Chat Messages -->
                        <div id="chat-messages" style="display:none; flex:1; padding:25px; overflow-y:auto; display:flex; flex-direction:column; gap:20px;">
                            <!-- Messages go here -->
                        </div>
                        
                        <!-- Chat Input -->
                        <div id="chat-input-area" style="display:none; padding:20px; background:var(--surface); border-top:1px solid var(--border-color);">
                            <div style="display:flex; gap:10px;">
                                <textarea id="chat-reply-text" class="fidelio-input" placeholder="Escribe tu respuesta al cliente..." style="flex:1; resize:none; height:45px; padding-top:12px;"></textarea>
                                <button class="btn btn-primary" onclick="replyToTicket()" style="width:45px; height:45px; border-radius:12px; display:flex; justify-content:center; align-items:center;"><i class="fa-solid fa-paper-plane"></i></button>
                            </div>
                        </div>
                    </div>
                </div>"""

if "inbox-table-body" in html and "inbox-ticket-list" not in html:
    html = html.replace(old_inbox, new_inbox)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html Support Inbox updated to Split-Pane")
else:
    print("index.html already updated or could not find inbox-table-body")
