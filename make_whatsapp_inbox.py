import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the Inbox content panel with a WhatsApp UI
inbox_target = r'<div class="content-panel" style="background: var\(--surface\); border-radius: 20px; padding: 24px; box-shadow: var\(--shadow-sm\); overflow-x: auto;">[\s\S]*?</tbody>\s*</table>\s*</div>'

whatsapp_ui = """
                <!-- WHATSAPP STYLE INBOX -->
                <div class="content-panel" style="background: #ffffff; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); display: flex; height: 600px; overflow: hidden; border: 1px solid #e2e8f0;">
                    
                    <!-- Left Sidebar: Contact List -->
                    <div style="width: 320px; border-right: 1px solid #e2e8f0; background: #f8fafc; display: flex; flex-direction: column;">
                        <div style="padding: 16px; background: #f1f5f9; border-bottom: 1px solid #e2e8f0; font-weight: 800; color: #1e293b; display:flex; justify-content:space-between; align-items:center;">
                            <span><i class="fa-brands fa-whatsapp" style="color: #25D366; font-size: 18px; margin-right: 8px;"></i> Chats Activos</span>
                            <i class="fa-solid fa-pen-to-square" style="color: #64748b; cursor:pointer;"></i>
                        </div>
                        <div style="padding: 12px;">
                            <input type="text" placeholder="Buscar cliente..." style="width: 100%; padding: 10px 14px; border-radius: 20px; border: 1px solid #cbd5e1; background: #ffffff; outline: none; font-size: 13px;">
                        </div>
                        <div id="inbox-contact-list" style="flex: 1; overflow-y: auto;">
                            <!-- Hardcoded Demo Chat to show the UI since backend data is not fully connected -->
                            <div style="padding: 16px; border-bottom: 1px solid #e2e8f0; display: flex; gap: 12px; cursor: pointer; background: #ffffff; transition: background 0.2s;" onmouseover="this.style.background='#f1f5f9'" onmouseout="this.style.background='#ffffff'">
                                <div style="width: 48px; height: 48px; border-radius: 50%; background: #e2e8f0; display:flex; align-items:center; justify-content:center; overflow:hidden;">
                                    <img src="https://i.pravatar.cc/150?img=33" style="width:100%; height:100%; object-fit:cover;">
                                </div>
                                <div style="flex: 1; overflow: hidden;">
                                    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
                                        <div style="font-weight: 700; color: #0f172a; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Roberto Ordóñez</div>
                                        <div style="font-size: 11px; color: #94a3b8;">10:42 AM</div>
                                    </div>
                                    <div style="font-size: 13px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">¡Hola! Tengo una duda con mis sellos...</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right Side: Chat Window -->
                    <div style="flex: 1; display: flex; flex-direction: column; background: #efeae2;">
                        <div style="padding: 16px 24px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; gap: 16px;">
                            <div style="width: 40px; height: 40px; border-radius: 50%; overflow:hidden;">
                                <img src="https://i.pravatar.cc/150?img=33" style="width:100%; height:100%; object-fit:cover;">
                            </div>
                            <div>
                                <div style="font-weight: 700; color: #0f172a; font-size: 15px;">Roberto Ordóñez</div>
                                <div style="font-size: 12px; color: #25D366; font-weight: 600;">En línea</div>
                            </div>
                        </div>
                        
                        <div style="flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 16px;" id="chat-messages-area">
                            <div style="align-self: center; background: #ffeebb; color: #856404; font-size: 11px; padding: 6px 12px; border-radius: 8px; font-weight: 600; margin-bottom: 10px;">Hoy</div>
                            
                            <!-- Received Bubble -->
                            <div style="align-self: flex-start; max-width: 70%; display: flex; gap: 8px;">
                                <div style="background: #ffffff; padding: 12px 16px; border-radius: 0px 16px 16px 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); position: relative;">
                                    <div style="font-size: 14px; color: #1e293b; line-height: 1.4;">¡Hola! Vine a la cafetería la semana pasada y no se cargaron mis sellos en la Wallet. ¿Me pueden ayudar?</div>
                                    <div style="font-size: 10px; color: #94a3b8; text-align: right; margin-top: 4px;">10:42 AM</div>
                                </div>
                            </div>

                            <!-- Sent Bubble -->
                            <div style="align-self: flex-end; max-width: 70%; display: flex; gap: 8px;">
                                <div style="background: #dcf8c6; padding: 12px 16px; border-radius: 16px 0px 16px 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); position: relative;">
                                    <div style="font-size: 14px; color: #1e293b; line-height: 1.4;">¡Hola Roberto! Una disculpa enorme. Acabo de revisar el sistema y ya te sumé manualmente los 2 sellos de tu visita. Como compensación, te agregué 1 sello extra. ¡Te esperamos pronto!</div>
                                    <div style="font-size: 10px; color: #64748b; text-align: right; margin-top: 4px;">10:45 AM <i class="fa-solid fa-check-double" style="color: #3b82f6;"></i></div>
                                </div>
                            </div>
                        </div>

                        <!-- Chat Input Area -->
                        <div style="padding: 16px 24px; background: #f8fafc; border-top: 1px solid #e2e8f0; display: flex; gap: 12px; align-items: center;">
                            <i class="fa-regular fa-face-smile" style="font-size: 24px; color: #64748b; cursor: pointer;"></i>
                            <i class="fa-solid fa-paperclip" style="font-size: 20px; color: #64748b; cursor: pointer;"></i>
                            <input type="text" placeholder="Escribe un mensaje..." style="flex: 1; padding: 12px 16px; border-radius: 24px; border: 1px solid #cbd5e1; outline: none; font-size: 14px;">
                            <button style="width: 44px; height: 44px; border-radius: 50%; background: #25D366; color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);">
                                <i class="fa-solid fa-paper-plane" style="margin-left: -2px;"></i>
                            </button>
                        </div>
                    </div>
                </div>
"""

html = re.sub(inbox_target, whatsapp_ui, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
