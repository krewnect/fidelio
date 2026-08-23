import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html = """                        <div style="margin-bottom: 16px;">
                            <label style="display: block; font-size: 12px; font-weight: 600; color: var(--text-muted); margin-bottom: 6px;">Precio Mensual (Mensualidad Personalizada)</label>
                            <div style="display: flex; gap: 8px;">
                                <input type="number" id="admin-custom-price" placeholder="Vacío = Tarifa Oficial" style="flex: 1; padding: 10px 14px; border-radius: 8px; border: 1px solid var(--border-soft); background: var(--bg-input); font-family: inherit; font-size: 14px; outline: none; transition: var(--transition);">
                                <button onclick="saveAdminCustomPrice()" class="fidelio-btn-primary" style="padding: 10px 16px; border-radius: 8px;"><i class="fa-solid fa-save"></i> Guardar</button>
                            </div>
                            <small style="display: block; font-size: 11px; color: var(--text-muted); margin-top: 6px;">MXN. Si dejas esto vacío, el negocio pagará el precio oficial de Stripe para su plan.</small>
                        </div>"""

new_html = """                        <div style="margin-bottom: 16px;">
                            <label style="display: block; font-size: 12px; font-weight: 600; color: var(--text-muted); margin-bottom: 6px;">Precio Mensual Personalizado (MXN)</label>
                            <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                                <input type="number" id="admin-custom-price" placeholder="Monto ($)" style="flex: 1; padding: 10px 14px; border-radius: 8px; border: 1px solid var(--border-soft); background: var(--bg-input); font-family: inherit; font-size: 14px; outline: none;">
                                <input type="number" id="admin-custom-price-months" placeholder="Meses (Opcional)" style="flex: 1; padding: 10px 14px; border-radius: 8px; border: 1px solid var(--border-soft); background: var(--bg-input); font-family: inherit; font-size: 14px; outline: none;" title="Dejar vacío para precio vitalicio">
                                <button onclick="saveAdminCustomPrice()" class="fidelio-btn-primary" style="padding: 10px 16px; border-radius: 8px;"><i class="fa-solid fa-save"></i></button>
                            </div>
                            <small id="admin-custom-price-expiry-label" style="display: block; font-size: 11px; color: var(--accent-violet); font-weight: 600; margin-bottom: 4px;"></small>
                            <small style="display: block; font-size: 11px; color: var(--text-muted);">Si dejas Meses vacío, la tarifa es permanente. Si dejas Monto vacío, pagará el precio oficial.</small>
                        </div>"""

if old_html in html:
    html = html.replace(old_html, new_html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("HTML patched successfully")
else:
    print("WARNING: Could not find old HTML block")
