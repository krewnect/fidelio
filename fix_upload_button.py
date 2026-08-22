import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html = """<label class="fidelio-btn-primary" style="flex: 1; height: 42px !important; box-sizing: border-box !important; white-space: nowrap; padding: 0 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important; margin: 0; cursor: pointer;">
                                <i class="fa-solid fa-cloud-arrow-up"></i> Subir CSV
                                <input type="file" id="upload-branches-csv" accept=".csv" style="display: none;" onchange="uploadBranchesCSV(event)">
                            </label>"""

new_html = """<button class="fidelio-btn-primary" onclick="document.getElementById('upload-branches-csv').click()" style="flex: 1; height: 42px !important; box-sizing: border-box !important; white-space: nowrap; padding: 0 16px !important; justify-content: center; min-width: 140px; font-size: 14px !important; margin: 0; cursor: pointer;">
                                <i class="fa-solid fa-cloud-arrow-up"></i> Subir CSV
                                <input type="file" id="upload-branches-csv" accept=".csv" style="display: none;" onchange="uploadBranchesCSV(event)">
                            </button>"""

if old_html in html:
    html = html.replace(old_html, new_html)
    print("Replaced button!")
else:
    print("WARNING: Could not find old_html block")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

