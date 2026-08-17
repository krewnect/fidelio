import re

# 1. UPDATE INDEX.HTML
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the 'rest-icon' section with the new file dropzone + select combination
old_icon_section = """                                <div>
                                    <label class="premium-label">Ícono (Temporal)</label>
                                    <select id="rest-icon" class="premium-input">
                                        <option value="fa-crown" selected>Corona (Premium)</option>
                                        <option value="fa-burger">Hamburguesa</option>
                                        <option value="fa-scissors">Tijeras</option>
                                        <option value="fa-mug-hot">Café</option>
                                        <option value="fa-hand-sparkles">Uñas/Belleza</option>
                                        <option value="fa-bag-shopping">Retail/Ropa</option>
                                        <option value="fa-paw">Mascotas</option>
                                        <option value="fa-gamepad">Arcade/Juegos</option>
                                        <option value="fa-dumbbell">Gimnasio</option>
                                    </select>
                                </div>"""

new_icon_section = """                                <div>
                                    <label class="premium-label">Ícono o Imagen del Sello</label>
                                    <select id="rest-icon" class="premium-input" style="margin-bottom: 8px;">
                                        <option value="fa-crown" selected>Corona (Premium)</option>
                                        <option value="fa-burger">Hamburguesa</option>
                                        <option value="fa-scissors">Tijeras</option>
                                        <option value="fa-mug-hot">Café</option>
                                        <option value="fa-hand-sparkles">Uñas/Belleza</option>
                                        <option value="fa-bag-shopping">Retail/Ropa</option>
                                        <option value="fa-paw">Mascotas</option>
                                        <option value="fa-gamepad">Arcade/Juegos</option>
                                        <option value="fa-dumbbell">Gimnasio</option>
                                    </select>
                                    <div class="file-dropzone" id="stamp-dropzone" style="height: 60px; min-height: 60px;">
                                        <input type="file" id="stamp-file-input" accept="image/png, image/jpeg">
                                        <i class="fa-solid fa-stamp" style="font-size:16px;"></i>
                                        <span style="font-size:11px;">Subir Sello Personalizado</span>
                                    </div>
                                    <button id="btn-remove-stamp" class="btn btn-outline" style="display:none; margin-top:8px; padding:6px 12px; font-size:12px; width:100%; justify-content:center;">Quitar Imagen Sello</button>
                                </div>"""

content = content.replace(old_icon_section, new_icon_section)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 2. UPDATE DASHBOARD.JS
with open('dashboard.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Add listener for stamp-file-input and btn-remove-stamp
upload_handlers_insertion = """    const stampFileInput = document.getElementById('stamp-file-input');
    const btnRemoveStamp = document.getElementById('btn-remove-stamp');
    
    if (stampFileInput) {
        stampFileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (evt) => {
                    state.iconClass = evt.target.result;
                    if(btnRemoveStamp) btnRemoveStamp.style.display = 'inline-block';
                    updatePassRender();
                    showToast("Sello personalizado cargado", "success");
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    if (btnRemoveStamp) {
        btnRemoveStamp.addEventListener('click', () => {
            const sel = document.getElementById('rest-icon');
            state.iconClass = sel ? sel.value : 'fa-star';
            if(stampFileInput) stampFileInput.value = '';
            btnRemoveStamp.style.display = 'none';
            updatePassRender();
            showToast("Imagen del sello removida", "info");
        });
    }
"""

js_content = js_content.replace("    const logoFileInput = document.getElementById('logo-file-input');", upload_handlers_insertion + "\n    const logoFileInput = document.getElementById('logo-file-input');")

# Also, when selectCampaign is called, update UI for stamp button
js_select_campaign = """        state.activeMode = camp.type || "hybrid";"""
js_select_campaign_new = """        state.activeMode = camp.type || "hybrid";
        const btnRemoveStamp = document.getElementById('btn-remove-stamp');
        if (state.iconClass && state.iconClass.startsWith('data:image')) {
            if (btnRemoveStamp) btnRemoveStamp.style.display = 'inline-block';
        } else {
            if (btnRemoveStamp) btnRemoveStamp.style.display = 'none';
        }
"""
js_content = js_content.replace(js_select_campaign, js_select_campaign_new)

with open('dashboard.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("index.html and dashboard.js updated successfully.")
