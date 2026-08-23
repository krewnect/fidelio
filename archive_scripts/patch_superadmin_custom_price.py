import re

html_path = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/super-admin.html'
js_path = '/Users/robertoordonez/.gemini/antigravity/scratch/restaurant_loyalty_app/super-admin.js'

# --- UPDATE HTML ---
with open(html_path, 'r') as f:
    html = f.read()

html_replacement = """
                                    <th>Estado</th>
                                    <th>Fecha Registro</th>
                                    <th>Precio Especial</th>
                                    <th>Código QR</th>
                                    <th colspan="2"></th>
"""
html_pattern = re.compile(r'                                    <th>Estado</th>\n                                    <th>Fecha Registro</th>\n                                    <th>Código QR</th>\n                                    <th colspan="3"></th>', re.DOTALL)
new_html = html_pattern.sub(html_replacement.strip('\n'), html)
with open(html_path, 'w') as f:
    f.write(new_html)


# --- UPDATE JS ---
with open(js_path, 'r') as f:
    js = f.read()

# Make window function for update
window_func = """
    window.setCustomPrice = async function(merchantId, currentPrice) {
        const newPrice = prompt(`Fijar Precio Especial (MXN) mensual.\\n(Deja en blanco para borrar el precio especial):`, currentPrice || '');
        if (newPrice === null) return;
        
        const priceVal = newPrice.trim() === '' ? null : parseInt(newPrice.trim(), 10);
        if (newPrice.trim() !== '' && isNaN(priceVal)) return alert("Precio inválido");

        const { error } = await window.supabaseClient
            .from('merchants')
            .update({ custom_price: priceVal })
            .eq('id', merchantId);

        if (error) {
            console.error(error);
            alert("Error actualizando precio");
        } else {
            // refresh data locally
            const m = merchants.find(x => x.id === merchantId);
            if(m) m.custom_price = priceVal;
            renderMasterTable();
        }
    };

    if (searchInput) {
"""
js = js.replace('    if (searchInput) {', window_func.strip('\n'))

js_replacement = """
                <td>${date}</td>
                <td>
                    <button class="btn-outline" style="padding: 4px 8px; font-size: 0.8rem; border-color:var(--border-glass);" onclick="setCustomPrice('${m.id}', ${m.custom_price || null})">
                        ${m.custom_price ? '$' + m.custom_price : 'Fijar'}
                    </button>
                </td>
                <td>
                    <button class="btn-primary" style="padding: 6px 12px; font-size: 0.8rem;" onclick="downloadQR('${qrUrl}', '${m.business_name || 'comercio'}')">
                        <i class="fa-solid fa-qrcode"></i> Descargar QR
                    </button>
                </td>
                <td colspan="2"></td>
"""

js_pattern = re.compile(r'                <td>\$\{date\}</td>\n                <td>\n                    <button class="btn-primary".*?Descargar QR\n                    </button>\n                </td>\n                <td colspan="3"></td>', re.DOTALL)
new_js = js_pattern.sub(js_replacement.strip('\n'), js)
with open(js_path, 'w') as f:
    f.write(new_js)
