import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the HTML for the Quick Templates
old_html_start = '<!-- Plantilla Cafetería -->'
old_html_end = '<!-- Desde Cero -->'

new_html = """<!-- Plantilla Médicos -->
                <div class="content-panel hover-glow" onclick="applyQuickTemplate('medico')" style="background:var(--surface); border:1px solid var(--border-soft); border-radius:16px; padding:24px; text-align:center; cursor:pointer; transition:all 0.2s;">
                    <div style="width:60px; height:60px; border-radius:50%; background:rgba(13, 148, 136, 0.1); color:#0d9488; display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 16px;">
                        <i class="fa-solid fa-heart-pulse"></i>
                    </div>
                    <h4 style="margin:0 0 8px; font-size:18px; color: var(--text-main);">Salud y Bienestar</h4>
                    <p style="margin:0; font-size:12px; color:var(--text-muted);">Doctores, Dentistas, Nutriólogos. Descuento en consultas.</p>
                </div>

                <!-- Plantilla Belleza -->
                <div class="content-panel hover-glow" onclick="applyQuickTemplate('belleza')" style="background:var(--surface); border:1px solid var(--border-soft); border-radius:16px; padding:24px; text-align:center; cursor:pointer; transition:all 0.2s;">
                    <div style="width:60px; height:60px; border-radius:50%; background:rgba(217, 70, 239, 0.1); color:#d946ef; display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 16px;">
                        <i class="fa-solid fa-scissors"></i>
                    </div>
                    <h4 style="margin:0 0 8px; font-size:18px; color: var(--text-main);">Belleza y Estética</h4>
                    <p style="margin:0; font-size:12px; color:var(--text-muted);">Barberos, Estilistas, Manicuristas. Recompensas en servicios.</p>
                </div>

                <!-- Plantilla Clases -->
                <div class="content-panel hover-glow" onclick="applyQuickTemplate('clases')" style="background:var(--surface); border:1px solid var(--border-soft); border-radius:16px; padding:24px; text-align:center; cursor:pointer; transition:all 0.2s;">
                    <div style="width:60px; height:60px; border-radius:50%; background:rgba(59, 130, 246, 0.1); color:#3b82f6; display:flex; align-items:center; justify-content:center; font-size:28px; margin:0 auto 16px;">
                        <i class="fa-solid fa-dumbbell"></i>
                    </div>
                    <h4 style="margin:0 0 8px; font-size:18px; color: var(--text-main);">Clases y Deportes</h4>
                    <p style="margin:0; font-size:12px; color:var(--text-muted);">Instructores, Entrenadores, Paseadores. Sesiones gratis.</p>
                </div>

                <!-- Desde Cero -->"""

pattern = re.compile(re.escape(old_html_start) + r'.*?' + re.escape(old_html_end), re.DOTALL)
html = pattern.sub(new_html, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# Update JS logic
with open('dashboard_v2.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_js_start = "if(type === 'cafeteria') {"
old_js_end = "        } else {"

new_js = """if(type === 'medico') {
            state.restaurantName = "Dr(a). Nombre / Especialidad";
            state.colorPrimary = "#134e4a";
            state.colorAccent = "#0d9488";
            state.iconClass = "fa-stethoscope";
            state.stampsReward = "¡Felicidades! Tienes 50% de Descuento en tu próxima consulta.";
            state.dynamicDesc = "Acumula tus visitas y cuida de tu salud.";
            state.activeMode = 'stamps';
        } else if(type === 'belleza') {
            state.restaurantName = "Nombre - Estilista/Barbero";
            state.colorPrimary = "#312e81";
            state.colorAccent = "#d946ef";
            state.iconClass = "fa-scissors";
            state.stampsReward = "¡Llegaste a la meta! Tienes un servicio de cortesía o Masaje Capilar.";
            state.dynamicDesc = "Cada visita cuenta. Premia tu estilo.";
            state.activeMode = 'stamps';
        } else if(type === 'clases') {
            state.restaurantName = "Coach / Instructor";
            state.colorPrimary = "#1e3a8a";
            state.colorAccent = "#3b82f6";
            state.iconClass = "fa-dumbbell";
            state.stampsReward = "¡Logrado! Te has ganado 1 Sesión de Entrenamiento Gratis.";
            state.dynamicDesc = "Acumula tus sesiones y alcanza tus metas.";
            state.activeMode = 'stamps';
        } else {"""

pattern2 = re.compile(re.escape(old_js_start) + r'.*?' + re.escape(old_js_end), re.DOTALL)
js = pattern2.sub(new_js, js)

with open('dashboard_v2.js', 'w', encoding='utf-8') as f:
    f.write(js)
