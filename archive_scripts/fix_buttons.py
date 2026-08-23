import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_block = """                        <div style="display:flex; align-items:center; gap: 8px;">
                            <button class="fidelio-btn-primary"><i class="fa-solid fa-file-excel"></i> Descargar Layout</button>
                            <label class="fidelio-btn-primary">
                                <i class="fa-solid fa-cloud-arrow-up"></i> Subir CSV
                                <input type="file" id="upload-branches-csv" accept=".csv" style="display: none;" onchange="uploadBranchesCSV(event)">
                            </label>
                            <button class="fidelio-btn-primary"><i class="fa-solid fa-plus"></i> Añadir Sucursal</button>
                        </div>"""

new_block = """                        <div style="display:flex; align-items:center; gap: 8px; flex-wrap: nowrap;">
                            <button class="fidelio-btn-primary" style="flex: 1; white-space: nowrap; padding: 12px 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important;"><i class="fa-solid fa-file-excel"></i> Descargar Layout</button>
                            <label class="fidelio-btn-primary" style="flex: 1; white-space: nowrap; padding: 12px 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important; margin: 0; cursor: pointer;">
                                <i class="fa-solid fa-cloud-arrow-up"></i> Subir CSV
                                <input type="file" id="upload-branches-csv" accept=".csv" style="display: none;" onchange="uploadBranchesCSV(event)">
                            </label>
                            <button class="fidelio-btn-primary" style="flex: 1; white-space: nowrap; padding: 12px 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important;"><i class="fa-solid fa-plus"></i> Añadir Sucursal</button>
                        </div>"""

if old_block in html:
    html = html.replace(old_block, new_block)
else:
    print("WARNING: Exact block not found. Trying regex.")
    
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Buttons fixed.")
