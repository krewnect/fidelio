import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = "<!-- WHATSAPP STYLE INBOX -->"
end_marker = "<!-- EQUIPO FIDELIO (STAFF / ROLES) -->"

pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)

new_layout = """<!-- SUPPORT TICKETS LIST -->
                <div class="content-panel" style="padding: 24px; min-height: 500px;">
                    <div style="width: 100%;">
                        <div style="display: grid; grid-template-columns: 1fr 2fr 3fr 1fr 1fr; gap: 16px; padding: 12px 16px; border-bottom: 2px solid var(--border-soft); color: var(--text-muted); font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                            <div>ID & Fecha</div>
                            <div>Usuario</div>
                            <div>Asunto & Mensaje</div>
                            <div>Estado</div>
                            <div style="text-align:right;">Acciones</div>
                        </div>
                        <div id="inbox-table-body" style="display: flex; flex-direction: column;">
                            <div style="padding: 20px; text-align: center; color: var(--text-muted);">Cargando tickets...</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- EQUIPO FIDELIO (STAFF / ROLES) -->"""

if re.search(pattern, html):
    html = re.sub(pattern, new_layout, html)
else:
    print("WARNING: Exact match failed for INBOX")

# Now inject the Antigravity button into modal-ticket-detail
old_modal_close = """                    <div id="ticket-modal-actions" style="display:flex; gap:12px; margin-top:24px;">
                        <!-- Actions injected via JS -->
                    </div>"""
new_modal_close = """                    <div id="ticket-modal-actions" style="display:flex; gap:12px; margin-top:24px;">
                        <!-- Actions injected via JS -->
                    </div>
                    <div style="margin-top: 16px; border-top: 1px solid var(--border-soft); padding-top: 16px; text-align: center;">
                        <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;"><i class="fa-solid fa-code"></i> ¿Es un bug o error de código?</p>
                        <button onclick="copyTicketForAntigravity()" class="fidelio-btn-primary" style="background: #111827; border: none; width: 100%; justify-content: center; font-size: 13px;">
                            <i class="fa-solid fa-terminal"></i> Copiar Ticket para Antigravity
                        </button>
                    </div>"""

if old_modal_close in html:
    html = html.replace(old_modal_close, new_modal_close)
else:
    print("WARNING: Exact match failed for MODAL")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML updated.")
