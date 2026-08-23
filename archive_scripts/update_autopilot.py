import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the weather promo label block with the new configurable block
old_weather_html = """<label style="display: flex; align-items: center; gap: 12px; cursor: pointer; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0;">
                                    <input type="checkbox" id="magic-weather-promo" style="width: 18px; height: 18px; accent-color: #8b5cf6;">
                                    <div>
                                        <span style="font-size: 14px; font-weight: 700; color: #1e293b; display: block;">Activar Promo de Lluvia (Weather API)</span>
                                        <span style="font-size: 12px; color: #64748b;">Lanza notificaciones Push automáticas si empieza a llover cerca de la sucursal.</span>
                                    </div>
                                </label>"""

new_weather_html = """<label style="display: flex; align-items: center; gap: 12px; cursor: pointer; background: #f8fafc; padding: 12px; border-radius: 8px 8px 0 0; border: 1px solid #e2e8f0; border-bottom: none;">
                                    <input type="checkbox" id="magic-weather-promo" onchange="document.getElementById('weather-config-panel').style.display = this.checked ? 'block' : 'none';" style="width: 18px; height: 18px; accent-color: #8b5cf6;">
                                    <div>
                                        <span style="font-size: 14px; font-weight: 700; color: #1e293b; display: block;">Activar Promo de Lluvia (OpenWeather API)</span>
                                        <span style="font-size: 12px; color: #64748b;">Lanza notificaciones Push automáticas si empieza a llover cerca de tu sucursal.</span>
                                    </div>
                                </label>
                                <div id="weather-config-panel" style="display: none; background: #ffffff; padding: 16px; border-radius: 0 0 8px 8px; border: 1px solid #e2e8f0; border-top: 1px dashed #cbd5e1; margin-bottom: 12px;">
                                    <div style="margin-bottom: 12px;">
                                        <label class="apple-label" style="font-size: 11px;">Ciudad para monitoreo del clima</label>
                                        <input type="text" id="magic-weather-city" class="apple-input fidelio-input" placeholder="Ej. Ciudad de México, Madrid..." value="Ciudad de México">
                                    </div>
                                    <div>
                                        <label class="apple-label" style="font-size: 11px;">Mensaje Push Automático (Flash Drop)</label>
                                        <input type="text" id="magic-weather-message" class="apple-input fidelio-input" placeholder="Ej. ¡Está lloviendo! Refúgiate con un 2x1 en Café." value="¡Está lloviendo! 🌧️ Ven a refugiarte y obtén 2x1 en capuchinos.">
                                    </div>
                                </div>"""

if "magic-weather-city" not in html:
    if old_weather_html in html:
        html = html.replace(old_weather_html, new_weather_html)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Updated autopilot UI successfully.")
    else:
        print("Could not find the old block to replace.")
else:
    print("Already updated.")
