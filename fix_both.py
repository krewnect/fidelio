import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Split around the sections. Let's just find each section manually using Python logic.
def extract_and_replace_section(html, section_id, start_marker, end_marker, replacement):
    pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
    # We want to replace only the first occurrence after the section ID
    section_start = html.find(f'id="{section_id}"')
    if section_start == -1:
        return html
    match = pattern.search(html, section_start)
    if match:
        return html[:match.start()] + replacement + html[match.end():]
    return html

# 1. INBOX SOPORTE
inbox_replacement = """<!-- SUPPORT TICKETS LIST -->
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
            </section>"""
html = extract_and_replace_section(html, "tab-inbox", "<!-- WHATSAPP STYLE INBOX -->", "</section>", inbox_replacement)

# 2. EQUIPO FIDELIO
team_replacement = """<!-- TEAM LIST -->
                    <div class="content-panel" style="padding: 24px;">
                        <h3 style="font-size: 1.4rem; margin-bottom: 16px; font-weight: 800;"><i class="fa-solid fa-users"></i> Miembros del Equipo</h3>
                        <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left;">
                            <thead>
                                <tr style="border-bottom: 2px solid var(--border-soft); color: var(--text-muted); font-size: 12px; text-transform: uppercase;">
                                    <th style="padding: 16px;">Usuario</th>
                                    <th style="padding: 16px;">Rol</th>
                                    <th style="padding: 16px; text-align: right;">Acciones</th>
                                </tr>
                            </thead>
                            <tbody id="admin-team-body">
                                <tr>
                                    <td style="padding: 16px;">
                                        <strong>hola@fideliorewards.com</strong>
                                    </td>
                                    <td style="padding: 16px;">
                                        <span class="menu-badge" style="background:var(--accent-violet); color:#fff; font-size:10px;">Super Admin</span>
                                    </td>
                                    <td style="padding: 16px; text-align: right;">
                                        <button class="fidelio-btn-secondary-preset" title="Remover"><i class="fa-solid fa-trash" style="color: #ef4444;"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>"""
html = extract_and_replace_section(html, "tab-fidelio-team", "<!-- WHATSAPP STYLE INBOX -->", "</section>", team_replacement)

# 3. MODAL ANTIGRAVITY BUTTON
old_modal_close = """                    <div id="ticket-modal-actions" style="display:flex; gap:12px; margin-top:24px;">
                        <!-- Actions injected via JS -->
                    </div>"""
new_modal_close = """                    <div id="ticket-modal-actions" style="display:flex; gap:12px; margin-top:24px;">
                        <!-- Actions injected via JS -->
                    </div>
                    <div style="margin-top: 16px; border-top: 1px solid var(--border-soft); padding-top: 16px; text-align: center;">
                        <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;"><i class="fa-solid fa-code"></i> ¿Es un bug o error de código reportado por un usuario?</p>
                        <button onclick="copyTicketForAntigravity()" class="fidelio-btn-primary" style="background: #111827; border: none; width: 100%; justify-content: center; font-size: 13px;">
                            <i class="fa-solid fa-terminal"></i> Copiar Detalles para Antigravity Copilot
                        </button>
                    </div>"""
html = html.replace(old_modal_close, new_modal_close)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML fully updated.")
