import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html = """                    <div style="margin-bottom: 20px; display: flex; gap: 16px; align-items: center;">
                        <input type="text" id="global-db-search" class="fidelio-input" placeholder="Buscar cliente por correo o nombre..." style="max-width: 400px;" oninput="filterGlobalDB(this.value)">
                    </div>
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 2px solid var(--border-soft); color: var(--text-muted);">
                                <th style="padding: 16px;">ID Cliente</th>
                                <th style="padding: 16px;">Nombre</th>
                                <th style="padding: 16px;">Email</th>
                                <th style="padding: 16px;">ID Restaurante</th>
                                <th style="padding: 16px;">Fecha de Registro</th>
                            </tr>
                        </thead>"""

new_html = """                    <div style="margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; background: var(--bg-main); padding: 16px; border-radius: 12px; border: 1px solid var(--border-soft);">
                        <input type="text" id="global-db-search" class="fidelio-input" placeholder="Buscar (Nombre / Hash)..." style="flex: 1; min-width: 200px;" oninput="filterGlobalDB()">
                        <input type="text" id="global-db-filter-business" class="fidelio-input" placeholder="Negocio/Restaurante..." style="width: 180px;" oninput="filterGlobalDB()">
                        <input type="text" id="global-db-filter-country" class="fidelio-input" placeholder="País..." style="width: 130px;" oninput="filterGlobalDB()">
                        <input type="text" id="global-db-filter-state" class="fidelio-input" placeholder="Estado..." style="width: 130px;" oninput="filterGlobalDB()">
                        <input type="text" id="global-db-filter-colonia" class="fidelio-input" placeholder="Colonia..." style="width: 130px;" oninput="filterGlobalDB()">
                    </div>
                    <table class="crm-table" style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="border-bottom: 2px solid var(--border-soft); color: var(--text-muted); font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">
                                <th style="padding: 16px;">ID / Hash</th>
                                <th style="padding: 16px;">Nombre</th>
                                <th style="padding: 16px;">Contacto <i class="fa-solid fa-shield-halved" style="color:var(--accent-violet);" title="Privacidad Activada"></i></th>
                                <th style="padding: 16px;">Negocio</th>
                                <th style="padding: 16px;">Ubicación Origen</th>
                                <th style="padding: 16px;">Registro</th>
                            </tr>
                        </thead>"""

if old_html in html:
    html = html.replace(old_html, new_html)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("HTML for global DB updated.")
else:
    print("WARNING: Could not find old HTML structure in index.html")
