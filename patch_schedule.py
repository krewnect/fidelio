import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_weather_panel = """                                <div id="weather-config-panel" style="display: none; background: #ffffff; padding: 16px; border-radius: 0 0 8px 8px; border: 1px solid #e2e8f0; border-top: 1px dashed #cbd5e1; margin-bottom: 12px;">
                                    <div style="margin-bottom: 12px;">
                                        <label class="apple-label" style="font-size: 11px;">Ciudad para monitoreo del clima</label>
                                        <input type="text" id="magic-weather-city" class="apple-input fidelio-input" placeholder="Ej. Ciudad de México, Madrid..." value="Ciudad de México">
                                    </div>
                                    <div>
                                        <label class="apple-label" style="font-size: 11px;">Mensaje Push Automático (Flash Drop)</label>
                                        <input type="text" id="magic-weather-message" class="apple-input fidelio-input" placeholder="Ej. ¡Está lloviendo! Refúgiate con un 2x1 en Café." value="¡Está lloviendo! 🌧️ Ven a refugiarte y obtén 2x1 en capuchinos.">
                                    </div>
                                </div>"""

new_weather_panel = """                                <div id="weather-config-panel" style="display: none; background: #ffffff; padding: 16px; border-radius: 0 0 8px 8px; border: 1px solid #e2e8f0; border-top: 1px dashed #cbd5e1; margin-bottom: 12px;">
                                    <div style="margin-bottom: 12px;">
                                        <label class="apple-label" style="font-size: 11px;">Ciudad para monitoreo del clima</label>
                                        <input type="text" id="magic-weather-city" class="apple-input fidelio-input" placeholder="Ej. Ciudad de México, Madrid..." value="Ciudad de México">
                                    </div>
                                    <div style="margin-bottom: 12px; display: flex; gap: 12px;">
                                        <div style="flex: 1;">
                                            <label class="apple-label" style="font-size: 11px;">Horario Activo (Inicio)</label>
                                            <input type="time" id="magic-weather-start" class="apple-input fidelio-input" value="10:00">
                                        </div>
                                        <div style="flex: 1;">
                                            <label class="apple-label" style="font-size: 11px;">Horario Activo (Fin)</label>
                                            <input type="time" id="magic-weather-end" class="apple-input fidelio-input" value="18:00">
                                        </div>
                                    </div>
                                    <div style="margin-bottom: 12px;">
                                        <label class="apple-label" style="font-size: 11px;">Días Válidos</label>
                                        <select id="magic-weather-days" class="apple-input fidelio-input" style="width: 100%;">
                                            <option value="all">Todos los días</option>
                                            <option value="weekdays">Lunes a Viernes</option>
                                            <option value="weekends">Fines de Semana</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="apple-label" style="font-size: 11px;">Mensaje Push Automático</label>
                                        <input type="text" id="magic-weather-message" class="apple-input fidelio-input" placeholder="Ej. ¡Está lloviendo! Refúgiate con un 2x1 en Café." value="¡Está lloviendo! 🌧️ Ven a refugiarte y obtén 2x1 en capuchinos.">
                                    </div>
                                </div>"""


old_flashdrop = """                                    <div style="margin-bottom: 16px;">
                                        <label class="apple-label" style="font-size: 11px; color: #991b1b;">Mensaje Push / Condiciones</label>
                                        <input type="text" id="magic-flash-message" class="apple-input fidelio-input" placeholder="Ej. 50% de descuento en la próxima hora." value="Obtén 30% OFF si nos visitas en los próximos 60 minutos.">
                                    </div>
                                    
                                    <button type="button" onclick="testFlashDrop()" class="fidelio-btn-primary" style="background: #ef4444 !important; width: 100%; border-color: #ef4444 !important;">
                                        <i class="fa-solid fa-bolt"></i> Lanzar Flash Drop Ahora
                                    </button>"""

new_flashdrop = """                                    <div style="margin-bottom: 12px;">
                                        <label class="apple-label" style="font-size: 11px; color: #991b1b;">Mensaje Push / Condiciones</label>
                                        <input type="text" id="magic-flash-message" class="apple-input fidelio-input" placeholder="Ej. 50% de descuento en la próxima hora." value="Obtén 30% OFF si nos visitas en los próximos 60 minutos.">
                                    </div>
                                    
                                    <div style="margin-bottom: 16px;">
                                        <label class="apple-label" style="font-size: 11px; color: #991b1b;">Programar Lanzamiento (Opcional)</label>
                                        <input type="datetime-local" id="magic-flash-schedule" class="apple-input fidelio-input" style="width: 100%;">
                                    </div>
                                    
                                    <button type="button" onclick="testFlashDrop()" class="fidelio-btn-primary" style="background: #ef4444 !important; width: 100%; border-color: #ef4444 !important;">
                                        <i class="fa-solid fa-bolt"></i> Programar / Lanzar Flash Drop
                                    </button>"""

if "magic-weather-start" not in html:
    html = html.replace(old_weather_panel, new_weather_panel)
    html = html.replace(old_flashdrop, new_flashdrop)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected scheduling config.")
else:
    print("Already scheduled.")
